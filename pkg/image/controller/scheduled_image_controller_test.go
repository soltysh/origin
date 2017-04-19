package controller

import (
	"sync"
	"testing"
	"time"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	kapi "k8s.io/kubernetes/pkg/api"
	kexternalfake "k8s.io/kubernetes/pkg/client/clientset_generated/clientset/fake"
	kinternalfake "k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/fake"
	kexternalinformers "k8s.io/kubernetes/pkg/client/informers/informers_generated/externalversions"
	kinternalinformers "k8s.io/kubernetes/pkg/client/informers/informers_generated/internalversion"

	"github.com/openshift/origin/pkg/client/testclient"
	"github.com/openshift/origin/pkg/controller/shared"
	"github.com/openshift/origin/pkg/image/api"

	_ "github.com/openshift/origin/pkg/api/install"
)

func TestScheduledImport(t *testing.T) {
	one := int64(1)
	stream := &api.ImageStream{
		ObjectMeta: metav1.ObjectMeta{
			Name: "test", Namespace: "other", UID: "1", ResourceVersion: "1",
			Annotations: map[string]string{api.DockerImageRepositoryCheckAnnotation: "done"},
			Generation:  1,
		},
		Spec: api.ImageStreamSpec{
			Tags: map[string]api.TagReference{
				"default": {
					From:         &kapi.ObjectReference{Kind: "DockerImage", Name: "mysql:latest"},
					Generation:   &one,
					ImportPolicy: api.TagImportPolicy{Scheduled: true},
				},
			},
		},
		Status: api.ImageStreamStatus{
			Tags: map[string]api.TagEventList{
				"default": {Items: []api.TagEvent{{Generation: 1}}},
			},
		},
	}

	internalKubeClient := kinternalfake.NewSimpleClientset()
	externalKubeClient := kexternalfake.NewSimpleClientset()
	externalKubeInformerFactory := kexternalinformers.NewSharedInformerFactory(externalKubeClient, 10*time.Minute)
	internalKubeInformerFactory := kinternalinformers.NewSharedInformerFactory(internalKubeClient, 10*time.Minute)
	informerFactory := shared.NewInformerFactory(internalKubeInformerFactory, externalKubeInformerFactory,
		internalKubeClient, testclient.NewSimpleFake(), shared.DefaultListerWatcherOverrides{}, 10*time.Minute)
	isInformer := informerFactory.ImageStreams()
	fake := testclient.NewSimpleFake()
	sched := newScheduledImageStreamController(isInformer, fake, nil, 1*time.Second, true)

	// queue, but don't import the stream
	sched.enqueueImageStream(stream)
	if sched.scheduler.Len() != 1 {
		t.Fatalf("should have scheduled: %#v", sched.scheduler)
	}
	if len(fake.Actions()) != 0 {
		t.Fatalf("should have made no calls: %#v", fake)
	}

	// encountering a not found error for image streams should drop the stream
	sched.scheduler.RunOnce() // we need to run it twice since we have 2 buckets
	sched.scheduler.RunOnce()
	if sched.scheduler.Len() != 0 {
		t.Fatalf("should have removed item in scheduler: %#v", sched.scheduler)
	}
	if len(fake.Actions()) != 0 {
		t.Fatalf("invalid actions: %#v", fake.Actions())
	}

	// queue back
	sched.enqueueImageStream(stream)
	// and add to informer
	isInformer.Informer().GetIndexer().Add(stream)

	// run a background import
	sched.scheduler.RunOnce() // we need to run it twice since we have 2 buckets
	sched.scheduler.RunOnce()
	if sched.scheduler.Len() != 1 {
		t.Fatalf("should have left item in scheduler: %#v", sched.scheduler)
	}
	if len(fake.Actions()) != 1 || !fake.Actions()[0].Matches("create", "imagestreamimports") {
		t.Fatalf("invalid actions: %#v", fake.Actions())
	}

	var key, value interface{}
	for k, v := range sched.scheduler.Map() {
		key, value = k, v
		break
	}

	var wg sync.WaitGroup

	// re-queue the stream with a new resource version
	stream.ResourceVersion = "2"
	wg.Add(1)
	go func(wg *sync.WaitGroup) {
		sched.enqueueImageStream(stream)
		if sched.scheduler.Len() != 1 {
			t.Fatalf("should have scheduled: %#v", sched.scheduler)
		}
		wg.Done()
	}(&wg)
	// simulate a race where another caller attempts to dequeue the item
	wg.Add(1)
	go func(wg *sync.WaitGroup) {
		if sched.scheduler.Remove(key, value) {
			t.Fatalf("should not have removed %s: %#v", key, sched.scheduler)
		}
		if sched.scheduler.Len() != 1 {
			t.Fatalf("should have left scheduled: %#v", sched.scheduler)
		}
		wg.Done()
	}(&wg)
	wg.Wait()
	if sched.scheduler.Len() != 1 {
		t.Fatalf("should have been left scheduled: %#v", sched.scheduler)
	}

	// disabling the scheduled import should drop the stream
	sched.enabled = false
	fake.ClearActions()

	sched.scheduler.RunOnce() // we need to run it twice since we have 2 buckets
	sched.scheduler.RunOnce()
	if sched.scheduler.Len() != 0 {
		t.Fatalf("should have removed item from scheduler: %#v", sched.scheduler)
	}
	if len(fake.Actions()) != 0 {
		t.Fatalf("invalid actions: %#v", fake.Actions())
	}

	// queuing when disabled should not add the stream
	sched.enqueueImageStream(stream)
	if sched.scheduler.Len() != 0 {
		t.Fatalf("should have not added item to scheduler: %#v", sched.scheduler)
	}
}
