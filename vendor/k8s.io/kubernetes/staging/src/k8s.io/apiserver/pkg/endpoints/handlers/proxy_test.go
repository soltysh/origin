package handlers

import (
	"bufio"
	"io/ioutil"
	"net"
	"net/http"
	"net/http/httptest"
	"net/url"
	"testing"
	"time"

	"github.com/stretchr/testify/require"

	"k8s.io/apimachinery/pkg/util/httpstream"
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

	proxyHandler := &ProxyHandler{
	//Prefix     string
	//Storage    map[string]rest.Storage
	//Serializer runtime.NegotiatedSerializer
	//Mapper     request.RequestContextMapper
	}
	proxy := httptest.NewServer(proxyHandler)
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
