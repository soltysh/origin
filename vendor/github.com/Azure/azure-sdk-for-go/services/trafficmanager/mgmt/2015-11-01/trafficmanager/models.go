package trafficmanager

// Copyright (c) Microsoft and contributors.  All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Code generated by Microsoft (R) AutoRest Code Generator.
// Changes may cause incorrect behavior and will be lost if the code is regenerated.

import (
	"encoding/json"
	"github.com/Azure/go-autorest/autorest"
)

// The package's fully qualified name.
const fqdn = "github.com/Azure/azure-sdk-for-go/services/trafficmanager/mgmt/2015-11-01/trafficmanager"

// CheckTrafficManagerRelativeDNSNameAvailabilityParameters parameters supplied to check Traffic Manager
// name operation.
type CheckTrafficManagerRelativeDNSNameAvailabilityParameters struct {
	// Name - Gets or sets the name of the resource.
	Name *string `json:"name,omitempty"`
	// Type - Gets or sets the type of the resource.
	Type *string `json:"type,omitempty"`
}

// DNSConfig class containing DNS settings in a Traffic Manager profile.
type DNSConfig struct {
	// RelativeName - Gets or sets the relative DNS name provided by this Traffic Manager profile.  This value is combined with the DNS domain name used by Azure Traffic Manager to form the fully-qualified domain name (FQDN) of the profile.
	RelativeName *string `json:"relativeName,omitempty"`
	// Fqdn - Gets or sets the fully-qualified domain name (FQDN) of the Traffic Manager profile.  This is formed from the concatenation of the RelativeName with the DNS domain used by Azure Traffic Manager.
	Fqdn *string `json:"fqdn,omitempty"`
	// TTL - Gets or sets the DNS Time-To-Live (TTL), in seconds.  This informs the local DNS resolvers and DNS clients how long to cache DNS responses provided by this Traffic Manager profile.
	TTL *int64 `json:"ttl,omitempty"`
}

// Endpoint class representing a Traffic Manager endpoint.
type Endpoint struct {
	autorest.Response `json:"-"`
	// ID - Gets or sets the ID of the Traffic Manager endpoint.
	ID *string `json:"id,omitempty"`
	// Name - Gets or sets the name of the Traffic Manager endpoint.
	Name *string `json:"name,omitempty"`
	// Type - Gets or sets the endpoint type of the Traffic Manager endpoint.
	Type                *string `json:"type,omitempty"`
	*EndpointProperties `json:"properties,omitempty"`
}

// MarshalJSON is the custom marshaler for Endpoint.
func (e Endpoint) MarshalJSON() ([]byte, error) {
	objectMap := make(map[string]interface{})
	if e.ID != nil {
		objectMap["id"] = e.ID
	}
	if e.Name != nil {
		objectMap["name"] = e.Name
	}
	if e.Type != nil {
		objectMap["type"] = e.Type
	}
	if e.EndpointProperties != nil {
		objectMap["properties"] = e.EndpointProperties
	}
	return json.Marshal(objectMap)
}

// UnmarshalJSON is the custom unmarshaler for Endpoint struct.
func (e *Endpoint) UnmarshalJSON(body []byte) error {
	var m map[string]*json.RawMessage
	err := json.Unmarshal(body, &m)
	if err != nil {
		return err
	}
	for k, v := range m {
		switch k {
		case "id":
			if v != nil {
				var ID string
				err = json.Unmarshal(*v, &ID)
				if err != nil {
					return err
				}
				e.ID = &ID
			}
		case "name":
			if v != nil {
				var name string
				err = json.Unmarshal(*v, &name)
				if err != nil {
					return err
				}
				e.Name = &name
			}
		case "type":
			if v != nil {
				var typeVar string
				err = json.Unmarshal(*v, &typeVar)
				if err != nil {
					return err
				}
				e.Type = &typeVar
			}
		case "properties":
			if v != nil {
				var endpointProperties EndpointProperties
				err = json.Unmarshal(*v, &endpointProperties)
				if err != nil {
					return err
				}
				e.EndpointProperties = &endpointProperties
			}
		}
	}

	return nil
}

