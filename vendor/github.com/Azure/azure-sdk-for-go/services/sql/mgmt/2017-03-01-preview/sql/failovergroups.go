package sql

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

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// FailoverGroupsClient is the the Azure SQL Database management API provides a RESTful set of web services that
// interact with Azure SQL Database services to manage your databases. The API enables you to create, retrieve, update,
// and delete databases.
type FailoverGroupsClient struct {
	BaseClient
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// NewFailoverGroupsClient creates an instance of the FailoverGroupsClient client.
func NewFailoverGroupsClient(subscriptionID string) FailoverGroupsClient {
	return NewFailoverGroupsClientWithBaseURI(DefaultBaseURI, subscriptionID)
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// NewFailoverGroupsClientWithBaseURI creates an instance of the FailoverGroupsClient client.
func NewFailoverGroupsClientWithBaseURI(baseURI string, subscriptionID string) FailoverGroupsClient {
	return FailoverGroupsClient{NewWithBaseURI(baseURI, subscriptionID)}
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// CreateOrUpdate creates or updates a failover group.
//
// resourceGroupName is the name of the resource group that contains the resource. You can obtain this value from
// the Azure Resource Manager API or the portal. serverName is the name of the server containing the failover
// group. failoverGroupName is the name of the failover group. parameters is the failover group parameters.
func (client FailoverGroupsClient) CreateOrUpdate(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string, parameters FailoverGroup) (result FailoverGroupsCreateOrUpdateFuture, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: parameters,
			Constraints: []validation.Constraint{{Target: "parameters.FailoverGroupProperties", Name: validation.Null, Rule: false,
				Chain: []validation.Constraint{{Target: "parameters.FailoverGroupProperties.ReadWriteEndpoint", Name: validation.Null, Rule: true, Chain: nil},
					{Target: "parameters.FailoverGroupProperties.PartnerServers", Name: validation.Null, Rule: true, Chain: nil},
				}}}}}); err != nil {
		return result, validation.NewError("sql.FailoverGroupsClient", "CreateOrUpdate", err.Error())
	}

	req, err := client.CreateOrUpdatePreparer(ctx, resourceGroupName, serverName, failoverGroupName, parameters)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "CreateOrUpdate", nil, "Failure preparing request")
		return
	}

	result, err = client.CreateOrUpdateSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "CreateOrUpdate", result.Response(), "Failure sending request")
		return
	}

	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// CreateOrUpdatePreparer prepares the CreateOrUpdate request.
