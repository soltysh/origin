package storsimple

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
	"context"
	"github.com/Azure/go-autorest/autorest"
	"github.com/Azure/go-autorest/autorest/azure"
	"github.com/Azure/go-autorest/autorest/validation"
	"github.com/Azure/go-autorest/tracing"
	"net/http"
)

// DeviceSettingsClient is the client for the DeviceSettings methods of the Storsimple service.
type DeviceSettingsClient struct {
	BaseClient
}

// NewDeviceSettingsClient creates an instance of the DeviceSettingsClient client.
func NewDeviceSettingsClient(subscriptionID string) DeviceSettingsClient {
	return NewDeviceSettingsClientWithBaseURI(DefaultBaseURI, subscriptionID)
}

// NewDeviceSettingsClientWithBaseURI creates an instance of the DeviceSettingsClient client.
func NewDeviceSettingsClientWithBaseURI(baseURI string, subscriptionID string) DeviceSettingsClient {
	return DeviceSettingsClient{NewWithBaseURI(baseURI, subscriptionID)}
}

// CreateOrUpdateAlertSettings creates or updates the alert settings of the specified device.
// Parameters:
// deviceName - the device name
// parameters - the alert settings to be added or updated.
// resourceGroupName - the resource group name
// managerName - the manager name
func (client DeviceSettingsClient) CreateOrUpdateAlertSettings(ctx context.Context, deviceName string, parameters AlertSettings, resourceGroupName string, managerName string) (result DeviceSettingsCreateOrUpdateAlertSettingsFuture, err error) {
	if tracing.IsEnabled() {
		ctx = tracing.StartSpan(ctx, fqdn+"/DeviceSettingsClient.CreateOrUpdateAlertSettings")
		defer func() {
			sc := -1
			if result.Response() != nil {
				sc = result.Response().StatusCode
			}
			tracing.EndSpan(ctx, sc, err)
		}()
	}
	if err := validation.Validate([]validation.Validation{
		{TargetValue: parameters,
			Constraints: []validation.Constraint{{Target: "parameters.AlertNotificationProperties", Name: validation.Null, Rule: true, Chain: nil}}},
		{TargetValue: managerName,
			Constraints: []validation.Constraint{{Target: "managerName", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "managerName", Name: validation.MinLength, Rule: 2, Chain: nil}}}}); err != nil {
		return result, validation.NewError("storsimple.DeviceSettingsClient", "CreateOrUpdateAlertSettings", err.Error())
	}

	req, err := client.CreateOrUpdateAlertSettingsPreparer(ctx, deviceName, parameters, resourceGroupName, managerName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "CreateOrUpdateAlertSettings", nil, "Failure preparing request")
		return
	}

	result, err = client.CreateOrUpdateAlertSettingsSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "CreateOrUpdateAlertSettings", result.Response(), "Failure sending request")
		return
	}

	return
}

