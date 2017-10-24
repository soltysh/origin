package fake

import (
	apps_v1 "github.com/openshift/origin/pkg/apps/apis/apps/v1"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	labels "k8s.io/apimachinery/pkg/labels"
	schema "k8s.io/apimachinery/pkg/runtime/schema"
	types "k8s.io/apimachinery/pkg/types"
	watch "k8s.io/apimachinery/pkg/watch"
	testing "k8s.io/client-go/testing"
	v1beta1 "k8s.io/kubernetes/pkg/apis/extensions/v1beta1"
)

// FakeDeploymentConfigs implements DeploymentConfigInterface
type FakeDeploymentConfigs struct {
	Fake *FakeAppsV1
	ns   string
}

var deploymentconfigsResource = schema.GroupVersionResource{Group: "apps.openshift.io", Version: "v1", Resource: "deploymentconfigs"}

var deploymentconfigsKind = schema.GroupVersionKind{Group: "apps.openshift.io", Version: "v1", Kind: "DeploymentConfig"}

// Get takes name of the deploymentConfig, and returns the corresponding deploymentConfig object, and an error if there is any.
func (c *FakeDeploymentConfigs) Get(name string, options v1.GetOptions) (result *apps_v1.DeploymentConfig, err error) {
	obj, err := c.Fake.
		Invokes(testing.NewGetAction(deploymentconfigsResource, c.ns, name), &apps_v1.DeploymentConfig{})

	if obj == nil {
		return nil, err
	}
	return obj.(*apps_v1.DeploymentConfig), err
}

// List takes label and field selectors, and returns the list of DeploymentConfigs that match those selectors.
func (c *FakeDeploymentConfigs) List(opts v1.ListOptions) (result *apps_v1.DeploymentConfigList, err error) {
	obj, err := c.Fake.
		Invokes(testing.NewListAction(deploymentconfigsResource, deploymentconfigsKind, c.ns, opts), &apps_v1.DeploymentConfigList{})

	if obj == nil {
		return nil, err
	}

	label, _, _ := testing.ExtractFromListOptions(opts)
	if label == nil {
		label = labels.Everything()
	}
	list := &apps_v1.DeploymentConfigList{}
	for _, item := range obj.(*apps_v1.DeploymentConfigList).Items {
		if label.Matches(labels.Set(item.Labels)) {
			list.Items = append(list.Items, item)
		}
	}
	return list, err
}

// Watch returns a watch.Interface that watches the requested deploymentConfigs.
func (c *FakeDeploymentConfigs) Watch(opts v1.ListOptions) (watch.Interface, error) {
	return c.Fake.
		InvokesWatch(testing.NewWatchAction(deploymentconfigsResource, c.ns, opts))

}

// Create takes the representation of a deploymentConfig and creates it.  Returns the server's representation of the deploymentConfig, and an error, if there is any.
func (c *FakeDeploymentConfigs) Create(deploymentConfig *apps_v1.DeploymentConfig) (result *apps_v1.DeploymentConfig, err error) {
	obj, err := c.Fake.
		Invokes(testing.NewCreateAction(deploymentconfigsResource, c.ns, deploymentConfig), &apps_v1.DeploymentConfig{})

	if obj == nil {
		return nil, err
	}
	return obj.(*apps_v1.DeploymentConfig), err
}

// Update takes the representation of a deploymentConfig and updates it. Returns the server's representation of the deploymentConfig, and an error, if there is any.
func (c *FakeDeploymentConfigs) Update(deploymentConfig *apps_v1.DeploymentConfig) (result *apps_v1.DeploymentConfig, err error) {
	obj, err := c.Fake.
		Invokes(testing.NewUpdateAction(deploymentconfigsResource, c.ns, deploymentConfig), &apps_v1.DeploymentConfig{})

	if obj == nil {
		return nil, err
	}
	return obj.(*apps_v1.DeploymentConfig), err
}

