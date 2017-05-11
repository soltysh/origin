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

package populator

import (
	"testing"
	"time"

	"k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/fake"
	"k8s.io/kubernetes/pkg/client/testing/core"
	"k8s.io/kubernetes/pkg/controller/informers"
	"k8s.io/kubernetes/pkg/controller/volume/attachdetach/cache"
	"k8s.io/kubernetes/pkg/runtime"
	"k8s.io/kubernetes/pkg/types"
	volumetesting "k8s.io/kubernetes/pkg/volume/testing"
	"k8s.io/kubernetes/pkg/volume/util/volumehelper"
	"k8s.io/kubernetes/pkg/watch"
)

func TestFindAndAddActivePods_FindAndRemoveDeletedPods(t *testing.T) {
	pod := api.Pod{
		ObjectMeta: api.ObjectMeta{
			Name:      "dswp-test-pod",
			UID:       "dswp-test-pod-uid",
			Namespace: "dswp-test",
		},
		Spec: api.PodSpec{
			NodeName: "dswp-test-host",
			Volumes: []api.Volume{
				{
					Name: "dswp-test-volume-name",
					VolumeSource: api.VolumeSource{
						GCEPersistentDisk: &api.GCEPersistentDiskVolumeSource{
							PDName: "dswp-test-fake-device",
						},
					},
				},
			},
		},
		Status: api.PodStatus{
			Phase: api.PodPhase("Running"),
		},
	}

	fakeVolumePluginMgr, _ := volumetesting.GetTestVolumePluginMgr(t)
	fakeKubeClient := &fake.Clientset{}
	fakeKubeClient.AddReactor("list", "pods", func(action core.Action) (handled bool, ret runtime.Object, err error) {
		obj := &api.PodList{}
		obj.Items = append(obj.Items, pod)
		return true, obj, nil
	})
	fakeWatch := watch.NewFake()
	fakeKubeClient.AddWatchReactor("pods", core.DefaultWatchReactor(fakeWatch, nil))

	resyncPeriod := 5 * time.Minute
	podInformer := informers.NewPodInformer(fakeKubeClient, resyncPeriod)
	pvcInformer := informers.NewPVCInformer(fakeKubeClient, resyncPeriod)
	pvInformer := informers.NewPVInformer(fakeKubeClient, resyncPeriod)
	var stopCh <-chan struct{}
	go podInformer.Run(stopCh)
	go pvcInformer.Run(stopCh)
	go pvInformer.Run(stopCh)
	for !podInformer.HasSynced() {
		time.Sleep(10 * time.Millisecond)
	}

	fakesDSW := cache.NewDesiredStateOfWorld(fakeVolumePluginMgr)

	podName := volumehelper.GetUniquePodName(&pod)

	generatedVolumeName := "fake-plugin/" + pod.Spec.Volumes[0].Name

	dswp := &desiredStateOfWorldPopulator{
		loopSleepDuration:     100 * time.Millisecond,
		listPodsRetryDuration: 3 * time.Second,
		desiredStateOfWorld:   fakesDSW,
		volumePluginMgr:       fakeVolumePluginMgr,
		podInformer:           podInformer,
		pvcInformer:           pvcInformer,
		pvInformer:            pvInformer,
	}

	//add the given node to the list of nodes managed by dsw
	dswp.desiredStateOfWorld.AddNode(types.NodeName(pod.Spec.NodeName), false /*keepTerminatedPodVolumes*/)

	dswp.findAndAddActivePods()

	expectedVolumeName := api.UniqueVolumeName(generatedVolumeName)

	//check if the given volume referenced by the pod is added to dsw
	volumeExists := dswp.desiredStateOfWorld.VolumeExists(expectedVolumeName, types.NodeName(pod.Spec.NodeName))
	if !volumeExists {
		t.Fatalf(
			"VolumeExists(%q) failed. Expected: <true> Actual: <%v>",
			expectedVolumeName,
			volumeExists)
	}

	//delete the pod and volume manually
	dswp.desiredStateOfWorld.DeletePod(podName, expectedVolumeName, types.NodeName(pod.Spec.NodeName))

	//check if the given volume referenced by the pod still exists in dsw
	volumeExists = dswp.desiredStateOfWorld.VolumeExists(expectedVolumeName, types.NodeName(pod.Spec.NodeName))
	if volumeExists {
		t.Fatalf(
			"VolumeExists(%q) failed. Expected: <false> Actual: <%v>",
			expectedVolumeName,
			volumeExists)
	}

	// add pod and volume again
	dswp.findAndAddActivePods()

	//check if the given volume referenced by the pod is added to dsw for the second time
	volumeExists = dswp.desiredStateOfWorld.VolumeExists(expectedVolumeName, types.NodeName(pod.Spec.NodeName))
	if !volumeExists {
		t.Fatalf(
			"VolumeExists(%q) failed. Expected: <true> Actual: <%v>",
			expectedVolumeName,
			volumeExists)
	}

	// delete the pod
	fakeWatch.Delete(&pod)
	for len(podInformer.GetStore().List()) > 0 {
		time.Sleep(10 * time.Millisecond)
	}

	dswp.findAndRemoveDeletedPods()
	//check if the given volume referenced by the pod still exists in dsw
	volumeExists = dswp.desiredStateOfWorld.VolumeExists(expectedVolumeName, types.NodeName(pod.Spec.NodeName))
	if volumeExists {
		t.Fatalf(
			"VolumeExists(%q) failed. Expected: <false> Actual: <%v>",
			expectedVolumeName,
			volumeExists)
	}

}