// CreateOrUpdateAlertSettingsPreparer prepares the CreateOrUpdateAlertSettings request.
func (client DeviceSettingsClient) CreateOrUpdateAlertSettingsPreparer(ctx context.Context, deviceName string, parameters AlertSettings, resourceGroupName string, managerName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"deviceName":        deviceName,
		"managerName":       managerName,
		"resourceGroupName": resourceGroupName,
		"subscriptionId":    client.SubscriptionID,
	}

	const APIVersion = "2017-06-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPut(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorSimple/managers/{managerName}/devices/{deviceName}/alertSettings/default", pathParameters),
		autorest.WithJSON(parameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// CreateOrUpdateAlertSettingsSender sends the CreateOrUpdateAlertSettings request. The method will close the
// http.Response Body if it receives an error.
func (client DeviceSettingsClient) CreateOrUpdateAlertSettingsSender(req *http.Request) (future DeviceSettingsCreateOrUpdateAlertSettingsFuture, err error) {
	sd := autorest.GetSendDecorators(req.Context(), azure.DoRetryWithRegistration(client.Client))
	var resp *http.Response
	resp, err = autorest.SendWithSender(client, req, sd...)
	if err != nil {
		return
	}
	future.Future, err = azure.NewFutureFromResponse(resp)
	return
}

// CreateOrUpdateAlertSettingsResponder handles the response to the CreateOrUpdateAlertSettings request. The method always
// closes the http.Response Body.
func (client DeviceSettingsClient) CreateOrUpdateAlertSettingsResponder(resp *http.Response) (result AlertSettings, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// CreateOrUpdateTimeSettings creates or updates the time settings of the specified device.
// Parameters:
// deviceName - the device name
// parameters - the time settings to be added or updated.
// resourceGroupName - the resource group name
// managerName - the manager name
func (client DeviceSettingsClient) CreateOrUpdateTimeSettings(ctx context.Context, deviceName string, parameters TimeSettings, resourceGroupName string, managerName string) (result DeviceSettingsCreateOrUpdateTimeSettingsFuture, err error) {
	if tracing.IsEnabled() {
		ctx = tracing.StartSpan(ctx, fqdn+"/DeviceSettingsClient.CreateOrUpdateTimeSettings")
		defer func() {
			sc := -1
			if result.Response() != nil {
				sc = result.Response().StatusCode
			}
			tracing.EndSpan(ctx, sc, err)
		}()
	}
	if err := validation.Validate([]validation.Validation{
		{TargetValue: parameters,
			Constraints: []validation.Constraint{{Target: "parameters.TimeSettingsProperties", Name: validation.Null, Rule: true,
				Chain: []validation.Constraint{{Target: "parameters.TimeSettingsProperties.TimeZone", Name: validation.Null, Rule: true, Chain: nil}}}}},
		{TargetValue: managerName,
			Constraints: []validation.Constraint{{Target: "managerName", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "managerName", Name: validation.MinLength, Rule: 2, Chain: nil}}}}); err != nil {
		return result, validation.NewError("storsimple.DeviceSettingsClient", "CreateOrUpdateTimeSettings", err.Error())
	}

	req, err := client.CreateOrUpdateTimeSettingsPreparer(ctx, deviceName, parameters, resourceGroupName, managerName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "CreateOrUpdateTimeSettings", nil, "Failure preparing request")
		return
	}

	result, err = client.CreateOrUpdateTimeSettingsSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "CreateOrUpdateTimeSettings", result.Response(), "Failure sending request")
		return
	}

	return
}

