/*
Copyright 2017 The Kubernetes Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package util

import (
	"os"
	"testing"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	utiltesting "k8s.io/client-go/util/testing"
	"k8s.io/kubernetes/pkg/api/v1"
	"k8s.io/kubernetes/pkg/api/v1/helper"
	"k8s.io/kubernetes/pkg/util/mount"
)

var nodeLabels map[string]string = map[string]string{
	"test-key1": "test-value1",
	"test-key2": "test-value2",
}

func TestCheckNodeAffinity(t *testing.T) {
	type affinityTest struct {
		name          string
		expectSuccess bool
		pv            *v1.PersistentVolume
	}

	cases := []affinityTest{
		{
			name:          "valid-no-constraints",
			expectSuccess: true,
			pv:            testVolumeWithNodeAffinity(t, &v1.NodeAffinity{}),
		},
		{
			name:          "valid-constraints",
			expectSuccess: true,
			pv: testVolumeWithNodeAffinity(t, &v1.NodeAffinity{
				RequiredDuringSchedulingIgnoredDuringExecution: &v1.NodeSelector{
					NodeSelectorTerms: []v1.NodeSelectorTerm{
						{
							MatchExpressions: []v1.NodeSelectorRequirement{
								{
									Key:      "test-key1",
									Operator: v1.NodeSelectorOpIn,
									Values:   []string{"test-value1", "test-value3"},
								},
								{
									Key:      "test-key2",
									Operator: v1.NodeSelectorOpIn,
									Values:   []string{"test-value0", "test-value2"},
								},
							},
						},
					},
				},
			}),
		},
		{
			name:          "invalid-key",
			expectSuccess: false,
			pv: testVolumeWithNodeAffinity(t, &v1.NodeAffinity{
				RequiredDuringSchedulingIgnoredDuringExecution: &v1.NodeSelector{
					NodeSelectorTerms: []v1.NodeSelectorTerm{
						{
							MatchExpressions: []v1.NodeSelectorRequirement{
								{
									Key:      "test-key1",
									Operator: v1.NodeSelectorOpIn,
									Values:   []string{"test-value1", "test-value3"},
								},
								{
									Key:      "test-key3",
									Operator: v1.NodeSelectorOpIn,
									Values:   []string{"test-value0", "test-value2"},
								},
							},
						},
					},
				},
			}),
		},
		{
			name:          "invalid-values",
			expectSuccess: false,
			pv: testVolumeWithNodeAffinity(t, &v1.NodeAffinity{
				RequiredDuringSchedulingIgnoredDuringExecution: &v1.NodeSelector{
					NodeSelectorTerms: []v1.NodeSelectorTerm{
						{
							MatchExpressions: []v1.NodeSelectorRequirement{
								{
									Key:      "test-key1",
									Operator: v1.NodeSelectorOpIn,
									Values:   []string{"test-value3", "test-value4"},
								},
								{
									Key:      "test-key2",
									Operator: v1.NodeSelectorOpIn,
									Values:   []string{"test-value0", "test-value2"},
								},
							},
						},
					},
				},
			}),
		},
	}

	for _, c := range cases {
		err := CheckNodeAffinity(c.pv, nodeLabels)

		if err != nil && c.expectSuccess {
			t.Errorf("CheckTopology %v returned error: %v", c.name, err)
		}
		if err == nil && !c.expectSuccess {
			t.Errorf("CheckTopology %v returned success, expected error", c.name)
		}
	}
}

func testVolumeWithNodeAffinity(t *testing.T, affinity *v1.NodeAffinity) *v1.PersistentVolume {
	objMeta := metav1.ObjectMeta{Name: "test-constraints"}
	objMeta.Annotations = map[string]string{}
	err := helper.StorageNodeAffinityToAlphaAnnotation(objMeta.Annotations, affinity)
	if err != nil {
		t.Fatalf("Failed to get node affinity annotation: %v", err)
	}

	return &v1.PersistentVolume{
		ObjectMeta: objMeta,
	}
}

func TestDoUnmountMountPoint(t *testing.T) {

	tmpDir1, err1 := utiltesting.MkTmpdir("umount_test1")
	if err1 != nil {
		t.Fatalf("error creating temp dir: %v", err1)
	}
	defer os.RemoveAll(tmpDir1)

	tmpDir2, err2 := utiltesting.MkTmpdir("umount_test2")
	if err2 != nil {
		t.Fatalf("error creating temp dir: %v", err2)
	}
	defer os.RemoveAll(tmpDir2)

	// Second part: want no error
	tests := []struct {
		mountPath    string
		corruptedMnt bool
	}{
		{
			mountPath:    tmpDir1,
			corruptedMnt: true,
		},
		{
			mountPath:    tmpDir2,
			corruptedMnt: false,
		},
	}

	fake := &mount.FakeMounter{}

	for _, tt := range tests {
		err := doUnmountMountPoint(tt.mountPath, fake, false, tt.corruptedMnt)
		if err != nil {
			t.Errorf("err Expected nil, but got: %v", err)
		}
	}
}
