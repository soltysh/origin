package server

import (
	"bytes"
	"crypto/sha256"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"net/url"
	"os"
	"strconv"
	"strings"
	"testing"
	"time"

	log "github.com/Sirupsen/logrus"

	"github.com/docker/distribution"
	"github.com/docker/distribution/configuration"
	"github.com/docker/distribution/context"
	"github.com/docker/distribution/digest"
	"github.com/docker/distribution/manifest/schema1"
	//"github.com/docker/distribution/registry/api/v2"
	"github.com/docker/distribution/registry/handlers"
	_ "github.com/docker/distribution/registry/storage/driver/inmemory"

	ktestclient "k8s.io/kubernetes/pkg/client/unversioned/testclient"

	"github.com/openshift/origin/pkg/client/testclient"
	registrytest "github.com/openshift/origin/pkg/dockerregistry/testutil"
	imagetest "github.com/openshift/origin/pkg/image/admission/testutil"
	imageapi "github.com/openshift/origin/pkg/image/api"
)

func TestPullthroughServeBlob(t *testing.T) {
	ctx := context.Background()

	installFakeAccessController(t)

	testImage, err := registrytest.NewImageForManifest("user/app", registrytest.SampleImageManifestSchema1, false)
	if err != nil {
		t.Fatal(err)
	}
	client := &testclient.Fake{}
	client.AddReactor("get", "images", registrytest.GetFakeImageGetHandler(t, *testImage))

	// TODO: get rid of those nasty global vars
	backupRegistryClient := DefaultRegistryClient
	DefaultRegistryClient = makeFakeRegistryClient(client, ktestclient.NewSimpleFake())
	defer func() {
		// set it back once this test finishes to make other unit tests working again
		DefaultRegistryClient = backupRegistryClient
	}()

	// pullthrough middleware will attempt to pull from this registry instance
	remoteRegistryApp := handlers.NewApp(ctx, &configuration.Configuration{
		Loglevel: "debug",
		Auth: map[string]configuration.Parameters{
			fakeAuthorizerName: {"realm": fakeAuthorizerName},
		},
		Storage: configuration.Storage{
			"inmemory": configuration.Parameters{},
			"cache": configuration.Parameters{
				"blobdescriptor": "inmemory",
			},
			"delete": configuration.Parameters{
				"enabled": true,
			},
		},
		Middleware: map[string][]configuration.Middleware{
			"registry":   {{Name: "openshift"}},
			"repository": {{Name: "openshift"}},
			"storage":    {{Name: "openshift"}},
		},
	})
	remoteRegistryServer := httptest.NewServer(remoteRegistryApp)
	defer remoteRegistryServer.Close()

	serverURL, err := url.Parse(remoteRegistryServer.URL)
	if err != nil {
		t.Fatalf("error parsing server url: %v", err)
	}
	os.Setenv("DOCKER_REGISTRY_URL", serverURL.Host)
	testImage.DockerImageReference = fmt.Sprintf("%s/%s@%s", serverURL.Host, "user/app", testImage.Name)

	testImageStream := registrytest.TestNewImageStreamObject("user", "app", "latest", testImage.Name, testImage.DockerImageReference)
	if testImageStream.Annotations == nil {
		testImageStream.Annotations = make(map[string]string)
	}
	testImageStream.Annotations[imageapi.InsecureRepositoryAnnotation] = "true"

	client.AddReactor("get", "imagestreams", imagetest.GetFakeImageStreamGetHandler(t, *testImageStream))

	blob1Desc, blob1Content, err := registrytest.UploadTestBlob(serverURL, nil, "user/app")
	if err != nil {
		t.Fatal(err)
	}
	blob2Desc, blob2Content, err := registrytest.UploadTestBlob(serverURL, nil, "user/app")
	if err != nil {
		t.Fatal(err)
	}

	blob1Storage := map[digest.Digest][]byte{blob1Desc.Digest: blob1Content}
	blob2Storage := map[digest.Digest][]byte{blob2Desc.Digest: blob2Content}

	for _, tc := range []struct {
		name                       string
		method                     string
		blobDigest                 digest.Digest
		localBlobs                 map[digest.Digest][]byte
		expectedStatError          error
		expectedContentLength      int64
		expectedBytesServed        int64
		expectedBytesServedLocally int64
		expectedLocalCalls         map[string]int
	}{
		{
			name:                  "stat local blob",
			method:                "HEAD",
			blobDigest:            blob1Desc.Digest,
			localBlobs:            blob1Storage,
			expectedContentLength: int64(len(blob1Content)),
			expectedLocalCalls: map[string]int{
				"Stat":      1,
				"ServeBlob": 1,
			},
		},

		{
			name:                       "serve local blob",
			method:                     "GET",
			blobDigest:                 blob1Desc.Digest,
			localBlobs:                 blob1Storage,
			expectedContentLength:      int64(len(blob1Content)),
			expectedBytesServed:        int64(len(blob1Content)),
			expectedBytesServedLocally: int64(len(blob1Content)),
			expectedLocalCalls: map[string]int{
				"Stat":      1,
				"ServeBlob": 1,
			},
		},

		{
			name:                  "stat remote blob",
			method:                "HEAD",
			blobDigest:            blob1Desc.Digest,
			localBlobs:            blob2Storage,
			expectedContentLength: int64(len(blob1Content)),
			expectedLocalCalls: map[string]int{
				"Stat":      1,
				"ServeBlob": 1,
			},
		},

		{
			name:                  "serve remote blob",
			method:                "GET",
			blobDigest:            blob1Desc.Digest,
			expectedContentLength: int64(len(blob1Content)),
			expectedBytesServed:   int64(len(blob1Content)),
			expectedLocalCalls: map[string]int{
				"Stat":      1,
				"ServeBlob": 1,
			},
		},

		{
			name:               "unknown blob digest",
			method:             "GET",
			blobDigest:         unknownBlobDigest,
			expectedStatError:  distribution.ErrBlobUnknown,
			expectedLocalCalls: map[string]int{"Stat": 1},
		},
	} {
		localBlobStore := newTestBlobStore(tc.localBlobs)

		cachedLayers, err := newDigestToRepositoryCache(10)
		if err != nil {
			t.Fatal(err)
		}
		repo := &repository{
			ctx:              ctx,
			namespace:        "user",
			name:             "app",
			pullthrough:      true,
			cachedLayers:     cachedLayers,
			registryOSClient: client,
		}

		rbs := &remoteBlobGetterService{
			repo:          repo,
			digestToStore: make(map[string]distribution.BlobStore),
		}

		ctx = WithRemoteBlobGetter(ctx, rbs)

		ptbs := &pullthroughBlobStore{
			BlobStore: localBlobStore,
			repo:      repo,
		}

		req, err := http.NewRequest(tc.method, fmt.Sprintf("http://example.org/v2/user/app/blobs/%s", tc.blobDigest), nil)
		if err != nil {
			t.Fatalf("[%s] failed to create http request: %v", tc.name, err)
		}
		w := httptest.NewRecorder()

		dgst := digest.Digest(tc.blobDigest)

		_, err = ptbs.Stat(ctx, dgst)
		if err != tc.expectedStatError {
			t.Errorf("[%s] Stat returned unexpected error: %#+v != %#+v", tc.name, err, tc.expectedStatError)
		}
		if err != nil || tc.expectedStatError != nil {
			continue
		}
		err = ptbs.ServeBlob(ctx, w, req, dgst)
		if err != nil {
			t.Errorf("[%s] unexpected ServeBlob error: %v", tc.name, err)
			continue
		}

		clstr := w.Header().Get("Content-Length")
		if cl, err := strconv.ParseInt(clstr, 10, 64); err != nil {
			t.Errorf(`[%s] unexpected Content-Length: %q != "%d"`, tc.name, clstr, tc.expectedContentLength)
		} else {
			if cl != tc.expectedContentLength {
				t.Errorf("[%s] Content-Length does not match expected size: %d != %d", tc.name, cl, tc.expectedContentLength)
			}
		}
		if w.Header().Get("Content-Type") != "application/octet-stream" {
			t.Errorf("[%s] Content-Type does not match expected: %q != %q", tc.name, w.Header().Get("Content-Type"), "application/octet-stream")
		}

		body := w.Body.Bytes()
		if int64(len(body)) != tc.expectedBytesServed {
			t.Errorf("[%s] unexpected size of body: %d != %d", tc.name, len(body), tc.expectedBytesServed)
		}

		for name, expCount := range tc.expectedLocalCalls {
			count := localBlobStore.calls[name]
			if count != expCount {
				t.Errorf("[%s] expected %d calls to method %s of local blob store, not %d", tc.name, expCount, name, count)
			}
		}
		for name, count := range localBlobStore.calls {
			if _, exists := tc.expectedLocalCalls[name]; !exists {
				t.Errorf("[%s] expected no calls to method %s of local blob store, got %d", tc.name, name, count)
			}
		}

		if localBlobStore.bytesServed != tc.expectedBytesServedLocally {
			t.Errorf("[%s] unexpected number of bytes served locally: %d != %d", tc.name, localBlobStore.bytesServed, tc.expectedBytesServed)
		}
	}
}