func (client FailoverGroupsClient) CreateOrUpdatePreparer(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string, parameters FailoverGroup) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"failoverGroupName": autorest.Encode("path", failoverGroupName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"serverName":        autorest.Encode("path", serverName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2015-05-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPut(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/failoverGroups/{failoverGroupName}", pathParameters),
		autorest.WithJSON(parameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// CreateOrUpdateSender sends the CreateOrUpdate request. The method will close the
// http.Response Body if it receives an error.
func (client FailoverGroupsClient) CreateOrUpdateSender(req *http.Request) (future FailoverGroupsCreateOrUpdateFuture, err error) {
	sender := autorest.DecorateSender(client, azure.DoRetryWithRegistration(client.Client))
	future.Future = azure.NewFuture(req)
	future.req = req
	_, err = future.Done(sender)
	if err != nil {
		return
	}
	err = autorest.Respond(future.Response(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusCreated, http.StatusAccepted))
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// CreateOrUpdateResponder handles the response to the CreateOrUpdate request. The method always
// closes the http.Response Body.
func (client FailoverGroupsClient) CreateOrUpdateResponder(resp *http.Response) (result FailoverGroup, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusCreated, http.StatusAccepted),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// Delete deletes a failover group.
//
// resourceGroupName is the name of the resource group that contains the resource. You can obtain this value from
// the Azure Resource Manager API or the portal. serverName is the name of the server containing the failover
// group. failoverGroupName is the name of the failover group.
func (client FailoverGroupsClient) Delete(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string) (result FailoverGroupsDeleteFuture, err error) {
	req, err := client.DeletePreparer(ctx, resourceGroupName, serverName, failoverGroupName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "Delete", nil, "Failure preparing request")
		return
	}

	result, err = client.DeleteSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "Delete", result.Response(), "Failure sending request")
		return
	}

	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// DeletePreparer prepares the Delete request.
func (client FailoverGroupsClient) DeletePreparer(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"failoverGroupName": autorest.Encode("path", failoverGroupName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"serverName":        autorest.Encode("path", serverName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2015-05-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsDelete(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/failoverGroups/{failoverGroupName}", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// DeleteSender sends the Delete request. The method will close the
// http.Response Body if it receives an error.
func (client FailoverGroupsClient) DeleteSender(req *http.Request) (future FailoverGroupsDeleteFuture, err error) {
	sender := autorest.DecorateSender(client, azure.DoRetryWithRegistration(client.Client))
	future.Future = azure.NewFuture(req)
	future.req = req
	_, err = future.Done(sender)
	if err != nil {
		return
	}
	err = autorest.Respond(future.Response(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted, http.StatusNoContent))
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// DeleteResponder handles the response to the Delete request. The method always
// closes the http.Response Body.
func (client FailoverGroupsClient) DeleteResponder(resp *http.Response) (result autorest.Response, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted, http.StatusNoContent),
		autorest.ByClosing())
	result.Response = resp
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// Failover fails over from the current primary server to this server.
//
// resourceGroupName is the name of the resource group that contains the resource. You can obtain this value from
// the Azure Resource Manager API or the portal. serverName is the name of the server containing the failover
// group. failoverGroupName is the name of the failover group.
func (client FailoverGroupsClient) Failover(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string) (result FailoverGroupsFailoverFuture, err error) {
	req, err := client.FailoverPreparer(ctx, resourceGroupName, serverName, failoverGroupName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "Failover", nil, "Failure preparing request")
		return
	}

	result, err = client.FailoverSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "Failover", result.Response(), "Failure sending request")
		return
	}

	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// FailoverPreparer prepares the Failover request.
func (client FailoverGroupsClient) FailoverPreparer(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"failoverGroupName": autorest.Encode("path", failoverGroupName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"serverName":        autorest.Encode("path", serverName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2015-05-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsPost(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/failoverGroups/{failoverGroupName}/failover", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// FailoverSender sends the Failover request. The method will close the
// http.Response Body if it receives an error.
func (client FailoverGroupsClient) FailoverSender(req *http.Request) (future FailoverGroupsFailoverFuture, err error) {
	sender := autorest.DecorateSender(client, azure.DoRetryWithRegistration(client.Client))
	future.Future = azure.NewFuture(req)
	future.req = req
	_, err = future.Done(sender)
	if err != nil {
		return
	}
	err = autorest.Respond(future.Response(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted))
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// FailoverResponder handles the response to the Failover request. The method always
// closes the http.Response Body.
func (client FailoverGroupsClient) FailoverResponder(resp *http.Response) (result FailoverGroup, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// ForceFailoverAllowDataLoss fails over from the current primary server to this server. This operation might result in
// data loss.
//
// resourceGroupName is the name of the resource group that contains the resource. You can obtain this value from
// the Azure Resource Manager API or the portal. serverName is the name of the server containing the failover
// group. failoverGroupName is the name of the failover group.
func (client FailoverGroupsClient) ForceFailoverAllowDataLoss(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string) (result FailoverGroupsForceFailoverAllowDataLossFuture, err error) {
	req, err := client.ForceFailoverAllowDataLossPreparer(ctx, resourceGroupName, serverName, failoverGroupName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "ForceFailoverAllowDataLoss", nil, "Failure preparing request")
		return
	}

	result, err = client.ForceFailoverAllowDataLossSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "ForceFailoverAllowDataLoss", result.Response(), "Failure sending request")
		return
	}

	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// ForceFailoverAllowDataLossPreparer prepares the ForceFailoverAllowDataLoss request.
func (client FailoverGroupsClient) ForceFailoverAllowDataLossPreparer(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"failoverGroupName": autorest.Encode("path", failoverGroupName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"serverName":        autorest.Encode("path", serverName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2015-05-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsPost(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/failoverGroups/{failoverGroupName}/forceFailoverAllowDataLoss", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// ForceFailoverAllowDataLossSender sends the ForceFailoverAllowDataLoss request. The method will close the
// http.Response Body if it receives an error.
func (client FailoverGroupsClient) ForceFailoverAllowDataLossSender(req *http.Request) (future FailoverGroupsForceFailoverAllowDataLossFuture, err error) {
	sender := autorest.DecorateSender(client, azure.DoRetryWithRegistration(client.Client))
	future.Future = azure.NewFuture(req)
	future.req = req
	_, err = future.Done(sender)
	if err != nil {
		return
	}
	err = autorest.Respond(future.Response(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted))
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// ForceFailoverAllowDataLossResponder handles the response to the ForceFailoverAllowDataLoss request. The method always
// closes the http.Response Body.
func (client FailoverGroupsClient) ForceFailoverAllowDataLossResponder(resp *http.Response) (result FailoverGroup, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// Get gets a failover group.
//
// resourceGroupName is the name of the resource group that contains the resource. You can obtain this value from
// the Azure Resource Manager API or the portal. serverName is the name of the server containing the failover
// group. failoverGroupName is the name of the failover group.
func (client FailoverGroupsClient) Get(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string) (result FailoverGroup, err error) {
	req, err := client.GetPreparer(ctx, resourceGroupName, serverName, failoverGroupName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "Get", nil, "Failure preparing request")
		return
	}

	resp, err := client.GetSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "Get", resp, "Failure sending request")
		return
	}

	result, err = client.GetResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "Get", resp, "Failure responding to request")
	}

	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// GetPreparer prepares the Get request.
func (client FailoverGroupsClient) GetPreparer(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"failoverGroupName": autorest.Encode("path", failoverGroupName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"serverName":        autorest.Encode("path", serverName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2015-05-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/failoverGroups/{failoverGroupName}", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// GetSender sends the Get request. The method will close the
// http.Response Body if it receives an error.
func (client FailoverGroupsClient) GetSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// GetResponder handles the response to the Get request. The method always
// closes the http.Response Body.
func (client FailoverGroupsClient) GetResponder(resp *http.Response) (result FailoverGroup, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// ListByServer lists the failover groups in a server.
//
// resourceGroupName is the name of the resource group that contains the resource. You can obtain this value from
// the Azure Resource Manager API or the portal. serverName is the name of the server containing the failover
// group.
func (client FailoverGroupsClient) ListByServer(ctx context.Context, resourceGroupName string, serverName string) (result FailoverGroupListResultPage, err error) {
	result.fn = client.listByServerNextResults
	req, err := client.ListByServerPreparer(ctx, resourceGroupName, serverName)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "ListByServer", nil, "Failure preparing request")
		return
	}

	resp, err := client.ListByServerSender(req)
	if err != nil {
		result.fglr.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "ListByServer", resp, "Failure sending request")
		return
	}

	result.fglr, err = client.ListByServerResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "ListByServer", resp, "Failure responding to request")
	}

	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// ListByServerPreparer prepares the ListByServer request.
func (client FailoverGroupsClient) ListByServerPreparer(ctx context.Context, resourceGroupName string, serverName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"serverName":        autorest.Encode("path", serverName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2015-05-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/failoverGroups", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// ListByServerSender sends the ListByServer request. The method will close the
// http.Response Body if it receives an error.
func (client FailoverGroupsClient) ListByServerSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// ListByServerResponder handles the response to the ListByServer request. The method always
// closes the http.Response Body.
func (client FailoverGroupsClient) ListByServerResponder(resp *http.Response) (result FailoverGroupListResult, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// listByServerNextResults retrieves the next set of results, if any.
func (client FailoverGroupsClient) listByServerNextResults(lastResults FailoverGroupListResult) (result FailoverGroupListResult, err error) {
	req, err := lastResults.failoverGroupListResultPreparer()
	if err != nil {
		return result, autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "listByServerNextResults", nil, "Failure preparing next results request")
	}
	if req == nil {
		return
	}
	resp, err := client.ListByServerSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		return result, autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "listByServerNextResults", resp, "Failure sending next results request")
	}
	result, err = client.ListByServerResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "listByServerNextResults", resp, "Failure responding to next results request")
	}
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// ListByServerComplete enumerates all values, automatically crossing page boundaries as required.
func (client FailoverGroupsClient) ListByServerComplete(ctx context.Context, resourceGroupName string, serverName string) (result FailoverGroupListResultIterator, err error) {
	result.page, err = client.ListByServer(ctx, resourceGroupName, serverName)
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// Update updates a failover group.
//
// resourceGroupName is the name of the resource group that contains the resource. You can obtain this value from
// the Azure Resource Manager API or the portal. serverName is the name of the server containing the failover
// group. failoverGroupName is the name of the failover group. parameters is the failover group parameters.
func (client FailoverGroupsClient) Update(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string, parameters FailoverGroupUpdate) (result FailoverGroupsUpdateFuture, err error) {
	req, err := client.UpdatePreparer(ctx, resourceGroupName, serverName, failoverGroupName, parameters)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "Update", nil, "Failure preparing request")
		return
	}

	result, err = client.UpdateSender(req)
	if err != nil {
		err = autorest.NewErrorWithError(err, "sql.FailoverGroupsClient", "Update", result.Response(), "Failure sending request")
		return
	}

	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// UpdatePreparer prepares the Update request.
func (client FailoverGroupsClient) UpdatePreparer(ctx context.Context, resourceGroupName string, serverName string, failoverGroupName string, parameters FailoverGroupUpdate) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"failoverGroupName": autorest.Encode("path", failoverGroupName),
		"resourceGroupName": autorest.Encode("path", resourceGroupName),
		"serverName":        autorest.Encode("path", serverName),
		"subscriptionId":    autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2015-05-01-preview"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsContentType("application/json; charset=utf-8"),
		autorest.AsPatch(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/failoverGroups/{failoverGroupName}", pathParameters),
		autorest.WithJSON(parameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// UpdateSender sends the Update request. The method will close the
// http.Response Body if it receives an error.
func (client FailoverGroupsClient) UpdateSender(req *http.Request) (future FailoverGroupsUpdateFuture, err error) {
	sender := autorest.DecorateSender(client, azure.DoRetryWithRegistration(client.Client))
	future.Future = azure.NewFuture(req)
	future.req = req
	_, err = future.Done(sender)
	if err != nil {
		return
	}
	err = autorest.Respond(future.Response(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted))
	return
}

// Deprecated: Please use package github.com/Azure/azure-sdk-for-go/services/preview/sql/mgmt/2017-03-01-preview/sql instead.
// UpdateResponder handles the response to the Update request. The method always
// closes the http.Response Body.
func (client FailoverGroupsClient) UpdateResponder(resp *http.Response) (result FailoverGroup, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK, http.StatusAccepted),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}
