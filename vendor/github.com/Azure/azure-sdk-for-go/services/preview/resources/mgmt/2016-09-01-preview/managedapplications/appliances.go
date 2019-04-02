package managedapplications

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
	"net/http"
)

// AppliancesClient is the ARM managed applications (appliances)
type AppliancesClient struct {
	BaseClient
}

// NewAppliancesClient creates an instance of the AppliancesClient client.
func NewAppliancesClient(subscriptionID string) AppliancesClient {
	return NewAppliancesClientWithBaseURI(DefaultBaseURI, subscriptionID)
}

// NewAppliancesClientWithBaseURI creates an instance of the AppliancesClient client.
func NewAppliancesClientWithBaseURI(baseURI string, subscriptionID string) AppliancesClient {
	return AppliancesClient{NewWithBaseURI(baseURI, subscriptionID)}
}

// CreateOrUpdate creates a new appliance.
// Parameters:
// resourceGroupName - the name of the resource group. The name is case insensitive.
// applianceName - the name of the appliance.
// parameters - parameters supplied to the create or update an appliance.
func (client AppliancesClient) CreateOrUpdate(ctx context.Context, resourceGroupName string, applianceName string, parameters Appliance) (result AppliancesCreateOrUpdateFuture, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: resourceGroupName,
			Constraints: []validation.Constraint{{Target: "resourceGroupName", Name: validation.MaxLength, Rule: 90, Chain: nil},
				{Target: "resourceGroupName", Name: validation.MinLength, Rule: 1, Chain: nil},
				{Target: "resourceGroupName", Name: validation.Pattern, Rule: `^[-\w\._\(\)]+$`, Chain: nil}}},
		{TargetValue: applianceName,
			Constraints: []validation.Constraint{{Target: "applianceName", Name: validation.MaxLength, Rule: 64, Chain: nil},
				{Target: "applianceName", Name: validation.MinLength, Rule: 3, Chain: nil}}},
		{TargetValue: parameters,
			Constraints: []validation.Constraint{{Target: "parameters.ApplianceProperties", Name: validation.Null, Rule: false,
				Chain: []validation.Constraint{{Target: "parameters.ApplianceProperties.ManagedResourceGroupID", Name: validation.Null, Rule: true, Chain: nil}}},
				{Target: "parameters.Plan", Name: validation.Null, Rule: false,
					Chain: []validation.Constraint{{Target: "parameters.Plan.Name", Name: validation.Null, Rule: true, Chain: nil},
						{Target: "parameters.Plan.Publisher", Name: validation.Null, Rule: true, Chain: nil},
						{Target: "parameters.Plan.Product", Name: validation.Null, Rule: true, Chain: nil},
						{Target: "parameters.Plan.Version", Name: validation.Null, Rule: true, Chain: nil},
					}},
				{Target: "parameters.Kind", Name: validation.Null, Rule: false,
					Chain: []validation.Constraint{{Target: "parameters.Kind", Name: validation.Pattern, Rule: `^[-\w\._,\(\)]+$`, Chain: nil}}}}}}); err != nil {
		return result, validation.NewError("managedapplications.AppliancesClient", "CreateOrUpdate", err.Error())
	}

	req, err := client.CreateOrUpdatePreparer(ctx, resourceGroupName, applianceName, parameters)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "CreateOrUpdate", nil, "Failure preparing request")
		return
	}

	result, err = client.CreateOrUpdateSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "CreateOrUpdate", result.Response(), "Failure sending request")
		return
	}

	return
}

