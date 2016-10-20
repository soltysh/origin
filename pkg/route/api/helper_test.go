package api

import (
	"testing"
	"time"

	kapi "k8s.io/kubernetes/pkg/api"
	"k8s.io/kubernetes/pkg/api/unversioned"
	"k8s.io/kubernetes/pkg/types"
)

func TestRouteLessThan(t *testing.T) {
	olderTimestamp := unversioned.Now().Rfc3339Copy()
	newerTimestamp := unversioned.Time{
		Time: olderTimestamp.Add(1 * time.Minute),
	}

	tcs := []struct {
		testName   string
		timestamp1 unversioned.Time
		timestamp2 unversioned.Time
		uid1       types.UID
		uid2       types.UID
		expected   bool
	}{
		{
			testName:   "Older route less than newer route",
			timestamp1: olderTimestamp,
			timestamp2: newerTimestamp,
			expected:   true,
		},
		{
			testName:   "Newer route not less than older route",
			timestamp1: newerTimestamp,
			timestamp2: olderTimestamp,
			expected:   false,
		},
		{
			testName:   "Same age route less with smaller uid",
			timestamp1: newerTimestamp,
			timestamp2: newerTimestamp,
			uid1:       "alpha",
			uid2:       "beta",
			expected:   true,
		},
		{
			testName:   "Same age route not less with greater uid",
			timestamp1: newerTimestamp,
			timestamp2: newerTimestamp,
			uid1:       "beta",
			uid2:       "alpha",
			expected:   false,
		},
	}

	for _, tc := range tcs {
		r1 := &Route{
			ObjectMeta: kapi.ObjectMeta{
				CreationTimestamp: tc.timestamp1,
				UID:               tc.uid1,
			},
		}
		r2 := &Route{
			ObjectMeta: kapi.ObjectMeta{
				CreationTimestamp: tc.timestamp2,
				UID:               tc.uid2,
			},
		}

		if RouteLessThan(r1, r2) != tc.expected {
			var msg string
			if tc.expected {
				msg = "Expected %v to be less than %v"
			} else {
				msg = "Expected %v to not be less than %v"
			}
			t.Errorf(msg, r1, r2)
		}
	}
}