// CreateOrUpdateTimeSettingsPreparer prepares the CreateOrUpdateTimeSettings request.
func (client DeviceSettingsClient) CreateOrUpdateTimeSettingsPreparer(ctx context.Context, deviceName string, parameters TimeSettings, resourceGroupName string, managerName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"deviceName":        deviceName,
		"managerName":       managerName,
		"resourceGroupName": resourceGroupName,
		"subscriptionId":    client.SubscriptionID,
	}

	const APIVersion = "2017-06-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPut(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorSimple/managers/{managerName}/devices/{deviceName}/timeSettings/default", pathParameters),
		autorest.WithJSON(parameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// CreateOrUpdateTimeSettingsSender sends the CreateOrUpdateTimeSettings request. The method will close the
// http.Response Body if it receives an error.
func (client DeviceSettingsClient) CreateOrUpdateTimeSettingsSender(req *http.Request) (future DeviceSettingsCreateOrUpdateTimeSettingsFuture, err error) {
	sd := autorest.GetSendDecorators(req.Context(), azure.DoRetryWithRegistration(client.Client))
	var resp *http.Response
	resp, err = autorest.SendWithSender(client, req, sd...)
	if err != nil {
		return
	}
	future.Future, err = azure.NewFutureFromResponse(resp)
	return
}

// CreateOrUpdateTimeSettingsResponder handles the response to the CreateOrUpdateTimeSettings request. The method always
// closes the http.Response Body.
func (client DeviceSettingsClient) CreateOrUpdateTimeSettingsResponder(resp *http.Response) (result TimeSettings, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// GetAlertSettings gets the alert settings of the specified device.
// Parameters:
// deviceName - the device name
// resourceGroupName - the resource group name
// managerName - the manager name
func (client DeviceSettingsClient) GetAlertSettings(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (result AlertSettings, err error) {
	if tracing.IsEnabled() {
		ctx = tracing.StartSpan(ctx, fqdn+"/DeviceSettingsClient.GetAlertSettings")
		defer func() {
			sc := -1
			if result.Response.Response != nil {
				sc = result.Response.Response.StatusCode
			}
			tracing.EndSpan(ctx, sc, err)
		}()
	}
	if err := validation.Validate([]validation.Validation{
		{TargetValue: managerName,
			Constraints: []validation.Constraint{{Target: "managerName", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "managerName", Name: validation.MinLength, Rule: 2, Chain: nil}}}}); err != nil {
		return result, validation.NewError("storsimple.DeviceSettingsClient", "GetAlertSettings", err.Error())
	}

	req, err := client.GetAlertSettingsPreparer(ctx, deviceName, resourceGroupName, managerName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetAlertSettings", nil, "Failure preparing request")
		return
	}

	resp, err := client.GetAlertSettingsSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetAlertSettings", resp, "Failure sending request")
		return
	}

	result, err = client.GetAlertSettingsResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetAlertSettings", resp, "Failure responding to request")
	}

	return
}

// GetAlertSettingsPreparer prepares the GetAlertSettings request.
func (client DeviceSettingsClient) GetAlertSettingsPreparer(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"deviceName":        deviceName,
		"managerName":       managerName,
		"resourceGroupName": resourceGroupName,
		"subscriptionId":    client.SubscriptionID,
	}

	const APIVersion = "2017-06-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorSimple/managers/{managerName}/devices/{deviceName}/alertSettings/default", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// GetAlertSettingsSender sends the GetAlertSettings request. The method will close the
// http.Response Body if it receives an error.
func (client DeviceSettingsClient) GetAlertSettingsSender(req *http.Request) (*http.Response, error) {
	sd := autorest.GetSendDecorators(req.Context(), azure.DoRetryWithRegistration(client.Client))
	return autorest.SendWithSender(client, req, sd...)
}

// GetAlertSettingsResponder handles the response to the GetAlertSettings request. The method always
// closes the http.Response Body.
func (client DeviceSettingsClient) GetAlertSettingsResponder(resp *http.Response) (result AlertSettings, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// GetNetworkSettings gets the network settings of the specified device.
// Parameters:
// deviceName - the device name
// resourceGroupName - the resource group name
// managerName - the manager name
func (client DeviceSettingsClient) GetNetworkSettings(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (result NetworkSettings, err error) {
	if tracing.IsEnabled() {
		ctx = tracing.StartSpan(ctx, fqdn+"/DeviceSettingsClient.GetNetworkSettings")
		defer func() {
			sc := -1
			if result.Response.Response != nil {
				sc = result.Response.Response.StatusCode
			}
			tracing.EndSpan(ctx, sc, err)
		}()
	}
	if err := validation.Validate([]validation.Validation{
		{TargetValue: managerName,
			Constraints: []validation.Constraint{{Target: "managerName", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "managerName", Name: validation.MinLength, Rule: 2, Chain: nil}}}}); err != nil {
		return result, validation.NewError("storsimple.DeviceSettingsClient", "GetNetworkSettings", err.Error())
	}

	req, err := client.GetNetworkSettingsPreparer(ctx, deviceName, resourceGroupName, managerName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetNetworkSettings", nil, "Failure preparing request")
		return
	}

	resp, err := client.GetNetworkSettingsSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetNetworkSettings", resp, "Failure sending request")
		return
	}

	result, err = client.GetNetworkSettingsResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetNetworkSettings", resp, "Failure responding to request")
	}

	return
}

// GetNetworkSettingsPreparer prepares the GetNetworkSettings request.
func (client DeviceSettingsClient) GetNetworkSettingsPreparer(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"deviceName":        deviceName,
		"managerName":       managerName,
		"resourceGroupName": resourceGroupName,
		"subscriptionId":    client.SubscriptionID,
	}

	const APIVersion = "2017-06-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorSimple/managers/{managerName}/devices/{deviceName}/networkSettings/default", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// GetNetworkSettingsSender sends the GetNetworkSettings request. The method will close the
// http.Response Body if it receives an error.
func (client DeviceSettingsClient) GetNetworkSettingsSender(req *http.Request) (*http.Response, error) {
	sd := autorest.GetSendDecorators(req.Context(), azure.DoRetryWithRegistration(client.Client))
	return autorest.SendWithSender(client, req, sd...)
}

// GetNetworkSettingsResponder handles the response to the GetNetworkSettings request. The method always
// closes the http.Response Body.
func (client DeviceSettingsClient) GetNetworkSettingsResponder(resp *http.Response) (result NetworkSettings, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// GetSecuritySettings returns the Security properties of the specified device name.
// Parameters:
// deviceName - the device name
// resourceGroupName - the resource group name
// managerName - the manager name
func (client DeviceSettingsClient) GetSecuritySettings(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (result SecuritySettings, err error) {
	if tracing.IsEnabled() {
		ctx = tracing.StartSpan(ctx, fqdn+"/DeviceSettingsClient.GetSecuritySettings")
		defer func() {
			sc := -1
			if result.Response.Response != nil {
				sc = result.Response.Response.StatusCode
			}
			tracing.EndSpan(ctx, sc, err)
		}()
	}
	if err := validation.Validate([]validation.Validation{
		{TargetValue: managerName,
			Constraints: []validation.Constraint{{Target: "managerName", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "managerName", Name: validation.MinLength, Rule: 2, Chain: nil}}}}); err != nil {
		return result, validation.NewError("storsimple.DeviceSettingsClient", "GetSecuritySettings", err.Error())
	}

	req, err := client.GetSecuritySettingsPreparer(ctx, deviceName, resourceGroupName, managerName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetSecuritySettings", nil, "Failure preparing request")
		return
	}

	resp, err := client.GetSecuritySettingsSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetSecuritySettings", resp, "Failure sending request")
		return
	}

	result, err = client.GetSecuritySettingsResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetSecuritySettings", resp, "Failure responding to request")
	}

	return
}

// GetSecuritySettingsPreparer prepares the GetSecuritySettings request.
func (client DeviceSettingsClient) GetSecuritySettingsPreparer(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"deviceName":        deviceName,
		"managerName":       managerName,
		"resourceGroupName": resourceGroupName,
		"subscriptionId":    client.SubscriptionID,
	}

	const APIVersion = "2017-06-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorSimple/managers/{managerName}/devices/{deviceName}/securitySettings/default", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// GetSecuritySettingsSender sends the GetSecuritySettings request. The method will close the
// http.Response Body if it receives an error.
func (client DeviceSettingsClient) GetSecuritySettingsSender(req *http.Request) (*http.Response, error) {
	sd := autorest.GetSendDecorators(req.Context(), azure.DoRetryWithRegistration(client.Client))
	return autorest.SendWithSender(client, req, sd...)
}

// GetSecuritySettingsResponder handles the response to the GetSecuritySettings request. The method always
// closes the http.Response Body.
func (client DeviceSettingsClient) GetSecuritySettingsResponder(resp *http.Response) (result SecuritySettings, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// GetTimeSettings gets the time settings of the specified device.
// Parameters:
// deviceName - the device name
// resourceGroupName - the resource group name
// managerName - the manager name
func (client DeviceSettingsClient) GetTimeSettings(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (result TimeSettings, err error) {
	if tracing.IsEnabled() {
		ctx = tracing.StartSpan(ctx, fqdn+"/DeviceSettingsClient.GetTimeSettings")
		defer func() {
			sc := -1
			if result.Response.Response != nil {
				sc = result.Response.Response.StatusCode
			}
			tracing.EndSpan(ctx, sc, err)
		}()
	}
	if err := validation.Validate([]validation.Validation{
		{TargetValue: managerName,
			Constraints: []validation.Constraint{{Target: "managerName", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "managerName", Name: validation.MinLength, Rule: 2, Chain: nil}}}}); err != nil {
		return result, validation.NewError("storsimple.DeviceSettingsClient", "GetTimeSettings", err.Error())
	}

	req, err := client.GetTimeSettingsPreparer(ctx, deviceName, resourceGroupName, managerName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetTimeSettings", nil, "Failure preparing request")
		return
	}

	resp, err := client.GetTimeSettingsSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetTimeSettings", resp, "Failure sending request")
		return
	}

	result, err = client.GetTimeSettingsResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "GetTimeSettings", resp, "Failure responding to request")
	}

	return
}

