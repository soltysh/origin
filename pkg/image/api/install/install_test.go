package install

import (
	"encoding/json"
	"testing"

	kapi "k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/api/latest"
	"k8s.io/kubernetes/pkg/api/unversioned"

	"github.com/openshift/origin/pkg/image/api"
)

func TestResourceVersioner(t *testing.T) {
	image := api.ImageStream{ObjectMeta: kapi.ObjectMeta{ResourceVersion: "10"}}
	version, err := accessor.ResourceVersion(&image)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if version != "10" {
		t.Errorf("unexpected version %v", version)
	}

	imageList := api.ImageStreamList{ListMeta: unversioned.ListMeta{ResourceVersion: "10"}}
	version, err = accessor.ResourceVersion(&imageList)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if version != "10" {
		t.Errorf("unexpected version %v", version)
	}
}

func TestCodec(t *testing.T) {
	image := api.ImageStream{}
	// We do want to use package latest rather than testapi here, because we
	// want to test if the package install and package latest work as expected.
	data, err := latest.GroupOrDie("").Codec.Encode(&image)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	other := api.ImageStream{}
	if err := json.Unmarshal(data, &other); err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if other.APIVersion != latest.GroupOrDie("").GroupVersion.Version || other.Kind != "ImageStream" {
		t.Errorf("unexpected unmarshalled object %#v", other)
	}
}

func TestInterfacesFor(t *testing.T) {
	if _, err := latest.GroupOrDie("").InterfacesFor(api.SchemeGroupVersion); err == nil {
		t.Fatalf("unexpected non-error: %v", err)
	}
	for i, version := range latest.GroupOrDie("").GroupVersions {
		if vi, err := latest.GroupOrDie("").InterfacesFor(version); err != nil || vi == nil {
			t.Fatalf("%d: unexpected result: %v", i, err)
		}
	}
}

func TestRESTMapper(t *testing.T) {
	gv := unversioned.GroupVersion{Group: "", Version: "v1"}
	imageGVK := gv.WithKind("ImageStream")

	if gvk, err := latest.GroupOrDie("").RESTMapper.KindFor("imagestreams"); err != nil || gvk != imageGVK {
		t.Errorf("unexpected version mapping: %v %v", gvk, err)
	}

	if m, err := latest.GroupOrDie("").RESTMapper.RESTMapping(imageGVK.GroupKind(), ""); err != nil || m.GroupVersionKind != imageGVK || m.Resource != "imagestreams" {
		t.Errorf("unexpected version mapping: %#v %v", m, err)
	}

	for _, version := range latest.GroupOrDie("").GroupVersions {
		mapping, err := latest.GroupOrDie("").RESTMapper.RESTMapping(imageGVK.GroupKind(), version.Version)
		if err != nil {
			t.Errorf("unexpected error: %v", err)
		}

		if mapping.Resource != "imagestreams" {
			t.Errorf("incorrect resource name: %#v", mapping)
		}
		if mapping.GroupVersionKind.GroupVersion() != version {
			t.Errorf("incorrect version: %v", mapping)
		}

		interfaces, _ := latest.GroupOrDie("").InterfacesFor(version)
		if mapping.Codec != interfaces.Codec {
			t.Errorf("unexpected codec: %#v, expected: %#v", mapping, interfaces)
		}

		image := &api.ImageStream{ObjectMeta: kapi.ObjectMeta{Name: "foo"}}
		name, err := mapping.MetadataAccessor.Name(image)
		if err != nil {
			t.Errorf("unexpected error: %v", err)
		}
		if name != "foo" {
			t.Errorf("unable to retrieve object meta with: %v", mapping.MetadataAccessor)
		}
	}
}