// EndpointProperties class representing a Traffic Manager endpoint properties.
type EndpointProperties struct {
	// TargetResourceID - Gets or sets the Azure Resource URI of the of the endpoint.  Not applicable to endpoints of type 'ExternalEndpoints'.
	TargetResourceID *string `json:"targetResourceId,omitempty"`
	// Target - Gets or sets the fully-qualified DNS name of the endpoint.  Traffic Manager returns this value in DNS responses to direct traffic to this endpoint.
	Target *string `json:"target,omitempty"`
	// EndpointStatus - Gets or sets the status of the endpoint..  If the endpoint is Enabled, it is probed for endpoint health and is included in the traffic routing method.  Possible values are 'Enabled' and 'Disabled'.
	EndpointStatus *string `json:"endpointStatus,omitempty"`
	// Weight - Gets or sets the weight of this endpoint when using the 'Weighted' traffic routing method. Possible values are from 1 to 1000.
	Weight *int64 `json:"weight,omitempty"`
	// Priority - Gets or sets the priority of this endpoint when using the ‘Priority’ traffic routing method. Possible values are from 1 to 1000, lower values represent higher priority. This is an optional parameter.  If specified, it must be specified on all endpoints, and no two endpoints can share the same priority value.
	Priority *int64 `json:"priority,omitempty"`
	// EndpointLocation - Specifies the location of the external or nested endpoints when using the ‘Performance’ traffic routing method.
	EndpointLocation *string `json:"endpointLocation,omitempty"`
	// EndpointMonitorStatus - Gets or sets the monitoring status of the endpoint.
	EndpointMonitorStatus *string `json:"endpointMonitorStatus,omitempty"`
	// MinChildEndpoints - Gets or sets the minimum number of endpoints that must be available in the child profile in order for the parent profile to be considered available. Only applicable to endpoint of type 'NestedEndpoints'.
	MinChildEndpoints *int64 `json:"minChildEndpoints,omitempty"`
}

// MonitorConfig class containing endpoint monitoring settings in a Traffic Manager profile.
type MonitorConfig struct {
	// ProfileMonitorStatus - Gets or sets the profile-level monitoring status of the Traffic Manager profile.
	ProfileMonitorStatus *string `json:"profileMonitorStatus,omitempty"`
	// Protocol - Gets or sets the protocol (HTTP or HTTPS) used to probe for endpoint health.
	Protocol *string `json:"protocol,omitempty"`
	// Port - Gets or sets the TCP port used to probe for endpoint health.
	Port *int64 `json:"port,omitempty"`
	// Path - Gets or sets the path relative to the endpoint domain name used to probe for endpoint health.
	Path *string `json:"path,omitempty"`
}

// NameAvailability class representing a Traffic Manager Name Availability response.
type NameAvailability struct {
	autorest.Response `json:"-"`
	// Name - The relative name.
	Name *string `json:"name,omitempty"`
	// Type - Traffic Manager profile resource type.
	Type *string `json:"type,omitempty"`
	// NameAvailable - Describes whether the relative name is available or not.
	NameAvailable *bool `json:"nameAvailable,omitempty"`
	// Reason - The reason why the name is not available, when applicable.
	Reason *string `json:"reason,omitempty"`
	// Message - Descriptive message that explains why the name is not available, when applicable.
	Message *string `json:"message,omitempty"`
}

// Profile class representing a Traffic Manager profile.
type Profile struct {
	autorest.Response  `json:"-"`
	*ProfileProperties `json:"properties,omitempty"`
	// ID - READ-ONLY; Resource Id
	ID *string `json:"id,omitempty"`
	// Name - READ-ONLY; Resource name
	Name *string `json:"name,omitempty"`
	// Type - READ-ONLY; Resource type
	Type *string `json:"type,omitempty"`
	// Location - Resource location
	Location *string `json:"location,omitempty"`
	// Tags - Resource tags
	Tags map[string]*string `json:"tags"`
}