func TestPullthroughServeNotSeekableBlob(t *testing.T) {
	namespace, name := "user", "app"
	repoName := fmt.Sprintf("%s/%s", namespace, name)
	log.SetLevel(log.DebugLevel)
	installFakeAccessController(t)
	setPassthroughBlobDescriptorServiceFactory()

	testImage, err := registrytest.NewImageForManifest(repoName, registrytest.SampleImageManifestSchema1, false)
	if err != nil {
		t.Fatal(err)
	}
	client := &testclient.Fake{}
	client.AddReactor("get", "images", registrytest.GetFakeImageGetHandler(t, *testImage))

	// TODO: get rid of those nasty global vars
	backupRegistryClient := DefaultRegistryClient
	DefaultRegistryClient = makeFakeRegistryClient(client, ktestclient.NewSimpleFake())
	defer func() {
		// set it back once this test finishes to make other unit tests working again
		DefaultRegistryClient = backupRegistryClient
	}()

	reader, dgst, err := registrytest.CreateRandomTarFile()
	if err != nil {
		t.Fatalf("unexpected error generating test layer file: %v", err)
	}

	blob1Content, err := ioutil.ReadAll(reader)
	if err != nil {
		t.Fatalf("failed to read blob content: %v", err)
	}

	blob1Storage := map[digest.Digest][]byte{dgst: blob1Content}

	// start regular HTTP server
	remoteRegistryServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		t.Logf("External registry got %s %s", r.Method, r.URL.Path)

		w.Header().Set("Docker-Distribution-API-Version", "registry/2.0")

		switch r.URL.Path {
		case "/v2/":
			w.Write([]byte(`{}`))
		case "/v2/" + repoName + "/tags/list":
			w.Write([]byte("{\"name\": \"" + repoName + "\", \"tags\": [\"latest\"]}"))
		case "/v2/" + repoName + "/manifests/latest", "/v2/" + repoName + "/manifests/" + etcdDigest:
			if r.Method == "HEAD" {
				w.Header().Set("Content-Length", fmt.Sprintf("%d", len(etcdManifest)))
				w.Header().Set("Docker-Content-Digest", etcdDigest)
				w.WriteHeader(http.StatusOK)
			} else {
				w.Write([]byte(etcdManifest))
			}
		default:
			if strings.HasPrefix(r.URL.Path, "/v2/"+repoName+"/blobs/") {
				for dgst, payload := range blob1Storage {
					if r.URL.Path != "/v2/"+repoName+"/blobs/"+dgst.String() {
						continue
					}
					w.Header().Set("Content-Length", fmt.Sprintf("%d", len(payload)))
					if r.Method == "HEAD" {
						w.Header().Set("Docker-Content-Digest", dgst.String())
						w.WriteHeader(http.StatusOK)
						return
					} else {
						// Important!
						//
						// We need to return any return code between 200 and 399, expept 200 and 206.
						// https://github.com/docker/distribution/blob/master/registry/client/transport/http_reader.go#L192
						//
						// In this case the docker client library will make a not truly
						// seekable response.
						// https://github.com/docker/distribution/blob/master/registry/client/transport/http_reader.go#L239
						w.WriteHeader(http.StatusAccepted)
					}
					w.Write(payload)
					return
				}
			}
			t.Fatalf("unexpected request %s: %#v", r.URL.Path, r)
		}
	}))

	serverURL, err := url.Parse(remoteRegistryServer.URL)
	if err != nil {
		t.Fatalf("error parsing server url: %v", err)
	}
	os.Setenv("DOCKER_REGISTRY_URL", serverURL.Host)
	testImage.DockerImageReference = fmt.Sprintf("%s/%s@%s", serverURL.Host, repoName, testImage.Name)

	testImageStream := registrytest.TestNewImageStreamObject(namespace, name, "latest", testImage.Name, testImage.DockerImageReference)
	if testImageStream.Annotations == nil {
		testImageStream.Annotations = make(map[string]string)
	}
	testImageStream.Annotations[imageapi.InsecureRepositoryAnnotation] = "true"

	client.AddReactor("get", "imagestreams", imagetest.GetFakeImageStreamGetHandler(t, *testImageStream))

	localBlobStore := newTestBlobStore(nil)

	ctx := context.Background()
	ctx = WithTestPassthroughToUpstream(ctx, false)
	repo := newTestRepositoryForPullthrough(t, ctx, nil, namespace, name, client, true)

	rbs := &remoteBlobGetterService{
		repo:          repo,
		digestToStore: make(map[string]distribution.BlobStore),
	}
	ctx = WithRemoteBlobGetter(ctx, rbs)
	repo.ctx = ctx

	ptbs := &pullthroughBlobStore{
		BlobStore: localBlobStore,
		repo:      repo,
	}

	req, err := http.NewRequest("GET", fmt.Sprintf("http://example.org/v2/user/app/blobs/%s", dgst), nil)
	if err != nil {
		t.Fatalf("failed to create http request: %v", err)
	}
	w := httptest.NewRecorder()

	if _, err = ptbs.Stat(ctx, dgst); err != nil {
		t.Fatalf("Stat returned unexpected error: %#+v", err)
	}

	if err = ptbs.ServeBlob(ctx, w, req, dgst); err != nil {
		t.Fatalf("ServeBlob returned unexpected error: %#+v", err)
	}

	if w.Code != http.StatusOK {
		t.Fatalf(`unexpected StatusCode: %d (expected %d)`, w.Code, http.StatusOK)
	}

	clstr := w.Header().Get("Content-Length")
	if cl, err := strconv.ParseInt(clstr, 10, 64); err != nil {
		t.Fatalf(`unexpected Content-Length: %q (expected "%d")`, clstr, int64(len(blob1Content)))
	} else {
		if cl != int64(len(blob1Content)) {
			t.Fatalf("Content-Length does not match expected size: %d != %d", cl, int64(len(blob1Content)))
		}
	}

	body := w.Body.Bytes()
	if int64(len(body)) != int64(len(blob1Content)) {
		t.Errorf("unexpected size of body: %d != %d", len(body), int64(len(blob1Content)))
	}

	if localBlobStore.bytesServed != 0 {
		t.Fatalf("remote blob served locally")
	}

	expectedLocalCalls := map[string]int{
		"Stat":      1,
		"ServeBlob": 1,
	}

	for name, expCount := range expectedLocalCalls {
		count := localBlobStore.calls[name]
		if count != expCount {
			t.Errorf("expected %d calls to method %s of local blob store, not %d", expCount, name, count)
		}
	}

	for name, count := range localBlobStore.calls {
		if _, exists := expectedLocalCalls[name]; !exists {
			t.Errorf("expected no calls to method %s of local blob store, got %d", name, count)
		}
	}
}

