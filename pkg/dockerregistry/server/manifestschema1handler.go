package server

import (
	"encoding/json"

	"github.com/docker/distribution/manifest/schema1"
	"github.com/docker/libtrust"
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

func (h *manifestSchema1Handler) Manifest() *schema1.SignedManifest {
	return h.manifest
}

func (h *manifestSchema1Handler) Payload() (payload []byte, canonical []byte, err error) {
	canonical, err = h.manifest.Payload()
	return h.manifest.Raw, canonical, err
}