// GetTimeSettingsPreparer prepares the GetTimeSettings request.
func (client DeviceSettingsClient) GetTimeSettingsPreparer(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"deviceName":        deviceName,
		"managerName":       managerName,
		"resourceGroupName": resourceGroupName,
		"subscriptionId":    client.SubscriptionID,
	}

	const APIVersion = "2017-06-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorSimple/managers/{managerName}/devices/{deviceName}/timeSettings/default", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// GetTimeSettingsSender sends the GetTimeSettings request. The method will close the
// http.Response Body if it receives an error.
func (client DeviceSettingsClient) GetTimeSettingsSender(req *http.Request) (*http.Response, error) {
	sd := autorest.GetSendDecorators(req.Context(), azure.DoRetryWithRegistration(client.Client))
	return autorest.SendWithSender(client, req, sd...)
}

// GetTimeSettingsResponder handles the response to the GetTimeSettings request. The method always
// closes the http.Response Body.
func (client DeviceSettingsClient) GetTimeSettingsResponder(resp *http.Response) (result TimeSettings, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// SyncRemotemanagementCertificate sync Remote management Certificate between appliance and Service
// Parameters:
// deviceName - the device name
// resourceGroupName - the resource group name
// managerName - the manager name
func (client DeviceSettingsClient) SyncRemotemanagementCertificate(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (result DeviceSettingsSyncRemotemanagementCertificateFuture, err error) {
	if tracing.IsEnabled() {
		ctx = tracing.StartSpan(ctx, fqdn+"/DeviceSettingsClient.SyncRemotemanagementCertificate")
		defer func() {
			sc := -1
			if result.Response() != nil {
				sc = result.Response().StatusCode
			}
			tracing.EndSpan(ctx, sc, err)
		}()
	}
	if err := validation.Validate([]validation.Validation{
		{TargetValue: managerName,
			Constraints: []validation.Constraint{{Target: "managerName", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "managerName", Name: validation.MinLength, Rule: 2, Chain: nil}}}}); err != nil {
		return result, validation.NewError("storsimple.DeviceSettingsClient", "SyncRemotemanagementCertificate", err.Error())
	}

	req, err := client.SyncRemotemanagementCertificatePreparer(ctx, deviceName, resourceGroupName, managerName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "SyncRemotemanagementCertificate", nil, "Failure preparing request")
		return
	}

	result, err = client.SyncRemotemanagementCertificateSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "SyncRemotemanagementCertificate", result.Response(), "Failure sending request")
		return
	}

	return
}