func newTestRepositoryForPullthrough(
	t *testing.T,
	ctx context.Context,
	wrappedRepository distribution.Repository,
	namespace, name string,
	client *testclient.Fake,
	enablePullThrough bool,
) *repository {
	cachedLayers, err := newDigestToRepositoryCache(10)
	if err != nil {
		t.Fatal(err)
	}

	r := &repository{
		Repository:       wrappedRepository,
		ctx:              ctx,
		namespace:        namespace,
		name:             name,
		pullthrough:      enablePullThrough,
		cachedLayers:     cachedLayers,
		registryOSClient: client,
	}

	return r
}

const (
	unknownBlobDigest = "sha256:bef57ec7f53a6d40beb640a780a639c83bc29ac8a9816f1fc6c5c6dcd93c4721"
)

func makeDigestFromBytes(data []byte) digest.Digest {
	return digest.Digest(fmt.Sprintf("sha256:%x", sha256.Sum256(data)))
}

type testBlobStore struct {
	// blob digest mapped to content
	blobs map[digest.Digest][]byte
	// method name mapped to number of invocations
	calls       map[string]int
	bytesServed int64
}

var _ distribution.BlobStore = &testBlobStore{}

func newTestBlobStore(blobs map[digest.Digest][]byte) *testBlobStore {
	b := make(map[digest.Digest][]byte)
	for d, content := range blobs {
		b[d] = content
	}
	return &testBlobStore{
		blobs: b,
		calls: make(map[string]int),
	}
}