// CreateOrUpdatePreparer prepares the CreateOrUpdate request.
func (client AppliancesClient) CreateOrUpdatePreparer(ctx context.Context, resourceGroupName string, applianceName string, parameters Appliance) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"applianceName":     autorest.Encode("path", applianceName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPut(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/appliances/{applianceName}", pathParameters),
		autorest.WithJSON(parameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// CreateOrUpdateSender sends the CreateOrUpdate request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) CreateOrUpdateSender(req *http.Request) (future AppliancesCreateOrUpdateFuture, err error) {
	var resp *http.Response
	resp, err = autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
	if err != nil {
		return
	}
	future.Future, err = azure.NewFutureFromResponse(resp)
	return
}

// CreateOrUpdateResponder handles the response to the CreateOrUpdate request. The method always
// closes the http.Response Body.
func (client AppliancesClient) CreateOrUpdateResponder(resp *http.Response) (result Appliance, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusCreated),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// CreateOrUpdateByID creates a new appliance.
// Parameters:
// applianceID - the fully qualified ID of the appliance, including the appliance name and the appliance
// resource type. Use the format,
// /subscriptions/{guid}/resourceGroups/{resource-group-name}/Microsoft.Solutions/appliances/{appliance-name}
// parameters - parameters supplied to the create or update an appliance.
func (client AppliancesClient) CreateOrUpdateByID(ctx context.Context, applianceID string, parameters Appliance) (result AppliancesCreateOrUpdateByIDFuture, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: parameters,
			Constraints: []validation.Constraint{{Target: "parameters.ApplianceProperties", Name: validation.Null, Rule: false,
				Chain: []validation.Constraint{{Target: "parameters.ApplianceProperties.ManagedResourceGroupID", Name: validation.Null, Rule: true, Chain: nil}}},
				{Target: "parameters.Plan", Name: validation.Null, Rule: false,
					Chain: []validation.Constraint{{Target: "parameters.Plan.Name", Name: validation.Null, Rule: true, Chain: nil},
						{Target: "parameters.Plan.Publisher", Name: validation.Null, Rule: true, Chain: nil},
						{Target: "parameters.Plan.Product", Name: validation.Null, Rule: true, Chain: nil},
						{Target: "parameters.Plan.Version", Name: validation.Null, Rule: true, Chain: nil},
					}},
				{Target: "parameters.Kind", Name: validation.Null, Rule: false,
					Chain: []validation.Constraint{{Target: "parameters.Kind", Name: validation.Pattern, Rule: `^[-\w\._,\(\)]+$`, Chain: nil}}}}}}); err != nil {
		return result, validation.NewError("managedapplications.AppliancesClient", "CreateOrUpdateByID", err.Error())
	}

	req, err := client.CreateOrUpdateByIDPreparer(ctx, applianceID, parameters)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "CreateOrUpdateByID", nil, "Failure preparing request")
		return
	}

	result, err = client.CreateOrUpdateByIDSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "CreateOrUpdateByID", result.Response(), "Failure sending request")
		return
	}

	return
}

// CreateOrUpdateByIDPreparer prepares the CreateOrUpdateByID request.
func (client AppliancesClient) CreateOrUpdateByIDPreparer(ctx context.Context, applianceID string, parameters Appliance) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"applianceId": applianceID,
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPut(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/{applianceId}", pathParameters),
		autorest.WithJSON(parameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// CreateOrUpdateByIDSender sends the CreateOrUpdateByID request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) CreateOrUpdateByIDSender(req *http.Request) (future AppliancesCreateOrUpdateByIDFuture, err error) {
	var resp *http.Response
	resp, err = autorest.SendWithSender(client, req,
		autorest.DoRetryForStatusCodes(client.RetryAttempts, client.RetryDuration, autorest.StatusCodesForRetry...))
	if err != nil {
		return
	}
	future.Future, err = azure.NewFutureFromResponse(resp)
	return
}

// CreateOrUpdateByIDResponder handles the response to the CreateOrUpdateByID request. The method always
// closes the http.Response Body.
func (client AppliancesClient) CreateOrUpdateByIDResponder(resp *http.Response) (result Appliance, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusCreated),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// Delete deletes the appliance.
// Parameters:
// resourceGroupName - the name of the resource group. The name is case insensitive.
// applianceName - the name of the appliance.
func (client AppliancesClient) Delete(ctx context.Context, resourceGroupName string, applianceName string) (result AppliancesDeleteFuture, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: resourceGroupName,
			Constraints: []validation.Constraint{{Target: "resourceGroupName", Name: validation.MaxLength, Rule: 90, Chain: nil},
				{Target: "resourceGroupName", Name: validation.MinLength, Rule: 1, Chain: nil},
				{Target: "resourceGroupName", Name: validation.Pattern, Rule: `^[-\w\._\(\)]+$`, Chain: nil}}},
		{TargetValue: applianceName,
			Constraints: []validation.Constraint{{Target: "applianceName", Name: validation.MaxLength, Rule: 64, Chain: nil},
				{Target: "applianceName", Name: validation.MinLength, Rule: 3, Chain: nil}}}}); err != nil {
		return result, validation.NewError("managedapplications.AppliancesClient", "Delete", err.Error())
	}

	req, err := client.DeletePreparer(ctx, resourceGroupName, applianceName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "Delete", nil, "Failure preparing request")
		return
	}

	result, err = client.DeleteSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "Delete", result.Response(), "Failure sending request")
		return
	}

	return
}