// SyncRemotemanagementCertificatePreparer prepares the SyncRemotemanagementCertificate request.
func (client DeviceSettingsClient) SyncRemotemanagementCertificatePreparer(ctx context.Context, deviceName string, resourceGroupName string, managerName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"deviceName":        deviceName,
		"managerName":       managerName,
		"resourceGroupName": resourceGroupName,
		"subscriptionId":    client.SubscriptionID,
	}

	const APIVersion = "2017-06-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsPost(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorSimple/managers/{managerName}/devices/{deviceName}/securitySettings/default/syncRemoteManagementCertificate", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// SyncRemotemanagementCertificateSender sends the SyncRemotemanagementCertificate request. The method will close the
// http.Response Body if it receives an error.
func (client DeviceSettingsClient) SyncRemotemanagementCertificateSender(req *http.Request) (future DeviceSettingsSyncRemotemanagementCertificateFuture, err error) {
	sd := autorest.GetSendDecorators(req.Context(), azure.DoRetryWithRegistration(client.Client))
	var resp *http.Response
	resp, err = autorest.SendWithSender(client, req, sd...)
	if err != nil {
		return
	}
	future.Future, err = azure.NewFutureFromResponse(resp)
	return
}

// SyncRemotemanagementCertificateResponder handles the response to the SyncRemotemanagementCertificate request. The method always
// closes the http.Response Body.
func (client DeviceSettingsClient) SyncRemotemanagementCertificateResponder(resp *http.Response) (result autorest.Response, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted, http.StatusNoContent),
		autorest.ByClosing())
	result.Response = resp
	return
}

// UpdateNetworkSettings updates the network settings on the specified device.
// Parameters:
// deviceName - the device name
// parameters - the network settings to be updated.
// resourceGroupName - the resource group name
// managerName - the manager name
func (client DeviceSettingsClient) UpdateNetworkSettings(ctx context.Context, deviceName string, parameters NetworkSettingsPatch, resourceGroupName string, managerName string) (result DeviceSettingsUpdateNetworkSettingsFuture, err error) {
	if tracing.IsEnabled() {
		ctx = tracing.StartSpan(ctx, fqdn+"/DeviceSettingsClient.UpdateNetworkSettings")
		defer func() {
			sc := -1
			if result.Response() != nil {
				sc = result.Response().StatusCode
			}
			tracing.EndSpan(ctx, sc, err)
		}()
	}
	if err := validation.Validate([]validation.Validation{
		{TargetValue: managerName,
			Constraints: []validation.Constraint{{Target: "managerName", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "managerName", Name: validation.MinLength, Rule: 2, Chain: nil}}}}); err != nil {
		return result, validation.NewError("storsimple.DeviceSettingsClient", "UpdateNetworkSettings", err.Error())
	}

	req, err := client.UpdateNetworkSettingsPreparer(ctx, deviceName, parameters, resourceGroupName, managerName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "UpdateNetworkSettings", nil, "Failure preparing request")
		return
	}

	result, err = client.UpdateNetworkSettingsSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "UpdateNetworkSettings", result.Response(), "Failure sending request")
		return
	}

	return
}

