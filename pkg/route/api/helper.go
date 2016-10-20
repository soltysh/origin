package api

import (
	kapi "k8s.io/kubernetes/pkg/api"
)

// IngressConditionStatus returns the first status and condition matching the provided ingress condition type. Conditions
// prefer the first matching entry and clients are allowed to ignore later conditions of the same type.
func IngressConditionStatus(ingress *RouteIngress, t RouteIngressConditionType) (kapi.ConditionStatus, RouteIngressCondition) {
	for _, condition := range ingress.Conditions {
		if t != condition.Type {
			continue
		}
		return condition.Status, condition
	}
	return kapi.ConditionUnknown, RouteIngressCondition{}
}

func RouteLessThan(route1, route2 *Route) bool {
	if route1.CreationTimestamp.Before(route2.CreationTimestamp) {
		return true
	}
	if route2.CreationTimestamp.Before(route1.CreationTimestamp) {
		return false
	}
	// In the event that timestamps are equal, use UID as a tie-breaker.
	// Creation timestamps are in RFC3339 format, only accurate to the second.
	return route1.UID < route2.UID
}