// DeletePreparer prepares the Delete request.
func (client AppliancesClient) DeletePreparer(ctx context.Context, resourceGroupName string, applianceName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"applianceName":     autorest.Encode("path", applianceName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsDelete(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/appliances/{applianceName}", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// DeleteSender sends the Delete request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) DeleteSender(req *http.Request) (future AppliancesDeleteFuture, err error) {
	var resp *http.Response
	resp, err = autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
	if err != nil {
		return
	}
	future.Future, err = azure.NewFutureFromResponse(resp)
	return
}

// DeleteResponder handles the response to the Delete request. The method always
// closes the http.Response Body.
func (client AppliancesClient) DeleteResponder(resp *http.Response) (result autorest.Response, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted, http.StatusNoContent),
		autorest.ByClosing())
	result.Response = resp
	return
}

// DeleteByID deletes the appliance.
// Parameters:
// applianceID - the fully qualified ID of the appliance, including the appliance name and the appliance
// resource type. Use the format,
// /subscriptions/{guid}/resourceGroups/{resource-group-name}/Microsoft.Solutions/appliances/{appliance-name}
func (client AppliancesClient) DeleteByID(ctx context.Context, applianceID string) (result AppliancesDeleteByIDFuture, err error) {
	req, err := client.DeleteByIDPreparer(ctx, applianceID)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "DeleteByID", nil, "Failure preparing request")
		return
	}

	result, err = client.DeleteByIDSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "DeleteByID", result.Response(), "Failure sending request")
		return
	}

	return
}

// DeleteByIDPreparer prepares the DeleteByID request.
func (client AppliancesClient) DeleteByIDPreparer(ctx context.Context, applianceID string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"applianceId": applianceID,
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsDelete(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/{applianceId}", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// DeleteByIDSender sends the DeleteByID request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) DeleteByIDSender(req *http.Request) (future AppliancesDeleteByIDFuture, err error) {
	var resp *http.Response
	resp, err = autorest.SendWithSender(client, req,
		autorest.DoRetryForStatusCodes(client.RetryAttempts, client.RetryDuration, autorest.StatusCodesForRetry...))
	if err != nil {
		return
	}
	future.Future, err = azure.NewFutureFromResponse(resp)
	return
}

// DeleteByIDResponder handles the response to the DeleteByID request. The method always
// closes the http.Response Body.
func (client AppliancesClient) DeleteByIDResponder(resp *http.Response) (result autorest.Response, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted, http.StatusNoContent),
		autorest.ByClosing())
	result.Response = resp
	return
}

