package server

import (
	"encoding/json"

	"github.com/docker/distribution/context"
	"github.com/docker/distribution/manifest/schema1"
	"github.com/docker/libtrust"

	"k8s.io/kubernetes/pkg/util/sets"

	imageapi "github.com/openshift/origin/pkg/image/api"
)

func unmarshalManifestSchema1(content []byte, signatures [][]byte) (*schema1.SignedManifest, error) {
	// prefer signatures from the manifest
	if _, err := libtrust.ParsePrettySignature(content, "signatures"); err == nil {
		sm := schema1.SignedManifest{Raw: content}
		if err = json.Unmarshal(content, &sm); err == nil {
			return &sm, nil
		}
	}

	jsig, err := libtrust.NewJSONSignature(content, signatures...)
	if err != nil {
		return nil, err
	}

	// Extract the pretty JWS
	content, err = jsig.PrettySignature("signatures")
	if err != nil {
		return nil, err
	}

	var sm schema1.SignedManifest
	if err = json.Unmarshal(content, &sm); err != nil {
		return nil, err
	}
	return &sm, err
}

type manifestSchema1Handler struct {
	repo     *repository
	manifest *schema1.SignedManifest
}

var _ ManifestHandler = &manifestSchema1Handler{}

func (h *manifestSchema1Handler) FillImageMetadata(ctx context.Context, image *imageapi.Image) error {
	if err := imageapi.ImageWithMetadata(image); err != nil {
		return err
	}

	layers := h.manifest.FSLayers

	blobSet := sets.NewString()
	image.DockerImageMetadata.Size = int64(0)

	blobs := h.repo.Blobs(ctx)
	for i := range image.DockerImageLayers {
		layer := &image.DockerImageLayers[i]
		// DockerImageLayers represents h.manifest.Manifest.FSLayers in reversed order
		desc, err := blobs.Stat(ctx, layers[len(image.DockerImageLayers)-i-1].BlobSum)
		if err != nil {
			context.GetLogger(ctx).Errorf("failed to stat blob %s of image %s", layer.Name, image.DockerImageReference)
			return err
		}
		layer.Size = desc.Size
		// count empty layer just once (empty layer may actually have non-zero size)
		if !blobSet.Has(layer.Name) {
			image.DockerImageMetadata.Size += desc.Size
			blobSet.Insert(layer.Name)
		}
	}

	context.GetLogger(ctx).Infof("total size of image %s with docker ref %s: %d", image.Name, image.DockerImageReference, image.DockerImageMetadata.Size)

	return nil
}

func (h *manifestSchema1Handler) Manifest() *schema1.SignedManifest {
	return h.manifest
}

func (h *manifestSchema1Handler) Payload() (payload []byte, canonical []byte, err error) {
	canonical, err = h.manifest.Payload()
	return h.manifest.Raw, canonical, err
}