// UpdateStatus was generated because the type contains a Status member.
// Add a +genclient:noStatus comment above the type to avoid generating UpdateStatus().
func (c *FakeDeploymentConfigs) UpdateStatus(deploymentConfig *apps_v1.DeploymentConfig) (*apps_v1.DeploymentConfig, error) {
	obj, err := c.Fake.
		Invokes(testing.NewUpdateSubresourceAction(deploymentconfigsResource, "status", c.ns, deploymentConfig), &apps_v1.DeploymentConfig{})

	if obj == nil {
		return nil, err
	}
	return obj.(*apps_v1.DeploymentConfig), err
}

// Delete takes name of the deploymentConfig and deletes it. Returns an error if one occurs.
func (c *FakeDeploymentConfigs) Delete(name string, options *v1.DeleteOptions) error {
	_, err := c.Fake.
		Invokes(testing.NewDeleteAction(deploymentconfigsResource, c.ns, name), &apps_v1.DeploymentConfig{})

	return err
}

// DeleteCollection deletes a collection of objects.
func (c *FakeDeploymentConfigs) DeleteCollection(options *v1.DeleteOptions, listOptions v1.ListOptions) error {
	action := testing.NewDeleteCollectionAction(deploymentconfigsResource, c.ns, listOptions)

	_, err := c.Fake.Invokes(action, &apps_v1.DeploymentConfigList{})
	return err
}

// Patch applies the patch and returns the patched deploymentConfig.
func (c *FakeDeploymentConfigs) Patch(name string, pt types.PatchType, data []byte, subresources ...string) (result *apps_v1.DeploymentConfig, err error) {
	obj, err := c.Fake.
		Invokes(testing.NewPatchSubresourceAction(deploymentconfigsResource, c.ns, name, data, subresources...), &apps_v1.DeploymentConfig{})

	if obj == nil {
		return nil, err
	}
	return obj.(*apps_v1.DeploymentConfig), err
}

// Instantiate takes the representation of a deploymentRequest and creates it.  Returns the server's representation of the deploymentConfig, and an error, if there is any.
func (c *FakeDeploymentConfigs) Instantiate(deploymentConfigName string, deploymentRequest *apps_v1.DeploymentRequest) (result *apps_v1.DeploymentConfig, err error) {
	obj, err := c.Fake.
		Invokes(testing.NewCreateSubresourceAction(deploymentconfigsResource, deploymentConfigName, "instantiate", c.ns, deploymentRequest), &apps_v1.DeploymentConfig{})

	if obj == nil {
		return nil, err
	}
	return obj.(*apps_v1.DeploymentConfig), err
}

// Rollback takes the representation of a deploymentConfigRollback and creates it.  Returns the server's representation of the deploymentConfig, and an error, if there is any.
func (c *FakeDeploymentConfigs) Rollback(deploymentConfigName string, deploymentConfigRollback *apps_v1.DeploymentConfigRollback) (result *apps_v1.DeploymentConfig, err error) {
	obj, err := c.Fake.
		Invokes(testing.NewCreateSubresourceAction(deploymentconfigsResource, deploymentConfigName, "rollback", c.ns, deploymentConfigRollback), &apps_v1.DeploymentConfig{})

	if obj == nil {
		return nil, err
	}
	return obj.(*apps_v1.DeploymentConfig), err
}

// GetScale takes name of the deploymentConfig, and returns the corresponding scale object, and an error if there is any.
func (c *FakeDeploymentConfigs) GetScale(deploymentConfigName string, options v1.GetOptions) (result *v1beta1.Scale, err error) {
	obj, err := c.Fake.
		Invokes(testing.NewGetSubresourceAction(deploymentconfigsResource, c.ns, "scale", deploymentConfigName), &v1beta1.Scale{})

	if obj == nil {
		return nil, err
	}
	return obj.(*v1beta1.Scale), err
}

// UpdateScale takes the representation of a scale and updates it. Returns the server's representation of the scale, and an error, if there is any.
func (c *FakeDeploymentConfigs) UpdateScale(deploymentConfigName string, scale *v1beta1.Scale) (result *v1beta1.Scale, err error) {
	obj, err := c.Fake.
		Invokes(testing.NewUpdateSubresourceAction(deploymentconfigsResource, "scale", c.ns, scale), &v1beta1.Scale{})

	if obj == nil {
		return nil, err
	}
	return obj.(*v1beta1.Scale), err
}