// Get gets the appliance.
// Parameters:
// resourceGroupName - the name of the resource group. The name is case insensitive.
// applianceName - the name of the appliance.
func (client AppliancesClient) Get(ctx context.Context, resourceGroupName string, applianceName string) (result Appliance, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: resourceGroupName,
			Constraints: []validation.Constraint{{Target: "resourceGroupName", Name: validation.MaxLength, Rule: 90, Chain: nil},
				{Target: "resourceGroupName", Name: validation.MinLength, Rule: 1, Chain: nil},
				{Target: "resourceGroupName", Name: validation.Pattern, Rule: `^[-\w\._\(\)]+$`, Chain: nil}}},
		{TargetValue: applianceName,
			Constraints: []validation.Constraint{{Target: "applianceName", Name: validation.MaxLength, Rule: 64, Chain: nil},
				{Target: "applianceName", Name: validation.MinLength, Rule: 3, Chain: nil}}}}); err != nil {
		return result, validation.NewError("managedapplications.AppliancesClient", "Get", err.Error())
	}

	req, err := client.GetPreparer(ctx, resourceGroupName, applianceName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "Get", nil, "Failure preparing request")
		return
	}

	resp, err := client.GetSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "Get", resp, "Failure sending request")
		return
	}

	result, err = client.GetResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "Get", resp, "Failure responding to request")
	}

	return
}

// GetPreparer prepares the Get request.
func (client AppliancesClient) GetPreparer(ctx context.Context, resourceGroupName string, applianceName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"applianceName":     autorest.Encode("path", applianceName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/appliances/{applianceName}", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// GetSender sends the Get request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) GetSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
}

// GetResponder handles the response to the Get request. The method always
// closes the http.Response Body.
func (client AppliancesClient) GetResponder(resp *http.Response) (result Appliance, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusNotFound),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// GetByID gets the appliance.
// Parameters:
// applianceID - the fully qualified ID of the appliance, including the appliance name and the appliance
// resource type. Use the format,
// /subscriptions/{guid}/resourceGroups/{resource-group-name}/Microsoft.Solutions/appliances/{appliance-name}
func (client AppliancesClient) GetByID(ctx context.Context, applianceID string) (result Appliance, err error) {
	req, err := client.GetByIDPreparer(ctx, applianceID)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "GetByID", nil, "Failure preparing request")
		return
	}

	resp, err := client.GetByIDSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "GetByID", resp, "Failure sending request")
		return
	}

	result, err = client.GetByIDResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "GetByID", resp, "Failure responding to request")
	}

	return
}

// GetByIDPreparer prepares the GetByID request.
func (client AppliancesClient) GetByIDPreparer(ctx context.Context, applianceID string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"applianceId": applianceID,
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/{applianceId}", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// GetByIDSender sends the GetByID request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) GetByIDSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		autorest.DoRetryForStatusCodes(client.RetryAttempts, client.RetryDuration, autorest.StatusCodesForRetry...))
}

// GetByIDResponder handles the response to the GetByID request. The method always
// closes the http.Response Body.
func (client AppliancesClient) GetByIDResponder(resp *http.Response) (result Appliance, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusNotFound),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// ListByResourceGroup gets all the appliances within a resource group.
// Parameters:
// resourceGroupName - the name of the resource group. The name is case insensitive.
func (client AppliancesClient) ListByResourceGroup(ctx context.Context, resourceGroupName string) (result ApplianceListResultPage, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: resourceGroupName,
			Constraints: []validation.Constraint{{Target: "resourceGroupName", Name: validation.MaxLength, Rule: 90, Chain: nil},
				{Target: "resourceGroupName", Name: validation.MinLength, Rule: 1, Chain: nil},
				{Target: "resourceGroupName", Name: validation.Pattern, Rule: `^[-\w\._\(\)]+$`, Chain: nil}}}}); err != nil {
		return result, validation.NewError("managedapplications.AppliancesClient", "ListByResourceGroup", err.Error())
	}

	result.fn = client.listByResourceGroupNextResults
	req, err := client.ListByResourceGroupPreparer(ctx, resourceGroupName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "ListByResourceGroup", nil, "Failure preparing request")
		return
	}

	resp, err := client.ListByResourceGroupSender(req)
	if err != nil {
		result.alr.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "ListByResourceGroup", resp, "Failure sending request")
		return
	}

	result.alr, err = client.ListByResourceGroupResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "ListByResourceGroup", resp, "Failure responding to request")
	}

	return
}

