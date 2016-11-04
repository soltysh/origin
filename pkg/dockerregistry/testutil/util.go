package testutil

import (
	"archive/tar"
	"bytes"
	"crypto/rand"
	"fmt"
	"io"
	"io/ioutil"
	mrand "math/rand"
	"net/url"
	"testing"
	"time"

	"github.com/docker/distribution"
	"github.com/docker/distribution/context"
	"github.com/docker/distribution/digest"
	"github.com/docker/distribution/manifest/schema1"
	distclient "github.com/docker/distribution/registry/client"

	kapi "k8s.io/kubernetes/pkg/api"
	kerrors "k8s.io/kubernetes/pkg/api/errors"
	ktestclient "k8s.io/kubernetes/pkg/client/unversioned/testclient"
	"k8s.io/kubernetes/pkg/runtime"

	imageapi "github.com/openshift/origin/pkg/image/api"
)

func NewImageForManifest(repoName string, rawManifest string, managedByOpenShift bool) (*imageapi.Image, error) {
	sm := schema1.SignedManifest{}
	if err := sm.UnmarshalJSON([]byte(rawManifest)); err != nil {
		return nil, err
	}

	payload, err := sm.Payload()
	if err != nil {
		return nil, err
	}

	// Calculate digest
	dgst, err := digest.FromBytes(payload)
	if err != nil {
		return nil, err
	}

	annotations := make(map[string]string)
	if managedByOpenShift {
		annotations[imageapi.ManagedByOpenShiftAnnotation] = "true"
	}

	img := &imageapi.Image{
		ObjectMeta: kapi.ObjectMeta{
			Name:        dgst.String(),
			Annotations: annotations,
		},
		DockerImageReference: fmt.Sprintf("localhost:5000/%s@%s", repoName, dgst),
		DockerImageManifest:  string(rawManifest),
	}

	if err := imageapi.ImageWithMetadata(img); err != nil {
		return nil, err
	}

	return img, nil
}

// UploadTestBlob generates a random tar file and uploads it to the given repository.
func UploadTestBlob(serverURL *url.URL, repoName string) (distribution.Descriptor, []byte, error) {
	rs, ds, err := CreateRandomTarFile()
	if err != nil {
		return distribution.Descriptor{}, nil, fmt.Errorf("unexpected error generating test layer file: %v", err)
	}
	dgst := digest.Digest(ds)

	ctx := context.Background()
	repo, err := distclient.NewRepository(ctx, repoName, serverURL.String(), nil)
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

const SampleImageManifestSchema1 = `{
   "schemaVersion": 1,
   "name": "nm/is",
   "tag": "latest",
   "architecture": "",
   "fsLayers": [
      {
         "blobSum": "sha256:b2c5513bd934a7efb412c0dd965600b8cb00575b585eaff1cb980b69037fe6cd"
      },
      {
         "blobSum": "sha256:2dde6f11a89463bf20dba3b47d8b3b6de7cdcc19e50634e95a18dd95c278768d"
      }
   ],
   "history": [
      {
         "v1Compatibility": "{\"size\":18407936}"
      },
      {
         "v1Compatibility": "{\"size\":19387392}"
      }
   ],
   "signatures": [
      {
         "header": {
            "jwk": {
               "crv": "P-256",
               "kid": "5HTY:A24B:L6PG:TQ3G:GMAK:QGKZ:ICD4:S7ZJ:P5JX:UTMP:XZLK:ZXVH",
               "kty": "EC",
               "x": "j5YnDSyrVIt3NquUKvcZIpbfeD8HLZ7BVBFL4WutRBM",
               "y": "PBgFAZ3nNakYN3H9enhrdUrQ_HPYzb8oX5rtJxJo1Y8"
            },
            "alg": "ES256"
         },
         "signature": "1rXiEmWnf9eL7m7Wy3K4l25-Zv2XXl5GgqhM_yjT0ujPmTn0uwfHcCWlweHa9gput3sECj507eQyGpBOF5rD6Q",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjQ4NSwiZm9ybWF0VGFpbCI6IkNuMCIsInRpbWUiOiIyMDE2LTA3LTI2VDExOjQ2OjQ2WiJ9"
      }
   ]
}`

// GetFakeImageGetHandler returns a reaction function for use with wake os client returning one of given image
// objects if found.
func GetFakeImageGetHandler(t *testing.T, iss ...imageapi.Image) ktestclient.ReactionFunc {
	return func(action ktestclient.Action) (handled bool, ret runtime.Object, err error) {
		switch a := action.(type) {
		case ktestclient.GetAction:
			for _, is := range iss {
				if a.GetName() == is.Name {
					t.Logf("images get handler: returning image %s", is.Name)
					return true, &is, nil
				}
			}

			err := kerrors.NewNotFound(kapi.Resource("images"), a.GetName())
			t.Logf("image get handler: %v", err)
			return true, nil, err
		}
		return false, nil, nil
	}
}

// TestNewImageStreamObject returns a new image stream object filled with given values.
func TestNewImageStreamObject(namespace, name, tag, imageName, dockerImageReference string) *imageapi.ImageStream {
	return &imageapi.ImageStream{
		ObjectMeta: kapi.ObjectMeta{
			Namespace: namespace,
			Name:      name,
		},
		Status: imageapi.ImageStreamStatus{
			Tags: map[string]imageapi.TagEventList{
				tag: {
					Items: []imageapi.TagEvent{
						{
							Image:                imageName,
							DockerImageReference: dockerImageReference,
						},
					},
				},
			},
		},
	}
}

// GetFakeImageStreamGetHandler creates a test handler to be used as a reactor with  ktestclient.Fake client
// that handles Get request on image stream resource. Matching is from given image stream list will be
// returned if found. Additionally, a shared image stream may be requested.
func GetFakeImageStreamGetHandler(t *testing.T, iss ...imageapi.ImageStream) ktestclient.ReactionFunc {
	return func(action ktestclient.Action) (handled bool, ret runtime.Object, err error) {
		switch a := action.(type) {
		case ktestclient.GetAction:
			for _, is := range iss {
				if is.Namespace == a.GetNamespace() && a.GetName() == is.Name {
					t.Logf("imagestream get handler: returning image stream %s/%s", is.Namespace, is.Name)
					return true, &is, nil
				}
			}

			err := kerrors.NewNotFound(kapi.Resource("imageStreams"), a.GetName())
			t.Logf("imagestream get handler: %v", err)
			return true, nil, err
		}
		return false, nil, nil
	}
}
