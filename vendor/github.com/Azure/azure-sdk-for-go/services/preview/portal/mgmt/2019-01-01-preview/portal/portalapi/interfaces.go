package portalapi

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
	"github.com/Azure/azure-sdk-for-go/services/preview/portal/mgmt/2019-01-01-preview/portal"
	"github.com/Azure/go-autorest/autorest"
)

// OperationsClientAPI contains the set of methods on the OperationsClient type.
type OperationsClientAPI interface {
	List(ctx context.Context) (result portal.ResourceProviderOperationListPage, err error)
}

var _ OperationsClientAPI = (*portal.OperationsClient)(nil)

// DashboardsClientAPI contains the set of methods on the DashboardsClient type.
type DashboardsClientAPI interface {
	CreateOrUpdate(ctx context.Context, resourceGroupName string, dashboardName string, dashboard portal.Dashboard) (result portal.Dashboard, err error)
	Delete(ctx context.Context, resourceGroupName string, dashboardName string) (result autorest.Response, err error)
	Get(ctx context.Context, resourceGroupName string, dashboardName string) (result portal.Dashboard, err error)
	ListByResourceGroup(ctx context.Context, resourceGroupName string) (result portal.DashboardListResultPage, err error)
	ListBySubscription(ctx context.Context) (result portal.DashboardListResultPage, err error)
	Update(ctx context.Context, resourceGroupName string, dashboardName string, dashboard portal.PatchableDashboard) (result portal.Dashboard, err error)
}

var _ DashboardsClientAPI = (*portal.DashboardsClient)(nil)
