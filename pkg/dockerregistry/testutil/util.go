package testutil

import (
	"archive/tar"
	"bytes"
	"crypto/rand"
	"fmt"
	"io"
	"io/ioutil"
	mrand "math/rand"
	"net/http"
	"net/url"
	"time"

	"github.com/docker/distribution"
	"github.com/docker/distribution/context"
	"github.com/docker/distribution/digest"
	distclient "github.com/docker/distribution/registry/client"
	"github.com/docker/distribution/registry/client/auth"
	"github.com/docker/distribution/registry/client/transport"
)

// UploadTestBlob generates a random tar file and uploads it to the given repository.
func UploadTestBlob(serverURL *url.URL, creds auth.CredentialStore, repoName string) (distribution.Descriptor, []byte, error) {
	rs, ds, err := CreateRandomTarFile()
	if err != nil {
		return distribution.Descriptor{}, nil, fmt.Errorf("unexpected error generating test layer file: %v", err)
	}
	dgst := digest.Digest(ds)

	ctx := context.Background()
	if err != nil {
		return distribution.Descriptor{}, nil, err
	}

	var rt http.RoundTripper
	if creds != nil {
		challengeManager := auth.NewSimpleChallengeManager()
		_, err := ping(challengeManager, serverURL.String()+"/v2/", "")
		if err != nil {
			return distribution.Descriptor{}, nil, err
		}
		rt = transport.NewTransport(
			nil,
			auth.NewAuthorizer(
				challengeManager,
				auth.NewTokenHandler(nil, creds, repoName, "pull", "push"),
				auth.NewBasicHandler(creds)))
	}
	repo, err := distclient.NewRepository(ctx, repoName, serverURL.String(), rt)
	if err != nil {
		return distribution.Descriptor{}, nil, fmt.Errorf("failed to get repository %q: %v", repoName, err)
	}

	wr, err := repo.Blobs(ctx).Create(ctx)
	if err != nil {
		return distribution.Descriptor{}, nil, err
	}
	if _, err := io.Copy(wr, rs); err != nil {
		return distribution.Descriptor{}, nil, fmt.Errorf("unexpected error copying to upload: %v", err)
	}
	desc, err := wr.Commit(ctx, distribution.Descriptor{Digest: dgst})
	if err != nil {
		return distribution.Descriptor{}, nil, err
	}

	if _, err := rs.Seek(0, 0); err != nil {
		return distribution.Descriptor{}, nil, fmt.Errorf("failed to seak blob reader: %v", err)
	}
	content, err := ioutil.ReadAll(rs)
	if err != nil {
		return distribution.Descriptor{}, nil, fmt.Errorf("failed to read blob content: %v", err)
	}

	return desc, content, nil
}

// createRandomTarFile creates a random tarfile, returning it as an io.ReadSeeker along with its digest. An
// error is returned if there is a problem generating valid content. Inspired by
// github.com/vendor/docker/distribution/testutil/tarfile.go.
func CreateRandomTarFile() (rs io.ReadSeeker, dgst digest.Digest, err error) {
	nFiles := 2
	target := &bytes.Buffer{}
	wr := tar.NewWriter(target)

	// Perturb this on each iteration of the loop below.
	header := &tar.Header{
		Mode:       0644,
		ModTime:    time.Now(),
		Typeflag:   tar.TypeReg,
		Uname:      "randocalrissian",
		Gname:      "cloudcity",
		AccessTime: time.Now(),
		ChangeTime: time.Now(),
	}

	for fileNumber := 0; fileNumber < nFiles; fileNumber++ {
		fileSize := mrand.Int63n(1<<9) + 1<<9

		header.Name = fmt.Sprint(fileNumber)
		header.Size = fileSize

		if err := wr.WriteHeader(header); err != nil {
			return nil, "", err
		}

		randomData := make([]byte, fileSize)

		// Fill up the buffer with some random data.
		n, err := rand.Read(randomData)

		if n != len(randomData) {
			return nil, "", fmt.Errorf("short read creating random reader: %v bytes != %v bytes", n, len(randomData))
		}

		if err != nil {
			return nil, "", err
		}

		nn, err := io.Copy(wr, bytes.NewReader(randomData))
		if nn != fileSize {
			return nil, "", fmt.Errorf("short copy writing random file to tar")
		}

		if err != nil {
			return nil, "", err
		}

		if err := wr.Flush(); err != nil {
			return nil, "", err
		}
	}

	if err := wr.Close(); err != nil {
		return nil, "", err
	}

	dgst, err = digest.FromBytes(target.Bytes())
	if err != nil {
		return nil, "", err
	}

	return bytes.NewReader(target.Bytes()), dgst, nil
}

type testCredentialStore struct {
	username      string
	password      string
	refreshTokens map[string]string
}

var _ auth.CredentialStore = &testCredentialStore{}

// NewBasicCredentialStore returns a test credential store for use with registry token handler and/or basic
// handler.
func NewBasicCredentialStore(username, password string) auth.CredentialStore {
	return &testCredentialStore{
		username: username,
		password: password,
	}
}

func (tcs *testCredentialStore) Basic(*url.URL) (string, string) {
	return tcs.username, tcs.password
}

func (tcs *testCredentialStore) RefreshToken(u *url.URL, service string) string {
	return tcs.refreshTokens[service]
}

func (tcs *testCredentialStore) SetRefreshToken(u *url.URL, service string, token string) {
	if tcs.refreshTokens != nil {
		tcs.refreshTokens[service] = token
	}
}

// ping pings the provided endpoint to determine its required authorization challenges.
// If a version header is provided, the versions will be returned.
func ping(manager auth.ChallengeManager, endpoint, versionHeader string) ([]auth.APIVersion, error) {
	resp, err := http.Get(endpoint)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if err := manager.AddResponse(resp); err != nil {
		return nil, err
	}

	return auth.APIVersions(resp, versionHeader), err
}