func (t *testBlobStore) Stat(ctx context.Context, dgst digest.Digest) (distribution.Descriptor, error) {
	t.calls["Stat"]++
	content, exists := t.blobs[dgst]
	if !exists {
		return distribution.Descriptor{}, distribution.ErrBlobUnknown
	}
	return distribution.Descriptor{
		MediaType: schema1.MediaTypeManifestLayer,
		Size:      int64(len(content)),
		Digest:    makeDigestFromBytes(content),
	}, nil
}

func (t *testBlobStore) Get(ctx context.Context, dgst digest.Digest) ([]byte, error) {
	t.calls["Get"]++
	content, exists := t.blobs[dgst]
	if !exists {
		return nil, distribution.ErrBlobUnknown
	}
	return content, nil
}

func (t *testBlobStore) Open(ctx context.Context, dgst digest.Digest) (distribution.ReadSeekCloser, error) {
	t.calls["Open"]++
	content, exists := t.blobs[dgst]
	if !exists {
		return nil, distribution.ErrBlobUnknown
	}
	return &testBlobFileReader{
		bs:      t,
		content: content,
	}, nil
}

func (t *testBlobStore) Put(ctx context.Context, mediaType string, p []byte) (distribution.Descriptor, error) {
	t.calls["Put"]++
	return distribution.Descriptor{}, fmt.Errorf("method not implemented")
}

