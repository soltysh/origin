package admission

import (
	"testing"

	kapi "k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/runtime"
)

func newPod() *kapi.Pod {
	return &kapi.Pod{
		ObjectMeta: kapi.ObjectMeta{
			Annotations:     map[string]string{},
			Name:            "foo",
			OwnerReferences: []kapi.OwnerReference{},
		},
	}

}

func TestIsOnlyMutatingGCFields(t *testing.T) {
	tests := []struct {
		name     string
		obj      func() runtime.Object
		old      func() runtime.Object
		expected bool
	}{
		{
			name: "same",
			obj: func() runtime.Object {
				return newPod()
			},
			old: func() runtime.Object {
				return newPod()
			},
			expected: true,
		},
		{
			name: "only annotations",
			obj: func() runtime.Object {
				obj := newPod()
				obj.Annotations["foo"] = "bar"
				return obj
			},
			old: func() runtime.Object {
				return newPod()
			},
			expected: false,
		},
		{
			name: "only other",
			obj: func() runtime.Object {
				obj := newPod()
				obj.Spec.RestartPolicy = kapi.RestartPolicyAlways
				return obj
			},
			old: func() runtime.Object {
				return newPod()
			},
			expected: false,
		},
		{
			name: "only ownerRef",
			obj: func() runtime.Object {
				obj := newPod()
				obj.OwnerReferences = append(obj.OwnerReferences, kapi.OwnerReference{Name: "foo"})
				return obj
			},
			old: func() runtime.Object {
				return newPod()
			},
			expected: true,
		},
		{
			name: "ownerRef and finalizer",
			obj: func() runtime.Object {
				obj := newPod()
				obj.OwnerReferences = append(obj.OwnerReferences, kapi.OwnerReference{Name: "foo"})
				obj.Finalizers = []string{"final"}
				return obj
			},
			old: func() runtime.Object {
				return newPod()
			},
			expected: true,
		},
		{
			name: "and annotations",
			obj: func() runtime.Object {
				obj := newPod()
				obj.OwnerReferences = append(obj.OwnerReferences, kapi.OwnerReference{Name: "foo"})
				obj.Annotations["foo"] = "bar"
				return obj
			},
			old: func() runtime.Object {
				return newPod()
			},
			expected: false,
		},
		{
			name: "and other",
			obj: func() runtime.Object {
				obj := newPod()
				obj.OwnerReferences = append(obj.OwnerReferences, kapi.OwnerReference{Name: "foo"})
				obj.Spec.RestartPolicy = kapi.RestartPolicyAlways
				return obj
			},
			old: func() runtime.Object {
				return newPod()
			},
			expected: false,
		},
	}

	for _, tc := range tests {
		actual := IsOnlyMutatingGCFields(tc.obj(), tc.old())
		if tc.expected != actual {
			t.Errorf("%s: expected %v, got %v", tc.name, tc.expected, actual)
		}
	}
}
