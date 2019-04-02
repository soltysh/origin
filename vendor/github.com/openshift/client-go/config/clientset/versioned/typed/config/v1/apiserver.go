// Code generated by client-gen. DO NOT EDIT.

package v1

import (
	"time"

	v1 "github.com/openshift/api/config/v1"
	scheme "github.com/openshift/client-go/config/clientset/versioned/scheme"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	types "k8s.io/apimachinery/pkg/types"
	watch "k8s.io/apimachinery/pkg/watch"
	rest "k8s.io/client-go/rest"
)

// APIServersGetter has a method to return a APIServerInterface.
// A group's client should implement this interface.
type APIServersGetter interface {
	APIServers() APIServerInterface
}

// APIServerInterface has methods to work with APIServer resources.
type APIServerInterface interface {
	Create(*v1.APIServer) (*v1.APIServer, error)
	Update(*v1.APIServer) (*v1.APIServer, error)
	UpdateStatus(*v1.APIServer) (*v1.APIServer, error)
	Delete(name string, options *metav1.DeleteOptions) error
	DeleteCollection(options *metav1.DeleteOptions, listOptions metav1.ListOptions) error
	Get(name string, options metav1.GetOptions) (*v1.APIServer, error)
	List(opts metav1.ListOptions) (*v1.APIServerList, error)
	Watch(opts metav1.ListOptions) (watch.Interface, error)
	Patch(name string, pt types.PatchType, data []byte, subresources ...string) (result *v1.APIServer, err error)
	APIServerExpansion
}

// aPIServers implements APIServerInterface
type aPIServers struct {
	client rest.Interface
}

// newAPIServers returns a APIServers
func newAPIServers(c *ConfigV1Client) *aPIServers {
	return &aPIServers{
		client: c.RESTClient(),
	}
}

// Get takes name of the aPIServer, and returns the corresponding aPIServer object, and an error if there is any.
func (c *aPIServers) Get(name string, options metav1.GetOptions) (result *v1.APIServer, err error) {
	result = &v1.APIServer{}
	err = c.client.Get().
		Resource("apiservers").
		Name(name).
		VersionedParams(&options, scheme.ParameterCodec).
		Do().
		Into(result)
	return
}

// List takes label and field selectors, and returns the list of APIServers that match those selectors.
func (c *aPIServers) List(opts metav1.ListOptions) (result *v1.APIServerList, err error) {
	var timeout time.Duration
	if opts.TimeoutSeconds != nil {
		timeout = time.Duration(*opts.TimeoutSeconds) * time.Second
	}
	result = &v1.APIServerList{}
	err = c.client.Get().
		Resource("apiservers").
		VersionedParams(&opts, scheme.ParameterCodec).
		Timeout(timeout).
		Do().
		Into(result)
	return
}

// Watch returns a watch.Interface that watches the requested aPIServers.
func (c *aPIServers) Watch(opts metav1.ListOptions) (watch.Interface, error) {
	var timeout time.Duration
	if opts.TimeoutSeconds != nil {
		timeout = time.Duration(*opts.TimeoutSeconds) * time.Second
	}
	opts.Watch = true
	return c.client.Get().
		Resource("apiservers").
		VersionedParams(&opts, scheme.ParameterCodec).
		Timeout(timeout).
		Watch()
}

// Create takes the representation of a aPIServer and creates it.  Returns the server's representation of the aPIServer, and an error, if there is any.
func (c *aPIServers) Create(aPIServer *v1.APIServer) (result *v1.APIServer, err error) {
	result = &v1.APIServer{}
	err = c.client.Post().
		Resource("apiservers").
		Body(aPIServer).
		Do().
		Into(result)
	return
}

// Update takes the representation of a aPIServer and updates it. Returns the server's representation of the aPIServer, and an error, if there is any.
func (c *aPIServers) Update(aPIServer *v1.APIServer) (result *v1.APIServer, err error) {
	result = &v1.APIServer{}
	err = c.client.Put().
		Resource("apiservers").
		Name(aPIServer.Name).
		Body(aPIServer).
		Do().
		Into(result)
	return
}

// UpdateStatus was generated because the type contains a Status member.
// Add a +genclient:noStatus comment above the type to avoid generating UpdateStatus().

func (c *aPIServers) UpdateStatus(aPIServer *v1.APIServer) (result *v1.APIServer, err error) {
	result = &v1.APIServer{}
	err = c.client.Put().
		Resource("apiservers").
		Name(aPIServer.Name).
		SubResource("status").
		Body(aPIServer).
		Do().
		Into(result)
	return
}

// Delete takes name of the aPIServer and deletes it. Returns an error if one occurs.
func (c *aPIServers) Delete(name string, options *metav1.DeleteOptions) error {
	return c.client.Delete().
		Resource("apiservers").
		Name(name).
		Body(options).
		Do().
		Error()
}

// DeleteCollection deletes a collection of objects.
func (c *aPIServers) DeleteCollection(options *metav1.DeleteOptions, listOptions metav1.ListOptions) error {
	var timeout time.Duration
	if listOptions.TimeoutSeconds != nil {
		timeout = time.Duration(*listOptions.TimeoutSeconds) * time.Second
	}
	return c.client.Delete().
		Resource("apiservers").
		VersionedParams(&listOptions, scheme.ParameterCodec).
		Timeout(timeout).
		Body(options).
		Do().
		Error()
}

// Patch applies the patch and returns the patched aPIServer.
func (c *aPIServers) Patch(name string, pt types.PatchType, data []byte, subresources ...string) (result *v1.APIServer, err error) {
	result = &v1.APIServer{}
	err = c.client.Patch(pt).
		Resource("apiservers").
		SubResource(subresources...).
		Name(name).
		Body(data).
		Do().
		Into(result)
	return
}
