package etcd

import (
	"fmt"
	"testing"
	"time"

	kapi "k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/api/errors"
	klatest "k8s.io/kubernetes/pkg/api/latest"
	"k8s.io/kubernetes/pkg/api/unversioned"
	"k8s.io/kubernetes/pkg/fields"
	"k8s.io/kubernetes/pkg/labels"
	"k8s.io/kubernetes/pkg/registry/registrytest"
	"k8s.io/kubernetes/pkg/runtime"
	etcdstorage "k8s.io/kubernetes/pkg/storage/etcd"
	"k8s.io/kubernetes/pkg/storage/etcd/etcdtest"
	etcdtesting "k8s.io/kubernetes/pkg/storage/etcd/testing"
	"k8s.io/kubernetes/pkg/watch"

	"github.com/openshift/origin/pkg/image/api"
	// Ensure the APIs are initilized.
	_ "github.com/openshift/origin/pkg/image/api/docker10"
	_ "github.com/openshift/origin/pkg/image/api/dockerpre012"
	_ "github.com/openshift/origin/pkg/image/api/install"
	_ "github.com/openshift/origin/pkg/image/api/v1"
	_ "github.com/openshift/origin/pkg/image/api/v1beta3"
	"github.com/openshift/origin/pkg/image/registry/image"
)

func newStorage(t *testing.T) (*REST, *etcdtesting.EtcdTestServer) {
	server := etcdtesting.NewEtcdTestClientServer(t)
	etcdStorage := etcdstorage.NewEtcdStorage(server.Client, klatest.GroupOrDie("").Codec, etcdtest.PathPrefix())
	imageStorage := NewREST(etcdStorage)
	return imageStorage, server
}

func TestStorage(t *testing.T) {
	storage, _ := newStorage(t)
	image.NewRegistry(storage)
}

func validImage() *api.Image {
	return &api.Image{
		ObjectMeta: kapi.ObjectMeta{
			Name:         "foo",
			GenerateName: "foo",
		},
		DockerImageReference: "openshift/origin",
	}
}

func TestCreate(t *testing.T) {
	storage, server := newStorage(t)
	defer server.Terminate(t)
	test := registrytest.New(t, storage.Etcd).ClusterScope()
	test.TestCreate(
		validImage(),
		// invalid
		&api.Image{},
	)
}

func TestList(t *testing.T) {
	storage, server := newStorage(t)
	defer server.Terminate(t)
	test := registrytest.New(t, storage.Etcd).ClusterScope()
	test.TestList(
		validImage(),
	)
}

func TestGet(t *testing.T) {
	storage, server := newStorage(t)
	defer server.Terminate(t)
	test := registrytest.New(t, storage.Etcd).ClusterScope()
	test.TestGet(
		validImage(),
	)
}

func TestDelete(t *testing.T) {
	storage, server := newStorage(t)
	defer server.Terminate(t)
	test := registrytest.New(t, storage.Etcd).ClusterScope()
	image := validImage()
	image.ObjectMeta = kapi.ObjectMeta{GenerateName: "foo"}
	test.TestDelete(
		validImage(),
	)
}

func TestWatchErrorFieldSet(t *testing.T) {
	storage, server := newStorage(t)
	defer server.Terminate(t)
	options := &unversioned.ListOptions{
		FieldSelector: unversioned.FieldSelector{fields.SelectorFromSet(fields.Set{"foo": "bar"})},
	}
	_, err := storage.Watch(kapi.NewDefaultContext(), options)
	if err == nil {
		t.Fatal("unexpected nil error")
	}
	if !errors.IsBadRequest(err) || err.Error() != "field selectors are not supported on images" {
		t.Fatalf("unexpected error: %s", err.Error())
	}
}

func TestWatch(t *testing.T) {
	storage, server := newStorage(t)
	defer server.Terminate(t)
	var tests = []struct {
		label    labels.Selector
		images   []*api.Image
		expected []bool
	}{
		{
			labels.Everything(),
			[]*api.Image{
				{ObjectMeta: kapi.ObjectMeta{Name: "a"}, DockerImageMetadata: api.DockerImage{}},
				{ObjectMeta: kapi.ObjectMeta{Name: "b"}, DockerImageMetadata: api.DockerImage{}},
				{ObjectMeta: kapi.ObjectMeta{Name: "c"}, DockerImageMetadata: api.DockerImage{}},
			},
			[]bool{
				true,
				true,
				true,
			},
		},
		{
			labels.Set{"color": "blue"}.AsSelector(),
			[]*api.Image{
				{ObjectMeta: kapi.ObjectMeta{Name: "a", Labels: map[string]string{"color": "blue"}}, DockerImageMetadata: api.DockerImage{}},
				{ObjectMeta: kapi.ObjectMeta{Name: "b", Labels: map[string]string{"color": "green"}}, DockerImageMetadata: api.DockerImage{}},
				{ObjectMeta: kapi.ObjectMeta{Name: "c", Labels: map[string]string{"color": "blue"}}, DockerImageMetadata: api.DockerImage{}},
			},
			[]bool{
				true,
				false,
				true,
			},
		},
	}
	for idx, tt := range tests {
		ctx := kapi.NewDefaultContext()
		options := &unversioned.ListOptions{
			LabelSelector:   unversioned.LabelSelector{tt.label},
			ResourceVersion: "1",
		}
		watching, err := storage.Watch(ctx, options)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}

		for testIndex, image := range tt.images {
			image.Name = fmt.Sprintf("%s%d", image.Name, idx)
			if err := emitObject(storage, ctx, image); err != nil {
				t.Errorf("unexpected error: %v", err)
			}

			select {
			case event, ok := <-watching.ResultChan():
				if !ok {
					t.Errorf("watching channel should be open")
				}
				if !tt.expected[testIndex] {
					t.Errorf("unexpected image returned from watch: %#v", event.Object)
				}
				if e, a := watch.Added, event.Type; e != a {
					t.Errorf("Expected %v, got %v", e, a)
				}
			case <-time.After(50 * time.Millisecond):
				if tt.expected[testIndex] {
					t.Errorf("%d:%d: Expected image %#v to be returned from watch", idx, testIndex, image)
				}
			}
		}
		watching.Stop()
	}
}

func emitObject(storage *REST, ctx kapi.Context, obj runtime.Object) error {
	meta, err := kapi.ObjectMetaFor(obj)
	if err != nil {
		return err
	}
	key, err := storage.KeyFunc(ctx, meta.Name)
	if err != nil {
		return err
	}
	return storage.Storage.Set(ctx, key, obj, nil, 0)
}

// type fakeStrategy struct {
// 	rest.RESTCreateStrategy
// }

// func (fakeStrategy) PrepareForCreate(obj runtime.Object) {
// 	img := obj.(*api.Image)
// 	img.Annotations = make(map[string]string, 1)
// 	img.Annotations["test"] = "PrepareForCreate"
// }

// func TestStrategyPrepareMethods(t *testing.T) {
// 	_, helper := newHelper(t)
// 	storage := NewREST(helper)
// 	img := validImage()
// 	strategy := fakeStrategy{image.Strategy}

// 	storage.store.CreateStrategy = strategy

// 	obj, err := storage.Create(kapi.NewDefaultContext(), img)
// 	if err != nil {
// 		t.Errorf("Unexpected error: %v", err)
// 	}

// 	newImage := obj.(*api.Image)
// 	if newImage.Annotations["test"] != "PrepareForCreate" {
// 		t.Errorf("Expected PrepareForCreate annotation")
// 	}
// }