// MarshalJSON is the custom marshaler for Profile.
func (p Profile) MarshalJSON() ([]byte, error) {
	objectMap := make(map[string]interface{})
	if p.ProfileProperties != nil {
		objectMap["properties"] = p.ProfileProperties
	}
	if p.Location != nil {
		objectMap["location"] = p.Location
	}
	if p.Tags != nil {
		objectMap["tags"] = p.Tags
	}
	return json.Marshal(objectMap)
}

// UnmarshalJSON is the custom unmarshaler for Profile struct.
func (p *Profile) UnmarshalJSON(body []byte) error {
	var m map[string]*json.RawMessage
	err := json.Unmarshal(body, &m)
	if err != nil {
		return err
	}
	for k, v := range m {
		switch k {
		case "properties":
			if v != nil {
				var profileProperties ProfileProperties
				err = json.Unmarshal(*v, &profileProperties)
				if err != nil {
					return err
				}
				p.ProfileProperties = &profileProperties
			}
		case "id":
			if v != nil {
				var ID string
				err = json.Unmarshal(*v, &ID)
				if err != nil {
					return err
				}
				p.ID = &ID
			}
		case "name":
			if v != nil {
				var name string
				err = json.Unmarshal(*v, &name)
				if err != nil {
					return err
				}
				p.Name = &name
			}
		case "type":
			if v != nil {
				var typeVar string
				err = json.Unmarshal(*v, &typeVar)
				if err != nil {
					return err
				}
				p.Type = &typeVar
			}
		case "location":
			if v != nil {
				var location string
				err = json.Unmarshal(*v, &location)
				if err != nil {
					return err
				}
				p.Location = &location
			}
		case "tags":
			if v != nil {
				var tags map[string]*string
				err = json.Unmarshal(*v, &tags)
				if err != nil {
					return err
				}
				p.Tags = tags
			}
		}
	}

	return nil
}

// ProfileListResult the list Traffic Manager profiles operation response.
type ProfileListResult struct {
	autorest.Response `json:"-"`
	// Value - Gets the list of Traffic manager profiles.
	Value *[]Profile `json:"value,omitempty"`
}

// ProfileProperties class representing the Traffic Manager profile properties.
type ProfileProperties struct {
	// ProfileStatus - Gets or sets the status of the Traffic Manager profile.  Possible values are 'Enabled' and 'Disabled'.
	ProfileStatus *string `json:"profileStatus,omitempty"`
	// TrafficRoutingMethod - Gets or sets the traffic routing method of the Traffic Manager profile.  Possible values are 'Performance', 'Weighted', or 'Priority'.
	TrafficRoutingMethod *string `json:"trafficRoutingMethod,omitempty"`
	// DNSConfig - Gets or sets the DNS settings of the Traffic Manager profile.
	DNSConfig *DNSConfig `json:"dnsConfig,omitempty"`
	// MonitorConfig - Gets or sets the endpoint monitoring settings of the Traffic Manager profile.
	MonitorConfig *MonitorConfig `json:"monitorConfig,omitempty"`
	// Endpoints - Gets or sets the list of endpoints in the Traffic Manager profile.
	Endpoints *[]Endpoint `json:"endpoints,omitempty"`
}

// Resource ...
type Resource struct {
	// ID - READ-ONLY; Resource Id
	ID *string `json:"id,omitempty"`
	// Name - READ-ONLY; Resource name
	Name *string `json:"name,omitempty"`
	// Type - READ-ONLY; Resource type
	Type *string `json:"type,omitempty"`
	// Location - Resource location
	Location *string `json:"location,omitempty"`
	// Tags - Resource tags
	Tags map[string]*string `json:"tags"`
}

// MarshalJSON is the custom marshaler for Resource.
func (r Resource) MarshalJSON() ([]byte, error) {
	objectMap := make(map[string]interface{})
	if r.Location != nil {
		objectMap["location"] = r.Location
	}
	if r.Tags != nil {
		objectMap["tags"] = r.Tags
	}
	return json.Marshal(objectMap)
}

// SubResource ...
type SubResource struct {
	// ID - Resource Id
	ID *string `json:"id,omitempty"`
}