// ListByResourceGroupPreparer prepares the ListByResourceGroup request.
func (client AppliancesClient) ListByResourceGroupPreparer(ctx context.Context, resourceGroupName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/appliances", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// ListByResourceGroupSender sends the ListByResourceGroup request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) ListByResourceGroupSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
}

// ListByResourceGroupResponder handles the response to the ListByResourceGroup request. The method always
// closes the http.Response Body.
func (client AppliancesClient) ListByResourceGroupResponder(resp *http.Response) (result ApplianceListResult, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// listByResourceGroupNextResults retrieves the next set of results, if any.
func (client AppliancesClient) listByResourceGroupNextResults(lastResults ApplianceListResult) (result ApplianceListResult, err error) {
	req, err := lastResults.applianceListResultPreparer()
	if err != nil {
		return result, autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "listByResourceGroupNextResults", nil, "Failure preparing next results request")
	}
	if req == nil {
		return
	}
	resp, err := client.ListByResourceGroupSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		return result, autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "listByResourceGroupNextResults", resp, "Failure sending next results request")
	}
	result, err = client.ListByResourceGroupResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "listByResourceGroupNextResults", resp, "Failure responding to next results request")
	}
	return
}

// ListByResourceGroupComplete enumerates all values, automatically crossing page boundaries as required.
func (client AppliancesClient) ListByResourceGroupComplete(ctx context.Context, resourceGroupName string) (result ApplianceListResultIterator, err error) {
	result.page, err = client.ListByResourceGroup(ctx, resourceGroupName)
	return
}

// ListBySubscription gets all the appliances within a subscription.
func (client AppliancesClient) ListBySubscription(ctx context.Context) (result ApplianceListResultPage, err error) {
	result.fn = client.listBySubscriptionNextResults
	req, err := client.ListBySubscriptionPreparer(ctx)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "ListBySubscription", nil, "Failure preparing request")
		return
	}

	resp, err := client.ListBySubscriptionSender(req)
	if err != nil {
		result.alr.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "ListBySubscription", resp, "Failure sending request")
		return
	}

	result.alr, err = client.ListBySubscriptionResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "ListBySubscription", resp, "Failure responding to request")
	}

	return
}

// ListBySubscriptionPreparer prepares the ListBySubscription request.
func (client AppliancesClient) ListBySubscriptionPreparer(ctx context.Context) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"subscriptionId": autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/providers/Microsoft.Solutions/appliances", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// ListBySubscriptionSender sends the ListBySubscription request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) ListBySubscriptionSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
}

// ListBySubscriptionResponder handles the response to the ListBySubscription request. The method always
// closes the http.Response Body.
func (client AppliancesClient) ListBySubscriptionResponder(resp *http.Response) (result ApplianceListResult, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// listBySubscriptionNextResults retrieves the next set of results, if any.
func (client AppliancesClient) listBySubscriptionNextResults(lastResults ApplianceListResult) (result ApplianceListResult, err error) {
	req, err := lastResults.applianceListResultPreparer()
	if err != nil {
		return result, autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "listBySubscriptionNextResults", nil, "Failure preparing next results request")
	}
	if req == nil {
		return
	}
	resp, err := client.ListBySubscriptionSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		return result, autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "listBySubscriptionNextResults", resp, "Failure sending next results request")
	}
	result, err = client.ListBySubscriptionResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "listBySubscriptionNextResults", resp, "Failure responding to next results request")
	}
	return
}

// ListBySubscriptionComplete enumerates all values, automatically crossing page boundaries as required.
func (client AppliancesClient) ListBySubscriptionComplete(ctx context.Context) (result ApplianceListResultIterator, err error) {
	result.page, err = client.ListBySubscription(ctx)
	return
}

