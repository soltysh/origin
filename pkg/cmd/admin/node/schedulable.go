package node

import (
	"fmt"

	kapi "k8s.io/kubernetes/pkg/api"
	kerrors "k8s.io/kubernetes/pkg/util/errors"
)

type SchedulableOptions struct {
	Options *NodeOptions

	Schedulable bool
}

func (s *SchedulableOptions) Run() error {
	nodes, err := s.Options.GetNodes()
	if err != nil {
		return err
	}

	errList := []error{}
	ignoreHeaders := false
	for _, node := range nodes {
		err := s.RunSchedulable(node, &ignoreHeaders)
		if err != nil {
			// Don't bail out if one node fails
			errList = append(errList, err)
		}
	}
	return kerrors.NewAggregate(errList)
}

func (s *SchedulableOptions) RunSchedulable(node *kapi.Node, ignoreHeaders *bool) error {
	var updatedNode *kapi.Node
	var err error

	if node.Spec.Unschedulable != !s.Schedulable {
		node.Spec.Unschedulable = !s.Schedulable

		patch := fmt.Sprintf(`{"spec":{"unschedulable":%t}}`, node.Spec.Unschedulable)
		err := s.Options.Kclient.Patch(kapi.MergePatchType).Resource("nodes").Name(node.Name).Body([]byte(patch)).Do().Error()
		if err != nil {
			return err
		}
	}

	updatedNode = node

	printerWithHeaders, printerNoHeaders, err := s.Options.GetPrintersByObject(updatedNode)
	if err != nil {
		return err
	}
	if *ignoreHeaders {
		printerNoHeaders.PrintObj(updatedNode, s.Options.Writer)
	} else {
		printerWithHeaders.PrintObj(updatedNode, s.Options.Writer)
		*ignoreHeaders = true
	}
	return nil
}
