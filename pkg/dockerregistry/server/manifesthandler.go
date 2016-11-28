package server

import (
	"github.com/docker/distribution/context"
	"github.com/docker/distribution/digest"
	"github.com/docker/distribution/manifest/schema1"

	imageapi "github.com/openshift/origin/pkg/image/api"
)

// A ManifestHandler defines a common set of operations on all versions of manifest schema.
type ManifestHandler interface {
	// Manifest returns a deserialized manifest object.
	Manifest() *schema1.SignedManifest

	// Payload returns manifest's media type, complete payload with signatures and canonical payload without
	// signatures or an error if the information could not be fetched.
	Payload() (payload []byte, canonical []byte, err error)

	// Verify returns an error if the contained manifest is not valid or has missing dependencies.
	Verify(ctx context.Context, skipDependencyVerification bool) error
}

// NewManifestHandler creates a manifest handler for the given manifest.
func NewManifestHandler(repo *repository, manifest *schema1.SignedManifest) (ManifestHandler, error) {
	return &manifestSchema1Handler{repo: repo, manifest: manifest}, nil
}

// NewManifestHandlerFromImage creates a new manifest handler for a manifest stored in the given image.
func NewManifestHandlerFromImage(repo *repository, image *imageapi.Image) (ManifestHandler, error) {
	// Fetch the signatures for the manifest
	signatures, err := repo.Signatures().Get(digest.Digest(image.Name))
	if err != nil {
		if image.Annotations[imageapi.ManagedByOpenShiftAnnotation] == "true" {
			context.GetLogger(repo.ctx).Errorf("failed to get signatures from storage for managed image %q: %v", image.Name, err)
		}
	}

	manifest, err := unmarshalManifestSchema1([]byte(image.DockerImageManifest), signatures)
	if err != nil {
		return nil, err
	}

	return NewManifestHandler(repo, manifest)
}