// Update updates an existing appliance. The only value that can be updated via PATCH currently is the tags.
// Parameters:
// resourceGroupName - the name of the resource group. The name is case insensitive.
// applianceName - the name of the appliance.
// parameters - parameters supplied to update an existing appliance.
func (client AppliancesClient) Update(ctx context.Context, resourceGroupName string, applianceName string, parameters *Appliance) (result Appliance, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: resourceGroupName,
			Constraints: []validation.Constraint{{Target: "resourceGroupName", Name: validation.MaxLength, Rule: 90, Chain: nil},
				{Target: "resourceGroupName", Name: validation.MinLength, Rule: 1, Chain: nil},
				{Target: "resourceGroupName", Name: validation.Pattern, Rule: `^[-\w\._\(\)]+$`, Chain: nil}}},
		{TargetValue: applianceName,
			Constraints: []validation.Constraint{{Target: "applianceName", Name: validation.MaxLength, Rule: 64, Chain: nil},
				{Target: "applianceName", Name: validation.MinLength, Rule: 3, Chain: nil}}}}); err != nil {
		return result, validation.NewError("managedapplications.AppliancesClient", "Update", err.Error())
	}

	req, err := client.UpdatePreparer(ctx, resourceGroupName, applianceName, parameters)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "Update", nil, "Failure preparing request")
		return
	}

	resp, err := client.UpdateSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "Update", resp, "Failure sending request")
		return
	}

	result, err = client.UpdateResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "Update", resp, "Failure responding to request")
	}

	return
}

// UpdatePreparer prepares the Update request.
func (client AppliancesClient) UpdatePreparer(ctx context.Context, resourceGroupName string, applianceName string, parameters *Appliance) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"applianceName":     autorest.Encode("path", applianceName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPatch(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Solutions/appliances/{applianceName}", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	if parameters != nil {
		preparer = autorest.DecoratePreparer(preparer,
			autorest.WithJSON(parameters))
	}
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// UpdateSender sends the Update request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) UpdateSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
}

// UpdateResponder handles the response to the Update request. The method always
// closes the http.Response Body.
func (client AppliancesClient) UpdateResponder(resp *http.Response) (result Appliance, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// UpdateByID updates an existing appliance. The only value that can be updated via PATCH currently is the tags.
// Parameters:
// applianceID - the fully qualified ID of the appliance, including the appliance name and the appliance
// resource type. Use the format,
// /subscriptions/{guid}/resourceGroups/{resource-group-name}/Microsoft.Solutions/appliances/{appliance-name}
// parameters - parameters supplied to update an existing appliance.
func (client AppliancesClient) UpdateByID(ctx context.Context, applianceID string, parameters *Appliance) (result Appliance, err error) {
	req, err := client.UpdateByIDPreparer(ctx, applianceID, parameters)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "UpdateByID", nil, "Failure preparing request")
		return
	}

	resp, err := client.UpdateByIDSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "UpdateByID", resp, "Failure sending request")
		return
	}

	result, err = client.UpdateByIDResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "managedapplications.AppliancesClient", "UpdateByID", resp, "Failure responding to request")
	}

	return
}

// UpdateByIDPreparer prepares the UpdateByID request.
func (client AppliancesClient) UpdateByIDPreparer(ctx context.Context, applianceID string, parameters *Appliance) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"applianceId": applianceID,
	}

	const APIVersion = "2016-09-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPatch(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/{applianceId}", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	if parameters != nil {
		preparer = autorest.DecoratePreparer(preparer,
			autorest.WithJSON(parameters))
	}
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// UpdateByIDSender sends the UpdateByID request. The method will close the
// http.Response Body if it receives an error.
func (client AppliancesClient) UpdateByIDSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		autorest.DoRetryForStatusCodes(client.RetryAttempts, client.RetryDuration, autorest.StatusCodesForRetry...))
}

// UpdateByIDResponder handles the response to the UpdateByID request. The method always
// closes the http.Response Body.
func (client AppliancesClient) UpdateByIDResponder(resp *http.Response) (result Appliance, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}
