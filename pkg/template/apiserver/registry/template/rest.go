package template

import (
	"context"
	"math/rand"
	"time"

	"k8s.io/klog"

	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apiserver/pkg/registry/rest"

	"github.com/openshift/api/template"
	"github.com/openshift/library-go/pkg/template/generator"
	templateapi "github.com/openshift/origin/pkg/template/apis/template"
	templatevalidation "github.com/openshift/origin/pkg/template/apis/template/validation"
	"github.com/openshift/origin/pkg/template/templateprocessing"
)

// REST implements RESTStorage interface for processing Template objects.
type REST struct {
}

var _ rest.Creater = &REST{}
var _ rest.Scoper = &REST{}

// NewREST creates new RESTStorage interface for processing Template objects. If
// legacyReturn is used, a Config object is returned. Otherwise, a List is returned
func NewREST() *REST {
	return &REST{}
}

// New returns a new Template
// TODO: this is the input, but not the output. pkg/api/rest should probably allow
// a rest.Storage object to vary its output or input types (not sure whether New()
// should be input or output... probably input).
func (s *REST) New() runtime.Object {
	return &templateapi.Template{}
}

func (s *REST) NamespaceScoped() bool {
	return true
}

// Create processes a Template and creates a new list of objects
func (s *REST) Create(ctx context.Context, obj runtime.Object, _ rest.ValidateObjectFunc, options *metav1.CreateOptions) (runtime.Object, error) {
	tpl, ok := obj.(*templateapi.Template)
	if !ok {
		return nil, errors.NewBadRequest("not a template")
	}
	if errs := templatevalidation.ValidateProcessedTemplate(tpl); len(errs) > 0 {
		return nil, errors.NewInvalid(template.Kind("Template"), tpl.Name, errs)
	}

	generators := map[string]generator.Generator{
		"expression": generator.NewExpressionValueGenerator(rand.New(rand.NewSource(time.Now().UnixNano()))),
	}
	processor := templateprocessing.NewProcessor(generators)
	if errs := processor.Process(tpl); len(errs) > 0 {
		klog.V(1).Infof(errs.ToAggregate().Error())
		return nil, errors.NewInvalid(template.Kind("Template"), tpl.Name, errs)
	}

	// we know that we get back runtime.Unstructured objects from the Process call.  We need to encode those
	// objects using the unstructured codec BEFORE the REST layers gets its shot at encoding to avoid a layered
	// encode being done.
	for i := range tpl.Objects {
		tpl.Objects[i] = runtime.NewEncodable(unstructured.UnstructuredJSONScheme, tpl.Objects[i])
	}

	return tpl, nil
}