func (t *testBlobStore) Create(ctx context.Context, options ...distribution.BlobCreateOption) (distribution.BlobWriter, error) {
	t.calls["Create"]++
	return nil, fmt.Errorf("method not implemented")
}

func (t *testBlobStore) Resume(ctx context.Context, id string) (distribution.BlobWriter, error) {
	t.calls["Resume"]++
	return nil, fmt.Errorf("method not implemented")
}

func (t *testBlobStore) ServeBlob(ctx context.Context, w http.ResponseWriter, req *http.Request, dgst digest.Digest) error {
	t.calls["ServeBlob"]++
	content, exists := t.blobs[dgst]
	if !exists {
		return distribution.ErrBlobUnknown
	}
	reader := bytes.NewReader(content)
	setResponseHeaders(w, int64(len(content)), "application/octet-stream", dgst)
	w.Header().Set("Content-Length", fmt.Sprintf("%d", int64(len(content))))
	http.ServeContent(w, req, dgst.String(), time.Time{}, reader)
	n, err := reader.Seek(0, 1)
	if err != nil {
		return err
	}
	t.bytesServed = n
	return nil
}

func (t *testBlobStore) Delete(ctx context.Context, dgst digest.Digest) error {
	t.calls["Delete"]++
	return fmt.Errorf("method not implemented")
}

type testBlobFileReader struct {
	bs      *testBlobStore
	content []byte
	offset  int64
}

var _ distribution.ReadSeekCloser = &testBlobFileReader{}

func (fr *testBlobFileReader) Read(p []byte) (n int, err error) {
	fr.bs.calls["ReadSeakCloser.Read"]++
	n = copy(p, fr.content[fr.offset:])
	fr.offset += int64(n)
	fr.bs.bytesServed += int64(n)
	return n, nil
}

func (fr *testBlobFileReader) Seek(offset int64, whence int) (int64, error) {
	fr.bs.calls["ReadSeakCloser.Seek"]++

	newOffset := fr.offset

	switch whence {
	case os.SEEK_CUR:
		newOffset += int64(offset)
	case os.SEEK_END:
		newOffset = int64(len(fr.content)) + offset
	case os.SEEK_SET:
		newOffset = int64(offset)
	}

	var err error
	if newOffset < 0 {
		err = fmt.Errorf("cannot seek to negative position")
	} else {
		// No problems, set the offset.
		fr.offset = newOffset
	}

	return fr.offset, err
}

func (fr *testBlobFileReader) Close() error {
	fr.bs.calls["ReadSeakCloser.Close"]++
	return nil
}
