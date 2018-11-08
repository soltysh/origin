package servicebus

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

// RegionsClient is the azure Service Bus client
type RegionsClient struct {
	BaseClient
}

// NewRegionsClient creates an instance of the RegionsClient client.
func NewRegionsClient(subscriptionID string) RegionsClient {
	return NewRegionsClientWithBaseURI(DefaultBaseURI, subscriptionID)
}

// NewRegionsClientWithBaseURI creates an instance of the RegionsClient client.
func NewRegionsClientWithBaseURI(baseURI string, subscriptionID string) RegionsClient {
	return RegionsClient{NewWithBaseURI(baseURI, subscriptionID)}
}

// ListBySku gets the available Regions for a given sku
// Parameters:
// sku - the sku type.
func (client RegionsClient) ListBySku(ctx context.Context, sku string) (result PremiumMessagingRegionsListResultPage, err error) {
	if err := validation.Validate([]validation.Validation{
		{TargetValue: sku,
			Constraints: []validation.Constraint{{Target: "sku", Name: validation.MaxLength, Rule: 50, Chain: nil},
				{Target: "sku", Name: validation.MinLength, Rule: 1, Chain: nil}}}}); err != nil {
		return result, validation.NewError("servicebus.RegionsClient", "ListBySku", err.Error())
	}

	result.fn = client.listBySkuNextResults
	req, err := client.ListBySkuPreparer(ctx, sku)
	if err != nil {
		err = autorest.NewErrorWithError(err, "servicebus.RegionsClient", "ListBySku", nil, "Failure preparing request")
		return
	}

	resp, err := client.ListBySkuSender(req)
	if err != nil {
		result.pmrlr.Response = autorest.Response{Response: resp}
		err = autorest.NewErrorWithError(err, "servicebus.RegionsClient", "ListBySku", resp, "Failure sending request")
		return
	}

	result.pmrlr, err = client.ListBySkuResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "servicebus.RegionsClient", "ListBySku", resp, "Failure responding to request")
	}

	return
}

// ListBySkuPreparer prepares the ListBySku request.
func (client RegionsClient) ListBySkuPreparer(ctx context.Context, sku string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"sku":            autorest.Encode("path", sku),
		"subscriptionId": autorest.Encode("path", client.SubscriptionID),
	}

	const APIVersion = "2017-04-01"
	queryParameters := map[string]interface{}{
		"api-version": APIVersion,
	}

	preparer := autorest.CreatePreparer(
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseURI),
		autorest.WithPathParameters("/subscriptions/{subscriptionId}/providers/Microsoft.ServiceBus/sku/{sku}/regions", pathParameters),
		autorest.WithQueryParameters(queryParameters))
	return preparer.Prepare((&http.Request{}).WithContext(ctx))
}

// ListBySkuSender sends the ListBySku request. The method will close the
// http.Response Body if it receives an error.
func (client RegionsClient) ListBySkuSender(req *http.Request) (*http.Response, error) {
	return autorest.SendWithSender(client, req,
		azure.DoRetryWithRegistration(client.Client))
}

// ListBySkuResponder handles the response to the ListBySku request. The method always
// closes the http.Response Body.
func (client RegionsClient) ListBySkuResponder(resp *http.Response) (result PremiumMessagingRegionsListResult, err error) {
	err = autorest.Respond(
		resp,
		client.ByInspecting(),
		azure.WithErrorUnlessStatusCode(http.StatusOK),
		autorest.ByUnmarshallingJSON(&result),
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}
	return
}

// listBySkuNextResults retrieves the next set of results, if any.
func (client RegionsClient) listBySkuNextResults(lastResults PremiumMessagingRegionsListResult) (result PremiumMessagingRegionsListResult, err error) {
	req, err := lastResults.premiumMessagingRegionsListResultPreparer()
	if err != nil {
		return result, autorest.NewErrorWithError(err, "servicebus.RegionsClient", "listBySkuNextResults", nil, "Failure preparing next results request")
	}
	if req == nil {
		return
	}
	resp, err := client.ListBySkuSender(req)
	if err != nil {
		result.Response = autorest.Response{Response: resp}
		return result, autorest.NewErrorWithError(err, "servicebus.RegionsClient", "listBySkuNextResults", resp, "Failure sending next results request")
	}
	result, err = client.ListBySkuResponder(resp)
	if err != nil {
		err = autorest.NewErrorWithError(err, "servicebus.RegionsClient", "listBySkuNextResults", resp, "Failure responding to next results request")
	}
	return
}

// ListBySkuComplete enumerates all values, automatically crossing page boundaries as required.
func (client RegionsClient) ListBySkuComplete(ctx context.Context, sku string) (result PremiumMessagingRegionsListResultIterator, err error) {
	result.page, err = client.ListBySku(ctx, sku)
	return
}
