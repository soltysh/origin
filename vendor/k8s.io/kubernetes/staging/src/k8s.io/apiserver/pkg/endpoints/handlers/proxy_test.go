package handlers

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/apimachinery/pkg/runtime/serializer"
	"k8s.io/apimachinery/pkg/util/httpstream"
	"k8s.io/apiserver/pkg/endpoints/handlers/responsewriters"
	"k8s.io/apiserver/pkg/endpoints/request"
	genericapirequest "k8s.io/apiserver/pkg/endpoints/request"
	"k8s.io/apiserver/pkg/registry/rest"
)

func TestProxyUpgradeErrorResponseTerminates(t *testing.T) {
	backend := http.NewServeMux()
	backend.Handle("/hello", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.Error(w, "Bad Request", 422)
	}))
	backend.Handle("/there", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		t.Error("request to /there")
	}))
	backendServer := httptest.NewServer(backend)
	defer backendServer.Close()
	backendServerURL, _ := url.Parse(backendServer.URL)
	backendServerURL.Path = "/hello"

	scheme := runtime.NewScheme()
	metav1.AddToGroupVersion(scheme, schema.GroupVersion{Group: "foo", Version: "v1"})

	proxyHandler := &ProxyHandler{
		//Prefix     string
		Storage: map[string]rest.Storage{
			"bars/proxy": fakeStorage{backendServerURL: backendServerURL},
		},
		Serializer: serializer.NewCodecFactory(scheme),
		Mapper:     request.NewRequestContextMapper(),
	}
	handler := withFakeRequestInfo(proxyHandler, fakeRequestInfoResolver{}, proxyHandler.Mapper)
	handler = request.WithRequestContext(handler, proxyHandler.Mapper)
	proxy := httptest.NewServer(handler)
	defer proxy.Close()
	proxyURL, _ := url.Parse(proxy.URL)
	conn, err := net.Dial("tcp", proxyURL.Host)
	require.NoError(t, err)
	bufferedReader := bufio.NewReader(conn)

	// Send upgrade request resulting in an error to the proxy server
	req, _ := http.NewRequest("GET", "/", nil)
	req.Header.Set(httpstream.HeaderConnection, httpstream.HeaderUpgrade)
	require.NoError(t, req.Write(conn))
	resp, err := http.ReadResponse(bufferedReader, nil)
	require.NoError(t, err)
	_, err = ioutil.ReadAll(resp.Body)
	require.NoError(t, err)
	resp.Body.Close()

	// Send another request
	req, _ = http.NewRequest("GET", "/there", nil)
	require.NoError(t, req.Write(conn))
	time.Sleep(time.Second)
	conn.SetReadDeadline(time.Now().Add(time.Second))
	resp, err = http.ReadResponse(bufferedReader, nil)
	require.Error(t, err)
}

type fakeRequestInfoResolver struct{}

func (fakeRequestInfoResolver) NewRequestInfo(req *http.Request) (*request.RequestInfo, error) {
	return &request.RequestInfo{
		IsResourceRequest: true,
		Path:              req.URL.Path,
		Verb:              req.Method,
		APIPrefix:         "/apis",
		APIGroup:          "foo",
		APIVersion:        "v1",
		Namespace:         "",
		Resource:          "bars/proxy",
		Subresource:       "proxy",
		Name:              "abc",
		Parts:             []string{"bars", "abc"},
	}, nil
}

type fakeStorage struct {
	backendServerURL *url.URL
}

func (fakeStorage) New() runtime.Object {
	return nil
}

func (s fakeStorage) ResourceLocation(ctx genericapirequest.Context, id string) (remoteLocation *url.URL, transport http.RoundTripper, err error) {
	return s.backendServerURL, http.DefaultTransport, nil
}

// withFakeRequestInfo attaches a RequestInfo to the context.
func withFakeRequestInfo(handler http.Handler, resolver fakeRequestInfoResolver, requestContextMapper request.RequestContextMapper) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, req *http.Request) {
		ctx, ok := requestContextMapper.Get(req)
		if !ok {
			responsewriters.InternalError(w, req, fmt.Errorf("no context found for request"))
			return
		}

		info, err := resolver.NewRequestInfo(req)
		if err != nil {
			responsewriters.InternalError(w, req, fmt.Errorf("failed to create RequestInfo: %v", err))
			return
		}

		requestContextMapper.Update(req, request.WithRequestInfo(ctx, info))

		handler.ServeHTTP(w, req)
	})
}
