// +build go1.9

// Copyright 2019 Microsoft Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// This code was auto-generated by:
// github.com/Azure/azure-sdk-for-go/tools/profileBuilder

package resourcegraph

import (
	"context"

	original "github.com/Azure/azure-sdk-for-go/services/preview/resourcegraph/mgmt/2018-09-01/resourcegraph"
)

const (
	DefaultBaseURI = original.DefaultBaseURI
)

type ColumnDataType = original.ColumnDataType

const (
	Boolean ColumnDataType = original.Boolean
	Integer ColumnDataType = original.Integer
	Number  ColumnDataType = original.Number
	Object  ColumnDataType = original.Object
	String  ColumnDataType = original.String
)

type FacetSortOrder = original.FacetSortOrder

const (
	Asc  FacetSortOrder = original.Asc
	Desc FacetSortOrder = original.Desc
)

type ResultKind = original.ResultKind

const (
	Basic ResultKind = original.Basic
)

type ResultTruncated = original.ResultTruncated

const (
	False ResultTruncated = original.False
	True  ResultTruncated = original.True
)

type ResultType = original.ResultType

const (
	ResultTypeFacet       ResultType = original.ResultTypeFacet
	ResultTypeFacetError  ResultType = original.ResultTypeFacetError
	ResultTypeFacetResult ResultType = original.ResultTypeFacetResult
)

type BaseClient = original.BaseClient
type BasicFacet = original.BasicFacet
type Column = original.Column
type DateTimeInterval = original.DateTimeInterval
type Error = original.Error
type ErrorDetails = original.ErrorDetails
type ErrorFieldContract = original.ErrorFieldContract
type ErrorResponse = original.ErrorResponse
type Facet = original.Facet
type FacetError = original.FacetError
type FacetRequest = original.FacetRequest
type FacetRequestOptions = original.FacetRequestOptions
type FacetResult = original.FacetResult
type GraphQueryClient = original.GraphQueryClient
type GraphQueryError = original.GraphQueryError
type GraphQueryListResult = original.GraphQueryListResult
type GraphQueryListResultIterator = original.GraphQueryListResultIterator
type GraphQueryListResultPage = original.GraphQueryListResultPage
type GraphQueryProperties = original.GraphQueryProperties
type GraphQueryPropertiesUpdateParameters = original.GraphQueryPropertiesUpdateParameters
type GraphQueryResource = original.GraphQueryResource
type GraphQueryUpdateParameters = original.GraphQueryUpdateParameters
type Operation = original.Operation
type OperationDisplay = original.OperationDisplay
type OperationListResult = original.OperationListResult
type OperationListResultIterator = original.OperationListResultIterator
type OperationListResultPage = original.OperationListResultPage
type OperationsClient = original.OperationsClient
type QueryRequest = original.QueryRequest
type QueryRequestOptions = original.QueryRequestOptions
type QueryResponse = original.QueryResponse
type Resource = original.Resource
type ResourceChangeData = original.ResourceChangeData
type ResourceChangeDataAfterSnapshot = original.ResourceChangeDataAfterSnapshot
type ResourceChangeDataBeforeSnapshot = original.ResourceChangeDataBeforeSnapshot
type ResourceChangeDetailsRequestParameters = original.ResourceChangeDetailsRequestParameters
type ResourceChangeList = original.ResourceChangeList
type ResourceChangesRequestParameters = original.ResourceChangesRequestParameters
type ResourceChangesRequestParametersInterval = original.ResourceChangesRequestParametersInterval
type ResourceSnapshotData = original.ResourceSnapshotData
type Table = original.Table

func New(subscriptionID string) BaseClient {
	return original.New(subscriptionID)
}
func NewGraphQueryClient(subscriptionID string) GraphQueryClient {
	return original.NewGraphQueryClient(subscriptionID)
}
func NewGraphQueryClientWithBaseURI(baseURI string, subscriptionID string) GraphQueryClient {
	return original.NewGraphQueryClientWithBaseURI(baseURI, subscriptionID)
}
func NewGraphQueryListResultIterator(page GraphQueryListResultPage) GraphQueryListResultIterator {
	return original.NewGraphQueryListResultIterator(page)
}
func NewGraphQueryListResultPage(getNextPage func(context.Context, GraphQueryListResult) (GraphQueryListResult, error)) GraphQueryListResultPage {
	return original.NewGraphQueryListResultPage(getNextPage)
}
func NewOperationListResultIterator(page OperationListResultPage) OperationListResultIterator {
	return original.NewOperationListResultIterator(page)
}
func NewOperationListResultPage(getNextPage func(context.Context, OperationListResult) (OperationListResult, error)) OperationListResultPage {
	return original.NewOperationListResultPage(getNextPage)
}
func NewOperationsClient(subscriptionID string) OperationsClient {
	return original.NewOperationsClient(subscriptionID)
}
func NewOperationsClientWithBaseURI(baseURI string, subscriptionID string) OperationsClient {
	return original.NewOperationsClientWithBaseURI(baseURI, subscriptionID)
}
func NewWithBaseURI(baseURI string, subscriptionID string) BaseClient {
	return original.NewWithBaseURI(baseURI, subscriptionID)
}
func PossibleColumnDataTypeValues() []ColumnDataType {
	return original.PossibleColumnDataTypeValues()
}
func PossibleFacetSortOrderValues() []FacetSortOrder {
	return original.PossibleFacetSortOrderValues()
}
func PossibleResultKindValues() []ResultKind {
	return original.PossibleResultKindValues()
}
func PossibleResultTruncatedValues() []ResultTruncated {
	return original.PossibleResultTruncatedValues()
}
func PossibleResultTypeValues() []ResultType {
	return original.PossibleResultTypeValues()
}
func UserAgent() string {
	return original.UserAgent() + " profiles/preview"
}
func Version() string {
	return original.Version()
}
