/*
Copyright 2014 The Kubernetes Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package rest

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strings"
	"sync"
	"time"

	"github.com/golang/glog"
	"github.com/mxk/go-flowrate/flowrate"
	"k8s.io/kubernetes/pkg/api/errors"
	"k8s.io/kubernetes/pkg/util/httpstream"
	"k8s.io/kubernetes/pkg/util/net"
	"k8s.io/kubernetes/pkg/util/proxy"
)

// UpgradeAwareProxyHandler is a handler for proxy requests that may require an upgrade
type UpgradeAwareProxyHandler struct {
	UpgradeRequired bool
	Location        *url.URL
	// Transport provides an optional round tripper to use to proxy. If nil, the default proxy transport is used
	Transport http.RoundTripper
	// WrapTransport indicates whether the provided Transport should be wrapped with default proxy transport behavior (URL rewriting, X-Forwarded-* header setting)
	WrapTransport  bool
	FlushInterval  time.Duration
	MaxBytesPerSec int64
	Responder      ErrorResponder
}

const defaultFlushInterval = 200 * time.Millisecond

// ErrorResponder abstracts error reporting to the proxy handler to remove the need to hardcode a particular
// error format.
type ErrorResponder interface {
	Error(err error)
}

// NewUpgradeAwareProxyHandler creates a new proxy handler with a default flush interval. Responder is required for returning
// errors to the caller.
func NewUpgradeAwareProxyHandler(location *url.URL, transport http.RoundTripper, wrapTransport, upgradeRequired bool, responder ErrorResponder) *UpgradeAwareProxyHandler {
	return &UpgradeAwareProxyHandler{
		Location:        location,
		Transport:       transport,
		WrapTransport:   wrapTransport,
		UpgradeRequired: upgradeRequired,
		FlushInterval:   defaultFlushInterval,
		Responder:       responder,
	}
}

// ServeHTTP handles the proxy request
func (h *UpgradeAwareProxyHandler) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	if len(h.Location.Scheme) == 0 {
		h.Location.Scheme = "http"
	}
	if h.tryUpgrade(w, req) {
		return
	}
	if h.UpgradeRequired {
		h.Responder.Error(errors.NewBadRequest("Upgrade request required"))
		return
	}

	loc := *h.Location
	loc.RawQuery = req.URL.RawQuery

	// If original request URL ended in '/', append a '/' at the end of the
	// of the proxy URL
	if !strings.HasSuffix(loc.Path, "/") && strings.HasSuffix(req.URL.Path, "/") {
		loc.Path += "/"
	}

	// From pkg/apiserver/proxy.go#ServeHTTP:
	// Redirect requests with an empty path to a location that ends with a '/'
	// This is essentially a hack for http://issue.k8s.io/4958.
	// Note: Keep this code after tryUpgrade to not break that flow.
	if len(loc.Path) == 0 {
		var queryPart string
		if len(req.URL.RawQuery) > 0 {
			queryPart = "?" + req.URL.RawQuery
		}
		w.Header().Set("Location", req.URL.Path+"/"+queryPart)
		w.WriteHeader(http.StatusMovedPermanently)
		return
	}

	if h.Transport == nil || h.WrapTransport {
		h.Transport = h.defaultProxyTransport(req.URL, h.Transport)
	}

	newReq, err := http.NewRequest(req.Method, loc.String(), req.Body)
	if err != nil {
		h.Responder.Error(err)
		return
	}
	newReq.Header = req.Header
	newReq.ContentLength = req.ContentLength
	// Copy the TransferEncoding is for future-proofing. Currently Go only supports "chunked" and
	// it can determine the TransferEncoding based on ContentLength and the Body.
	newReq.TransferEncoding = req.TransferEncoding

	proxy := httputil.NewSingleHostReverseProxy(&url.URL{Scheme: h.Location.Scheme, Host: h.Location.Host})
	proxy.Transport = h.Transport
	proxy.FlushInterval = h.FlushInterval
	proxy.ServeHTTP(w, newReq)
}

// tryUpgrade returns true if the request was handled.
func (h *UpgradeAwareProxyHandler) tryUpgrade(w http.ResponseWriter, req *http.Request) bool {
	if !httpstream.IsUpgradeRequest(req) {
		return false
	}

	backendConn, err := proxy.DialURL(h.Location, h.Transport)
	if err != nil {
		h.Responder.Error(err)
		return true
	}
	defer backendConn.Close()

	newReq, err := http.NewRequest(req.Method, h.Location.String(), req.Body)
	if err != nil {
		h.Responder.Error(err)
		return true
	}
	newReq.Header = req.Header
	if err = newReq.Write(backendConn); err != nil {
		h.Responder.Error(err)
		return true
	}

	// determine the http response code from the backend by reading from backendConn
	rawResponseCode, headerBytes, err := getResponseCode(backendConn)
	if err != nil {
		glog.V(6).Infof("Proxy connection error: %v", err)
		h.Responder.Error(fmt.Errorf("Proxy connection error: %v", err))
		return true
	}

	// Once the connection is hijacked, the ErrorResponder will no longer work, so
	// hijacking should be the last step in the upgrade.
	requestHijacker, ok := w.(http.Hijacker)
	if !ok {
		h.Responder.Error(fmt.Errorf("request connection cannot be hijacked: %T", w))
		return true
	}
	requestHijackedConn, _, err := requestHijacker.Hijack()
	if err != nil {
		h.Responder.Error(fmt.Errorf("error hijacking request connection: %v", err))
		return true
	}
	defer requestHijackedConn.Close()

	// Forward raw response bytes back to client.
	if len(headerBytes) > 0 {
		if _, err = requestHijackedConn.Write(headerBytes); err != nil {
			h.Responder.Error(fmt.Errorf("error hijacking request connection: %v", err))
			return true
		}
	}
	if rawResponseCode != http.StatusSwitchingProtocols {
		// If the backend did not upgrade the request, finish echoing the response from the backend to the client and return, closing the connection.
		glog.V(6).Infof("Proxy upgrade error, status code %d", rawResponseCode)
		_, err := io.Copy(requestHijackedConn, backendConn)
		if err != nil && !strings.Contains(err.Error(), "use of closed network connection") {
			glog.Errorf("Error proxying data from backend to client: %v", err)
		}
		// Indicate we handled the request
		return true
	}

	// Proxy the connection.
	wg := &sync.WaitGroup{}
	wg.Add(2)

	go func() {
		var writer io.WriteCloser
		if h.MaxBytesPerSec > 0 {
			writer = flowrate.NewWriter(backendConn, h.MaxBytesPerSec)
		} else {
			writer = backendConn
		}
		_, err := io.Copy(writer, requestHijackedConn)
		if err != nil && !strings.Contains(err.Error(), "use of closed network connection") {
			glog.Errorf("Error proxying data from client to backend: %v", err)
		}
		wg.Done()
	}()

	go func() {
		var reader io.ReadCloser
		if h.MaxBytesPerSec > 0 {
			reader = flowrate.NewReader(backendConn, h.MaxBytesPerSec)
		} else {
			reader = backendConn
		}
		_, err := io.Copy(requestHijackedConn, reader)
		if err != nil && !strings.Contains(err.Error(), "use of closed network connection") {
			glog.Errorf("Error proxying data from backend to client: %v", err)
		}
		wg.Done()
	}()

	wg.Wait()
	return true
}

func (h *UpgradeAwareProxyHandler) defaultProxyTransport(url *url.URL, internalTransport http.RoundTripper) http.RoundTripper {
	scheme := url.Scheme
	host := url.Host
	suffix := h.Location.Path
	if strings.HasSuffix(url.Path, "/") && !strings.HasSuffix(suffix, "/") {
		suffix += "/"
	}
	pathPrepend := strings.TrimSuffix(url.Path, suffix)
	rewritingTransport := &proxy.Transport{
		Scheme:       scheme,
		Host:         host,
		PathPrepend:  pathPrepend,
		RoundTripper: internalTransport,
	}
	return &corsRemovingTransport{
		RoundTripper: rewritingTransport,
	}
}

// getResponseCode reads a http response from the given reader, returns the status code,
// the bytes read from the reader, and any error encountered
func getResponseCode(r io.Reader) (int, []byte, error) {
	rawResponse := bytes.NewBuffer(make([]byte, 0, 256))
	// Save the bytes read while reading the response headers into the rawResponse buffer
	resp, err := http.ReadResponse(bufio.NewReader(io.TeeReader(r, rawResponse)), nil)
	if err != nil {
		return 0, nil, err
	}
	// return the http status code and the raw bytes consumed from the reader in the process
	return resp.StatusCode, rawResponse.Bytes(), nil
}

// corsRemovingTransport is a wrapper for an internal transport. It removes CORS headers
// from the internal response.
type corsRemovingTransport struct {
	http.RoundTripper
}

func (p *corsRemovingTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	resp, err := p.RoundTripper.RoundTrip(req)
	if err != nil {
		return nil, err
	}
	removeCORSHeaders(resp)
	return resp, nil
}

var _ = net.RoundTripperWrapper(&corsRemovingTransport{})

func (rt *corsRemovingTransport) WrappedRoundTripper() http.RoundTripper {
	return rt.RoundTripper
}

// removeCORSHeaders strip CORS headers sent from the backend
// This should be called on all responses before returning
func removeCORSHeaders(resp *http.Response) {
	resp.Header.Del("Access-Control-Allow-Credentials")
	resp.Header.Del("Access-Control-Allow-Headers")
	resp.Header.Del("Access-Control-Allow-Methods")
	resp.Header.Del("Access-Control-Allow-Origin")
}