// UpdateNetworkSettingsPreparer prepares the UpdateNetworkSettings request.
func (client DeviceSettingsClient) UpdateNetworkSettingsPreparer(ctx context.Context, deviceName string, parameters NetworkSettingsPatch, resourceGroupName string, managerName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"deviceName":        deviceName,
		"managerName":       managerName,
		"resourceGroupName": resourceGroupName,
		"subscriptionId":    client.SubscriptionID,
	}

	const APIVersion = "2017-06-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPatch(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorSimple/managers/{managerName}/devices/{deviceName}/networkSettings/default", pathParameters),
		autorest.WithJSON(parameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// UpdateNetworkSettingsSender sends the UpdateNetworkSettings request. The method will close the
// http.Response Body if it receives an error.
func (client DeviceSettingsClient) UpdateNetworkSettingsSender(req *http.Request) (future DeviceSettingsUpdateNetworkSettingsFuture, err error) {
	sd := autorest.GetSendDecorators(req.Context(), azure.DoRetryWithRegistration(client.Client))
	var resp *http.Response
	resp, err = autorest.SendWithSender(client, req, sd...)
	if err != nil {
		return
	}
	future.Future, err = azure.NewFutureFromResponse(resp)
	return
}

// UpdateNetworkSettingsResponder handles the response to the UpdateNetworkSettings request. The method always
// closes the http.Response Body.
func (client DeviceSettingsClient) UpdateNetworkSettingsResponder(resp *http.Response) (result NetworkSettings, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// UpdateSecuritySettings patch Security properties of the specified device name.
// Parameters:
// deviceName - the device name
// parameters - the security settings properties to be patched.
// resourceGroupName - the resource group name
// managerName - the manager name
func (client DeviceSettingsClient) UpdateSecuritySettings(ctx context.Context, deviceName string, parameters SecuritySettingsPatch, resourceGroupName string, managerName string) (result DeviceSettingsUpdateSecuritySettingsFuture, err error) {
	if tracing.IsEnabled() {
		ctx = tracing.StartSpan(ctx, fqdn+"/DeviceSettingsClient.UpdateSecuritySettings")
		defer func() {
			sc := -1
			if result.Response() != nil {
				sc = result.Response().StatusCode
			}
			tracing.EndSpan(ctx, sc, err)
		}()
	}
	if err := validation.Validate([]validation.Validation{
		{TargetValue: managerName,
			Constraints: []validation.Constraint{{Target: "managerName", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "managerName", Name: validation.MinLength, Rule: 2, Chain: nil}}}}); err != nil {
		return result, validation.NewError("storsimple.DeviceSettingsClient", "UpdateSecuritySettings", err.Error())
	}

	req, err := client.UpdateSecuritySettingsPreparer(ctx, deviceName, parameters, resourceGroupName, managerName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "UpdateSecuritySettings", nil, "Failure preparing request")
		return
	}

	result, err = client.UpdateSecuritySettingsSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "storsimple.DeviceSettingsClient", "UpdateSecuritySettings", result.Response(), "Failure sending request")
		return
	}

	return
}

// UpdateSecuritySettingsPreparer prepares the UpdateSecuritySettings request.
func (client DeviceSettingsClient) UpdateSecuritySettingsPreparer(ctx context.Context, deviceName string, parameters SecuritySettingsPatch, resourceGroupName string, managerName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"deviceName":        deviceName,
		"managerName":       managerName,
		"resourceGroupName": resourceGroupName,
		"subscriptionId":    client.SubscriptionID,
	}

	const APIVersion = "2017-06-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPatch(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.StorSimple/managers/{managerName}/devices/{deviceName}/securitySettings/default", pathParameters),
		autorest.WithJSON(parameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// UpdateSecuritySettingsSender sends the UpdateSecuritySettings request. The method will close the
// http.Response Body if it receives an error.
func (client DeviceSettingsClient) UpdateSecuritySettingsSender(req *http.Request) (future DeviceSettingsUpdateSecuritySettingsFuture, err error) {
	sd := autorest.GetSendDecorators(req.Context(), azure.DoRetryWithRegistration(client.Client))
	var resp *http.Response
	resp, err = autorest.SendWithSender(client, req, sd...)
	if err != nil {
		return
	}
	future.Future, err = azure.NewFutureFromResponse(resp)
	return
}

// UpdateSecuritySettingsResponder handles the response to the UpdateSecuritySettings request. The method always
// closes the http.Response Body.
func (client DeviceSettingsClient) UpdateSecuritySettingsResponder(resp *http.Response) (result SecuritySettings, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}
