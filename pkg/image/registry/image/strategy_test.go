package image

import (
	"math/rand"
	"reflect"
	"testing"

	"github.com/google/gofuzz"

	kapi "k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/api/meta"
	apitesting "k8s.io/kubernetes/pkg/api/testing"
	"k8s.io/kubernetes/pkg/util/diff"

	"github.com/openshift/origin/pkg/api/v1"
	"github.com/openshift/origin/pkg/image/api"
)

func fuzzImage(t *testing.T, image *api.Image, seed int64) *api.Image {
	f := apitesting.FuzzerFor(t, v1.SchemeGroupVersion, rand.NewSource(seed))
	f.Funcs(
		func(j *api.Image, c fuzz.Continue) {
			c.FuzzNoCustom(j)
			j.Annotations = make(map[string]string)
			j.Labels = make(map[string]string)
			j.Signatures = make([]api.ImageSignature, c.Rand.Intn(3)+2)
			for i := range j.Signatures {
				sign := &j.Signatures[i]
				c.Fuzz(sign)
				sign.Conditions = make([]api.SignatureCondition, c.Rand.Intn(3)+2)
				for ci := range sign.Conditions {
					cond := &sign.Conditions[ci]
					c.Fuzz(cond)
				}
			}
			for i := 0; i < c.Rand.Intn(3)+2; i++ {
				j.Labels[c.RandString()] = c.RandString()
				j.Annotations[c.RandString()] = c.RandString()
			}
		},
	)

	updated := api.Image{}
	f.Fuzz(&updated)
	updated.Namespace = image.Namespace
	updated.Name = image.Name

	j, err := meta.TypeAccessor(image)
	if err != nil {
		t.Fatalf("Unexpected error %v for %#v", err, image)
	}
	j.SetKind("")
	j.SetAPIVersion("")

	return &updated
}

func TestStrategyPrepareForCreate(t *testing.T) {
	ctx := kapi.NewDefaultContext()

	original := api.Image{
		ObjectMeta: kapi.ObjectMeta{
			Name: "image",
		},
	}

	seed := int64(2703387474910584091) //rand.Int63()
	fuzzed := fuzzImage(t, &original, seed)
	obj, err := kapi.Scheme.DeepCopy(fuzzed)
	if err != nil {
		t.Fatalf("faild to deep copy fuzzed image: %v", err)
	}
	image := obj.(*api.Image)

	if len(image.Signatures) == 0 {
		t.Fatalf("fuzzifier failed to generate signatures")
	}

	Strategy.PrepareForCreate(ctx, image)

	testVerifySignatures(t, fuzzed, image)
}

func testVerifySignatures(t *testing.T, orig, new *api.Image) {
	if len(new.Signatures) != len(orig.Signatures) {
		t.Errorf("unexpected number of signatures: %d != %d", len(new.Signatures), len(orig.Signatures))
	}

	for i, sig := range new.Signatures {
		// expect annotations to be cleared
		delete(orig.Signatures[i].Annotations, managedSignatureAnnotation)

		vi := reflect.ValueOf(&sig).Elem()
		vf := reflect.ValueOf(&orig.Signatures[i]).Elem()
		typeOfT := vf.Type()

		for j := 0; j < vf.NumField(); j++ {
			iField := vi.Field(j)
			fField := vf.Field(j)
			typeOfF := fField.Type()

			switch typeOfT.Field(j).Name {
			case "Content", "Type", "TypeMeta", "ObjectMeta":
				if !reflect.DeepEqual(iField.Interface(), fField.Interface()) {
					t.Errorf("%s field should not differ: %s", typeOfT.Field(j).Name, diff.ObjectGoPrintDiff(iField.Interface(), fField.Interface()))
				}

			default:
				if !reflect.DeepEqual(iField.Interface(), reflect.Zero(typeOfF).Interface()) {
					t.Errorf("expected Signatures.%s to be unset, not %#+v", typeOfF.Field(j).Name, iField.Interface())
				}
			}
		}
	}
}

func TestStrategyPrepareForCreateSignature(t *testing.T) {
	ctx := kapi.NewDefaultContext()

	original := api.Image{
		ObjectMeta: kapi.ObjectMeta{
			Name: "image",
		},
	}

	seed := int64(2703387474910584091) //rand.Int63()
	fuzzed := fuzzImage(t, &original, seed)

	if len(fuzzed.Signatures) == 0 {
		t.Fatalf("fuzzifier failed to generate signatures")
	}

	for _, tc := range []struct {
		name        string
		annotations map[string]string
		expected    map[string]string
	}{
		{
			name:        "unset annotations",
			annotations: nil,
			expected:    nil,
		},
		{
			name:        "empty annotations",
			annotations: map[string]string{},
			expected:    map[string]string{},
		},
		{
			name:        "managed annotation shall be removed",
			annotations: map[string]string{managedSignatureAnnotation: "value"},
			expected:    map[string]string{},
		},
		{
			name:        "other annotations shall stay",
			annotations: map[string]string{"key": "value"},
			expected:    map[string]string{"key": "value"},
		},
		{
			name:        "remove and keep",
			annotations: map[string]string{"key": "value", managedSignatureAnnotation: "true"},
			expected:    map[string]string{"key": "value"},
		},
	} {
		t.Run(tc.name, func(t *testing.T) {
			fuzzed.Signatures[0].Annotations = tc.annotations
			obj, err := kapi.Scheme.DeepCopy(fuzzed)
			if err != nil {
				t.Fatalf("failed to copy image: %v", err)
			}
			image := obj.(*api.Image)

			Strategy.PrepareForCreate(ctx, image)

			testVerifySignatures(t, fuzzed, image)

			if !reflect.DeepEqual(image.Signatures[0].Annotations, tc.expected) {
				t.Errorf("unexpected signature annotations: %s", diff.ObjectGoPrintDiff(image.Annotations, tc.expected))
			}
		})
	}
}
