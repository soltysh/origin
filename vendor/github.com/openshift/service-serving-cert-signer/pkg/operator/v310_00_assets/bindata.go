// Code generated by go-bindata.
// sources:
// bindata/v3.10.0/apiservice-cabundle-controller/clusterrole.yaml
// bindata/v3.10.0/apiservice-cabundle-controller/clusterrolebinding.yaml
// bindata/v3.10.0/apiservice-cabundle-controller/cm.yaml
// bindata/v3.10.0/apiservice-cabundle-controller/defaultconfig.yaml
// bindata/v3.10.0/apiservice-cabundle-controller/deployment.yaml
// bindata/v3.10.0/apiservice-cabundle-controller/ns.yaml
// bindata/v3.10.0/apiservice-cabundle-controller/sa.yaml
// bindata/v3.10.0/apiservice-cabundle-controller/signing-cabundle.yaml
// bindata/v3.10.0/apiservice-cabundle-controller/svc.yaml
// bindata/v3.10.0/configmap-cabundle-controller/clusterrole.yaml
// bindata/v3.10.0/configmap-cabundle-controller/clusterrolebinding.yaml
// bindata/v3.10.0/configmap-cabundle-controller/cm.yaml
// bindata/v3.10.0/configmap-cabundle-controller/defaultconfig.yaml
// bindata/v3.10.0/configmap-cabundle-controller/deployment.yaml
// bindata/v3.10.0/configmap-cabundle-controller/ns.yaml
// bindata/v3.10.0/configmap-cabundle-controller/sa.yaml
// bindata/v3.10.0/configmap-cabundle-controller/signing-cabundle.yaml
// bindata/v3.10.0/configmap-cabundle-controller/svc.yaml
// bindata/v3.10.0/service-serving-cert-signer-controller/clusterrole.yaml
// bindata/v3.10.0/service-serving-cert-signer-controller/clusterrolebinding.yaml
// bindata/v3.10.0/service-serving-cert-signer-controller/cm.yaml
// bindata/v3.10.0/service-serving-cert-signer-controller/defaultconfig.yaml
// bindata/v3.10.0/service-serving-cert-signer-controller/deployment.yaml
// bindata/v3.10.0/service-serving-cert-signer-controller/ns.yaml
// bindata/v3.10.0/service-serving-cert-signer-controller/sa.yaml
// bindata/v3.10.0/service-serving-cert-signer-controller/signing-secret.yaml
// bindata/v3.10.0/service-serving-cert-signer-controller/svc.yaml
// DO NOT EDIT!

package v310_00_assets

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"time"
)
type asset struct {
	bytes []byte
	info  os.FileInfo
}

type bindataFileInfo struct {
	name    string
	size    int64
	mode    os.FileMode
	modTime time.Time
}

func (fi bindataFileInfo) Name() string {
	return fi.name
}
func (fi bindataFileInfo) Size() int64 {
	return fi.size
}
func (fi bindataFileInfo) Mode() os.FileMode {
	return fi.mode
}
func (fi bindataFileInfo) ModTime() time.Time {
	return fi.modTime
}
func (fi bindataFileInfo) IsDir() bool {
	return false
}
func (fi bindataFileInfo) Sys() interface{} {
	return nil
}

var _v3100ApiserviceCabundleControllerClusterroleYaml = []byte(`apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:openshift:controller:apiservice-cabundle-injector
rules:
- apiGroups:
  - apiregistration.k8s.io
  resources:
  - apiservices
  verbs:
  - get
  - list
  - watch
  - update
  - patch
`)

func v3100ApiserviceCabundleControllerClusterroleYamlBytes() ([]byte, error) {
	return _v3100ApiserviceCabundleControllerClusterroleYaml, nil
}

func v3100ApiserviceCabundleControllerClusterroleYaml() (*asset, error) {
	bytes, err := v3100ApiserviceCabundleControllerClusterroleYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/apiservice-cabundle-controller/clusterrole.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ApiserviceCabundleControllerClusterrolebindingYaml = []byte(`apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: system:openshift:controller:apiservice-cabundle-injector
roleRef:
  kind: ClusterRole
  name: system:openshift:controller:apiservice-cabundle-injector
subjects:
- kind: ServiceAccount
  namespace: openshift-service-cert-signer
  name: apiservice-cabundle-injector-sa
`)

func v3100ApiserviceCabundleControllerClusterrolebindingYamlBytes() ([]byte, error) {
	return _v3100ApiserviceCabundleControllerClusterrolebindingYaml, nil
}

func v3100ApiserviceCabundleControllerClusterrolebindingYaml() (*asset, error) {
	bytes, err := v3100ApiserviceCabundleControllerClusterrolebindingYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/apiservice-cabundle-controller/clusterrolebinding.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ApiserviceCabundleControllerCmYaml = []byte(`apiVersion: v1
kind: ConfigMap
metadata:
  namespace: openshift-service-cert-signer
  name: apiservice-cabundle-injector-config
data:
  controller-config.yaml:
`)

func v3100ApiserviceCabundleControllerCmYamlBytes() ([]byte, error) {
	return _v3100ApiserviceCabundleControllerCmYaml, nil
}

func v3100ApiserviceCabundleControllerCmYaml() (*asset, error) {
	bytes, err := v3100ApiserviceCabundleControllerCmYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/apiservice-cabundle-controller/cm.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ApiserviceCabundleControllerDefaultconfigYaml = []byte(`apiVersion: servicecertsigner.config.openshift.io/v1alpha1
kind: APIServiceCABundleInjectorConfig
caBundleFile: /var/run/configmaps/signing-cabundle/cabundle.crt
`)

func v3100ApiserviceCabundleControllerDefaultconfigYamlBytes() ([]byte, error) {
	return _v3100ApiserviceCabundleControllerDefaultconfigYaml, nil
}

func v3100ApiserviceCabundleControllerDefaultconfigYaml() (*asset, error) {
	bytes, err := v3100ApiserviceCabundleControllerDefaultconfigYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/apiservice-cabundle-controller/defaultconfig.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ApiserviceCabundleControllerDeploymentYaml = []byte(`apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: openshift-service-cert-signer
  name: apiservice-cabundle-injector
  labels:
    app: openshift-apiservice-cabundle-injector
    apiservice-cabundle-injector: "true"
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: openshift-apiservice-cabundle-injector
      apiservice-cabundle-injector: "true"
  template:
    metadata:
      name: apiservice-cabundle-injector
      labels:
        app: openshift-apiservice-cabundle-injector
        apiservice-cabundle-injector: "true"
    spec:
      serviceAccountName: apiservice-cabundle-injector-sa
      containers:
      - name: apiservice-cabundle-injector-controller
        image: ${IMAGE}
        imagePullPolicy: IfNotPresent
        command: ["service-serving-cert-signer", "apiservice-cabundle-injector"]
        args:
        - "--config=/var/run/configmaps/config/controller-config.yaml"
        ports:
        - containerPort: 8443
        volumeMounts:
        - mountPath: /var/run/configmaps/config
          name: config
        - mountPath: /var/run/configmaps/signing-cabundle
          name: signing-cabundle
        - mountPath: /var/run/secrets/serving-cert
          name: serving-cert
      volumes:
      - name: serving-cert
        secret:
          secretName: apiservice-cabundle-injector-serving-cert
          optional: true
      - name: signing-cabundle
        configMap:
          name: signing-cabundle
      - name: config
        configMap:
          name: apiservice-cabundle-injector-config
      nodeSelector:
        node-role.kubernetes.io/master: ""
      tolerations:
      - operator: Exists
`)

func v3100ApiserviceCabundleControllerDeploymentYamlBytes() ([]byte, error) {
	return _v3100ApiserviceCabundleControllerDeploymentYaml, nil
}

func v3100ApiserviceCabundleControllerDeploymentYaml() (*asset, error) {
	bytes, err := v3100ApiserviceCabundleControllerDeploymentYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/apiservice-cabundle-controller/deployment.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ApiserviceCabundleControllerNsYaml = []byte(`apiVersion: v1
kind: Namespace
metadata:
  name: openshift-service-cert-signer
  labels:
    openshift.io/run-level: "1"`)

func v3100ApiserviceCabundleControllerNsYamlBytes() ([]byte, error) {
	return _v3100ApiserviceCabundleControllerNsYaml, nil
}

func v3100ApiserviceCabundleControllerNsYaml() (*asset, error) {
	bytes, err := v3100ApiserviceCabundleControllerNsYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/apiservice-cabundle-controller/ns.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ApiserviceCabundleControllerSaYaml = []byte(`apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: openshift-service-cert-signer
  name: apiservice-cabundle-injector-sa
`)

func v3100ApiserviceCabundleControllerSaYamlBytes() ([]byte, error) {
	return _v3100ApiserviceCabundleControllerSaYaml, nil
}

func v3100ApiserviceCabundleControllerSaYaml() (*asset, error) {
	bytes, err := v3100ApiserviceCabundleControllerSaYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/apiservice-cabundle-controller/sa.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ApiserviceCabundleControllerSigningCabundleYaml = []byte(`apiVersion: v1
kind: ConfigMap
metadata:
  namespace: openshift-service-cert-signer
  name: signing-cabundle
data:
  cabundle.crt:
`)

func v3100ApiserviceCabundleControllerSigningCabundleYamlBytes() ([]byte, error) {
	return _v3100ApiserviceCabundleControllerSigningCabundleYaml, nil
}

func v3100ApiserviceCabundleControllerSigningCabundleYaml() (*asset, error) {
	bytes, err := v3100ApiserviceCabundleControllerSigningCabundleYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/apiservice-cabundle-controller/signing-cabundle.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ApiserviceCabundleControllerSvcYaml = []byte(`apiVersion: v1
kind: Service
metadata:
  namespace: openshift-service-cert-signer
  name: service-serving-cert-signer
  annotations:
    service.alpha.openshift.io/serving-cert-secret-name: service-serving-cert-signer-serving-cert
    prometheus.io/scrape: "true"
    prometheus.io/scheme: https
spec:
  selector:
    service-serving-cert-signer: "true"
  ports:
  - name: https
    port: 443
    targetPort: 8443
`)

func v3100ApiserviceCabundleControllerSvcYamlBytes() ([]byte, error) {
	return _v3100ApiserviceCabundleControllerSvcYaml, nil
}

func v3100ApiserviceCabundleControllerSvcYaml() (*asset, error) {
	bytes, err := v3100ApiserviceCabundleControllerSvcYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/apiservice-cabundle-controller/svc.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ConfigmapCabundleControllerClusterroleYaml = []byte(`apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:openshift:controller:configmap-cabundle-injector
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  verbs:
  - get
  - list
  - watch
  - update
`)

func v3100ConfigmapCabundleControllerClusterroleYamlBytes() ([]byte, error) {
	return _v3100ConfigmapCabundleControllerClusterroleYaml, nil
}

func v3100ConfigmapCabundleControllerClusterroleYaml() (*asset, error) {
	bytes, err := v3100ConfigmapCabundleControllerClusterroleYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/configmap-cabundle-controller/clusterrole.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ConfigmapCabundleControllerClusterrolebindingYaml = []byte(`apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: system:openshift:controller:configmap-cabundle-injector
roleRef:
  kind: ClusterRole
  name: system:openshift:controller:configmap-cabundle-injector
subjects:
- kind: ServiceAccount
  namespace: openshift-service-cert-signer
  name: configmap-cabundle-injector-sa
`)

func v3100ConfigmapCabundleControllerClusterrolebindingYamlBytes() ([]byte, error) {
	return _v3100ConfigmapCabundleControllerClusterrolebindingYaml, nil
}

func v3100ConfigmapCabundleControllerClusterrolebindingYaml() (*asset, error) {
	bytes, err := v3100ConfigmapCabundleControllerClusterrolebindingYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/configmap-cabundle-controller/clusterrolebinding.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ConfigmapCabundleControllerCmYaml = []byte(`apiVersion: v1
kind: ConfigMap
metadata:
  namespace: openshift-service-cert-signer
  name: configmap-cabundle-injector-config
data:
  controller-config.yaml:
`)

func v3100ConfigmapCabundleControllerCmYamlBytes() ([]byte, error) {
	return _v3100ConfigmapCabundleControllerCmYaml, nil
}

func v3100ConfigmapCabundleControllerCmYaml() (*asset, error) {
	bytes, err := v3100ConfigmapCabundleControllerCmYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/configmap-cabundle-controller/cm.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ConfigmapCabundleControllerDefaultconfigYaml = []byte(`apiVersion: servicecertsigner.config.openshift.io/v1alpha1
kind: ConfigMapCABundleInjectorConfig
caBundleFile: /var/run/configmaps/signing-cabundle/cabundle.crt
`)

func v3100ConfigmapCabundleControllerDefaultconfigYamlBytes() ([]byte, error) {
	return _v3100ConfigmapCabundleControllerDefaultconfigYaml, nil
}

func v3100ConfigmapCabundleControllerDefaultconfigYaml() (*asset, error) {
	bytes, err := v3100ConfigmapCabundleControllerDefaultconfigYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/configmap-cabundle-controller/defaultconfig.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ConfigmapCabundleControllerDeploymentYaml = []byte(`apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: openshift-service-cert-signer
  name: configmap-cabundle-injector
  labels:
    app: openshift-configmap-cabundle-injector
    configmap-cabundle-injector: "true"
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: openshift-configmap-cabundle-injector
      configmap-cabundle-injector: "true"
  template:
    metadata:
      name: configmap-cabundle-injector
      labels:
        app: openshift-configmap-cabundle-injector
        configmap-cabundle-injector: "true"
    spec:
      serviceAccountName: configmap-cabundle-injector-sa
      containers:
      - name: configmap-cabundle-injector-controller
        image: ${IMAGE}
        imagePullPolicy: IfNotPresent
        command: ["service-serving-cert-signer", "configmap-cabundle-injector"]
        args:
        - "--config=/var/run/configmaps/config/controller-config.yaml"
        ports:
        - containerPort: 8443
        volumeMounts:
        - mountPath: /var/run/configmaps/config
          name: config
        - mountPath: /var/run/configmaps/signing-cabundle
          name: signing-cabundle
        - mountPath: /var/run/secrets/serving-cert
          name: serving-cert
      volumes:
      - name: serving-cert
        secret:
          secretName: configmap-cabundle-injector-serving-cert
          optional: true
      - name: signing-cabundle
        configMap:
          name: signing-cabundle
      - name: config
        configMap:
          name: configmap-cabundle-injector-config



`)

func v3100ConfigmapCabundleControllerDeploymentYamlBytes() ([]byte, error) {
	return _v3100ConfigmapCabundleControllerDeploymentYaml, nil
}

func v3100ConfigmapCabundleControllerDeploymentYaml() (*asset, error) {
	bytes, err := v3100ConfigmapCabundleControllerDeploymentYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/configmap-cabundle-controller/deployment.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ConfigmapCabundleControllerNsYaml = []byte(`apiVersion: v1
kind: Namespace
metadata:
  name: openshift-service-cert-signer
  labels:
    openshift.io/run-level: "1"
`)

func v3100ConfigmapCabundleControllerNsYamlBytes() ([]byte, error) {
	return _v3100ConfigmapCabundleControllerNsYaml, nil
}

func v3100ConfigmapCabundleControllerNsYaml() (*asset, error) {
	bytes, err := v3100ConfigmapCabundleControllerNsYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/configmap-cabundle-controller/ns.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ConfigmapCabundleControllerSaYaml = []byte(`apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: openshift-service-cert-signer
  name: configmap-cabundle-injector-sa
`)

func v3100ConfigmapCabundleControllerSaYamlBytes() ([]byte, error) {
	return _v3100ConfigmapCabundleControllerSaYaml, nil
}

func v3100ConfigmapCabundleControllerSaYaml() (*asset, error) {
	bytes, err := v3100ConfigmapCabundleControllerSaYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/configmap-cabundle-controller/sa.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ConfigmapCabundleControllerSigningCabundleYaml = []byte(`apiVersion: v1
kind: ConfigMap
metadata:
  namespace: openshift-service-cert-signer
  name: signing-cabundle
data:
  cabundle.crt:
`)

func v3100ConfigmapCabundleControllerSigningCabundleYamlBytes() ([]byte, error) {
	return _v3100ConfigmapCabundleControllerSigningCabundleYaml, nil
}

func v3100ConfigmapCabundleControllerSigningCabundleYaml() (*asset, error) {
	bytes, err := v3100ConfigmapCabundleControllerSigningCabundleYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/configmap-cabundle-controller/signing-cabundle.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ConfigmapCabundleControllerSvcYaml = []byte(`apiVersion: v1
kind: Service
metadata:
  namespace: openshift-service-cert-signer
  name: service-serving-cert-signer
  annotations:
    service.alpha.openshift.io/serving-cert-secret-name: service-serving-cert-signer-serving-cert
    prometheus.io/scrape: "true"
    prometheus.io/scheme: https
spec:
  selector:
    service-serving-cert-signer: "true"
  ports:
  - name: https
    port: 443
    targetPort: 8443
`)

func v3100ConfigmapCabundleControllerSvcYamlBytes() ([]byte, error) {
	return _v3100ConfigmapCabundleControllerSvcYaml, nil
}

func v3100ConfigmapCabundleControllerSvcYaml() (*asset, error) {
	bytes, err := v3100ConfigmapCabundleControllerSvcYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/configmap-cabundle-controller/svc.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ServiceServingCertSignerControllerClusterroleYaml = []byte(`apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:openshift:controller:service-serving-cert-signer
rules:
- apiGroups:
  - ""
  resources:
  - secrets
  verbs:
  - get
  - list
  - watch
  - create
  - update
  - patch
  - delete
  - deletecollection
- apiGroups:
  - ""
  resources:
  - services
  verbs:
  - get
  - list
  - watch
  - update
  - patch
`)

func v3100ServiceServingCertSignerControllerClusterroleYamlBytes() ([]byte, error) {
	return _v3100ServiceServingCertSignerControllerClusterroleYaml, nil
}

func v3100ServiceServingCertSignerControllerClusterroleYaml() (*asset, error) {
	bytes, err := v3100ServiceServingCertSignerControllerClusterroleYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/service-serving-cert-signer-controller/clusterrole.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ServiceServingCertSignerControllerClusterrolebindingYaml = []byte(`apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: system:openshift:controller:service-serving-cert-signer
roleRef:
  kind: ClusterRole
  name: system:openshift:controller:service-serving-cert-signer
subjects:
- kind: ServiceAccount
  namespace: openshift-service-cert-signer
  name: service-serving-cert-signer-sa
`)

func v3100ServiceServingCertSignerControllerClusterrolebindingYamlBytes() ([]byte, error) {
	return _v3100ServiceServingCertSignerControllerClusterrolebindingYaml, nil
}

func v3100ServiceServingCertSignerControllerClusterrolebindingYaml() (*asset, error) {
	bytes, err := v3100ServiceServingCertSignerControllerClusterrolebindingYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/service-serving-cert-signer-controller/clusterrolebinding.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ServiceServingCertSignerControllerCmYaml = []byte(`apiVersion: v1
kind: ConfigMap
metadata:
  namespace: openshift-service-cert-signer
  name: service-serving-cert-signer-config
data:
  controller-config.yaml:
`)

func v3100ServiceServingCertSignerControllerCmYamlBytes() ([]byte, error) {
	return _v3100ServiceServingCertSignerControllerCmYaml, nil
}

func v3100ServiceServingCertSignerControllerCmYaml() (*asset, error) {
	bytes, err := v3100ServiceServingCertSignerControllerCmYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/service-serving-cert-signer-controller/cm.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ServiceServingCertSignerControllerDefaultconfigYaml = []byte(`apiVersion: servicecertsigner.config.openshift.io/v1alpha1
kind: ServiceServingCertSignerConfig
signer:
  certFile: /var/run/secrets/signing-key/tls.crt
  keyFile: /var/run/secrets/signing-key/tls.key
`)

func v3100ServiceServingCertSignerControllerDefaultconfigYamlBytes() ([]byte, error) {
	return _v3100ServiceServingCertSignerControllerDefaultconfigYaml, nil
}

func v3100ServiceServingCertSignerControllerDefaultconfigYaml() (*asset, error) {
	bytes, err := v3100ServiceServingCertSignerControllerDefaultconfigYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/service-serving-cert-signer-controller/defaultconfig.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ServiceServingCertSignerControllerDeploymentYaml = []byte(`apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: openshift-service-cert-signer
  name: service-serving-cert-signer
  labels:
    app: openshift-service-serving-cert-signer
    service-serving-cert-signer: "true"
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: openshift-service-serving-cert-signer
      service-serving-cert-signer: "true"
  template:
    metadata:
      name: service-serving-cert-signer
      labels:
        app: openshift-service-serving-cert-signer
        service-serving-cert-signer: "true"
    spec:
      serviceAccountName: service-serving-cert-signer-sa
      containers:
      - name: service-serving-cert-signer-controller
        image: ${IMAGE}
        imagePullPolicy: IfNotPresent
        command: ["service-serving-cert-signer", "serving-cert-signer"]
        args:
        - "--config=/var/run/configmaps/config/controller-config.yaml"
        ports:
        - containerPort: 8443
        volumeMounts:
        - mountPath: /var/run/configmaps/config
          name: config
        - mountPath: /var/run/secrets/signing-key
          name: signing-key
        - mountPath: /var/run/secrets/serving-cert
          name: serving-cert
      volumes:
      - name: serving-cert
        secret:
          secretName: service-serving-cert-signer-serving-cert
          optional: true
      - name: signing-key
        secret:
          secretName: service-serving-cert-signer-signing-key
      - name: config
        configMap:
          name: service-serving-cert-signer-config
      nodeSelector:
        node-role.kubernetes.io/master: ""
      tolerations:
      - operator: Exists
`)

func v3100ServiceServingCertSignerControllerDeploymentYamlBytes() ([]byte, error) {
	return _v3100ServiceServingCertSignerControllerDeploymentYaml, nil
}

func v3100ServiceServingCertSignerControllerDeploymentYaml() (*asset, error) {
	bytes, err := v3100ServiceServingCertSignerControllerDeploymentYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/service-serving-cert-signer-controller/deployment.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ServiceServingCertSignerControllerNsYaml = []byte(`apiVersion: v1
kind: Namespace
metadata:
  name: openshift-service-cert-signer
  labels:
    openshift.io/run-level: "1"`)

func v3100ServiceServingCertSignerControllerNsYamlBytes() ([]byte, error) {
	return _v3100ServiceServingCertSignerControllerNsYaml, nil
}

func v3100ServiceServingCertSignerControllerNsYaml() (*asset, error) {
	bytes, err := v3100ServiceServingCertSignerControllerNsYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/service-serving-cert-signer-controller/ns.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ServiceServingCertSignerControllerSaYaml = []byte(`apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: openshift-service-cert-signer
  name: service-serving-cert-signer-sa
`)

func v3100ServiceServingCertSignerControllerSaYamlBytes() ([]byte, error) {
	return _v3100ServiceServingCertSignerControllerSaYaml, nil
}

func v3100ServiceServingCertSignerControllerSaYaml() (*asset, error) {
	bytes, err := v3100ServiceServingCertSignerControllerSaYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/service-serving-cert-signer-controller/sa.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ServiceServingCertSignerControllerSigningSecretYaml = []byte(`apiVersion: v1
kind: Secret
metadata:
  namespace: openshift-service-cert-signer
  name: service-serving-cert-signer-signing-key
type: kubernetes.io/tls
data:
  tls.crt:
  tls.key:
`)

func v3100ServiceServingCertSignerControllerSigningSecretYamlBytes() ([]byte, error) {
	return _v3100ServiceServingCertSignerControllerSigningSecretYaml, nil
}

func v3100ServiceServingCertSignerControllerSigningSecretYaml() (*asset, error) {
	bytes, err := v3100ServiceServingCertSignerControllerSigningSecretYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/service-serving-cert-signer-controller/signing-secret.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

var _v3100ServiceServingCertSignerControllerSvcYaml = []byte(`apiVersion: v1
kind: Service
metadata:
  namespace: openshift-service-cert-signer
  name: service-serving-cert-signer
  annotations:
    service.alpha.openshift.io/serving-cert-secret-name: service-serving-cert-signer-serving-cert
    prometheus.io/scrape: "true"
    prometheus.io/scheme: https
spec:
  selector:
    service-serving-cert-signer: "true"
  ports:
  - name: https
    port: 443
    targetPort: 8443
`)

func v3100ServiceServingCertSignerControllerSvcYamlBytes() ([]byte, error) {
	return _v3100ServiceServingCertSignerControllerSvcYaml, nil
}

func v3100ServiceServingCertSignerControllerSvcYaml() (*asset, error) {
	bytes, err := v3100ServiceServingCertSignerControllerSvcYamlBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "v3.10.0/service-serving-cert-signer-controller/svc.yaml", size: 0, mode: os.FileMode(0), modTime: time.Unix(0, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

// Asset loads and returns the asset for the given name.
// It returns an error if the asset could not be found or
// could not be loaded.
func Asset(name string) ([]byte, error) {
	cannonicalName := strings.Replace(name, "\\", "/", -1)
	if f, ok := _bindata[cannonicalName]; ok {
		a, err := f()
		if err != nil {
			return nil, fmt.Errorf("Asset %s can't read by error: %v", name, err)
		}
		return a.bytes, nil
	}
	return nil, fmt.Errorf("Asset %s not found", name)
}

// MustAsset is like Asset but panics when Asset would return an error.
// It simplifies safe initialization of global variables.
func MustAsset(name string) []byte {
	a, err := Asset(name)
	if err != nil {
		panic("asset: Asset(" + name + "): " + err.Error())
	}

	return a
}

// AssetInfo loads and returns the asset info for the given name.
// It returns an error if the asset could not be found or
// could not be loaded.
func AssetInfo(name string) (os.FileInfo, error) {
	cannonicalName := strings.Replace(name, "\\", "/", -1)
	if f, ok := _bindata[cannonicalName]; ok {
		a, err := f()
		if err != nil {
			return nil, fmt.Errorf("AssetInfo %s can't read by error: %v", name, err)
		}
		return a.info, nil
	}
	return nil, fmt.Errorf("AssetInfo %s not found", name)
}

// AssetNames returns the names of the assets.
func AssetNames() []string {
	names := make([]string, 0, len(_bindata))
	for name := range _bindata {
		names = append(names, name)
	}
	return names
}

// _bindata is a table, holding each asset generator, mapped to its name.
var _bindata = map[string]func() (*asset, error){
	"v3.10.0/apiservice-cabundle-controller/clusterrole.yaml": v3100ApiserviceCabundleControllerClusterroleYaml,
	"v3.10.0/apiservice-cabundle-controller/clusterrolebinding.yaml": v3100ApiserviceCabundleControllerClusterrolebindingYaml,
	"v3.10.0/apiservice-cabundle-controller/cm.yaml": v3100ApiserviceCabundleControllerCmYaml,
	"v3.10.0/apiservice-cabundle-controller/defaultconfig.yaml": v3100ApiserviceCabundleControllerDefaultconfigYaml,
	"v3.10.0/apiservice-cabundle-controller/deployment.yaml": v3100ApiserviceCabundleControllerDeploymentYaml,
	"v3.10.0/apiservice-cabundle-controller/ns.yaml": v3100ApiserviceCabundleControllerNsYaml,
	"v3.10.0/apiservice-cabundle-controller/sa.yaml": v3100ApiserviceCabundleControllerSaYaml,
	"v3.10.0/apiservice-cabundle-controller/signing-cabundle.yaml": v3100ApiserviceCabundleControllerSigningCabundleYaml,
	"v3.10.0/apiservice-cabundle-controller/svc.yaml": v3100ApiserviceCabundleControllerSvcYaml,
	"v3.10.0/configmap-cabundle-controller/clusterrole.yaml": v3100ConfigmapCabundleControllerClusterroleYaml,
	"v3.10.0/configmap-cabundle-controller/clusterrolebinding.yaml": v3100ConfigmapCabundleControllerClusterrolebindingYaml,
	"v3.10.0/configmap-cabundle-controller/cm.yaml": v3100ConfigmapCabundleControllerCmYaml,
	"v3.10.0/configmap-cabundle-controller/defaultconfig.yaml": v3100ConfigmapCabundleControllerDefaultconfigYaml,
	"v3.10.0/configmap-cabundle-controller/deployment.yaml": v3100ConfigmapCabundleControllerDeploymentYaml,
	"v3.10.0/configmap-cabundle-controller/ns.yaml": v3100ConfigmapCabundleControllerNsYaml,
	"v3.10.0/configmap-cabundle-controller/sa.yaml": v3100ConfigmapCabundleControllerSaYaml,
	"v3.10.0/configmap-cabundle-controller/signing-cabundle.yaml": v3100ConfigmapCabundleControllerSigningCabundleYaml,
	"v3.10.0/configmap-cabundle-controller/svc.yaml": v3100ConfigmapCabundleControllerSvcYaml,
	"v3.10.0/service-serving-cert-signer-controller/clusterrole.yaml": v3100ServiceServingCertSignerControllerClusterroleYaml,
	"v3.10.0/service-serving-cert-signer-controller/clusterrolebinding.yaml": v3100ServiceServingCertSignerControllerClusterrolebindingYaml,
	"v3.10.0/service-serving-cert-signer-controller/cm.yaml": v3100ServiceServingCertSignerControllerCmYaml,
	"v3.10.0/service-serving-cert-signer-controller/defaultconfig.yaml": v3100ServiceServingCertSignerControllerDefaultconfigYaml,
	"v3.10.0/service-serving-cert-signer-controller/deployment.yaml": v3100ServiceServingCertSignerControllerDeploymentYaml,
	"v3.10.0/service-serving-cert-signer-controller/ns.yaml": v3100ServiceServingCertSignerControllerNsYaml,
	"v3.10.0/service-serving-cert-signer-controller/sa.yaml": v3100ServiceServingCertSignerControllerSaYaml,
	"v3.10.0/service-serving-cert-signer-controller/signing-secret.yaml": v3100ServiceServingCertSignerControllerSigningSecretYaml,
	"v3.10.0/service-serving-cert-signer-controller/svc.yaml": v3100ServiceServingCertSignerControllerSvcYaml,
}

// AssetDir returns the file names below a certain
// directory embedded in the file by go-bindata.
// For example if you run go-bindata on data/... and data contains the
// following hierarchy:
//     data/
//       foo.txt
//       img/
//         a.png
//         b.png
// then AssetDir("data") would return []string{"foo.txt", "img"}
// AssetDir("data/img") would return []string{"a.png", "b.png"}
// AssetDir("foo.txt") and AssetDir("notexist") would return an error
// AssetDir("") will return []string{"data"}.
func AssetDir(name string) ([]string, error) {
	node := _bintree
	if len(name) != 0 {
		cannonicalName := strings.Replace(name, "\\", "/", -1)
		pathList := strings.Split(cannonicalName, "/")
		for _, p := range pathList {
			node = node.Children[p]
			if node == nil {
				return nil, fmt.Errorf("Asset %s not found", name)
			}
		}
	}
	if node.Func != nil {
		return nil, fmt.Errorf("Asset %s not found", name)
	}
	rv := make([]string, 0, len(node.Children))
	for childName := range node.Children {
		rv = append(rv, childName)
	}
	return rv, nil
}

type bintree struct {
	Func     func() (*asset, error)
	Children map[string]*bintree
}
var _bintree = &bintree{nil, map[string]*bintree{
	"v3.10.0": &bintree{nil, map[string]*bintree{
		"apiservice-cabundle-controller": &bintree{nil, map[string]*bintree{
			"clusterrole.yaml": &bintree{v3100ApiserviceCabundleControllerClusterroleYaml, map[string]*bintree{}},
			"clusterrolebinding.yaml": &bintree{v3100ApiserviceCabundleControllerClusterrolebindingYaml, map[string]*bintree{}},
			"cm.yaml": &bintree{v3100ApiserviceCabundleControllerCmYaml, map[string]*bintree{}},
			"defaultconfig.yaml": &bintree{v3100ApiserviceCabundleControllerDefaultconfigYaml, map[string]*bintree{}},
			"deployment.yaml": &bintree{v3100ApiserviceCabundleControllerDeploymentYaml, map[string]*bintree{}},
			"ns.yaml": &bintree{v3100ApiserviceCabundleControllerNsYaml, map[string]*bintree{}},
			"sa.yaml": &bintree{v3100ApiserviceCabundleControllerSaYaml, map[string]*bintree{}},
			"signing-cabundle.yaml": &bintree{v3100ApiserviceCabundleControllerSigningCabundleYaml, map[string]*bintree{}},
			"svc.yaml": &bintree{v3100ApiserviceCabundleControllerSvcYaml, map[string]*bintree{}},
		}},
		"configmap-cabundle-controller": &bintree{nil, map[string]*bintree{
			"clusterrole.yaml": &bintree{v3100ConfigmapCabundleControllerClusterroleYaml, map[string]*bintree{}},
			"clusterrolebinding.yaml": &bintree{v3100ConfigmapCabundleControllerClusterrolebindingYaml, map[string]*bintree{}},
			"cm.yaml": &bintree{v3100ConfigmapCabundleControllerCmYaml, map[string]*bintree{}},
			"defaultconfig.yaml": &bintree{v3100ConfigmapCabundleControllerDefaultconfigYaml, map[string]*bintree{}},
			"deployment.yaml": &bintree{v3100ConfigmapCabundleControllerDeploymentYaml, map[string]*bintree{}},
			"ns.yaml": &bintree{v3100ConfigmapCabundleControllerNsYaml, map[string]*bintree{}},
			"sa.yaml": &bintree{v3100ConfigmapCabundleControllerSaYaml, map[string]*bintree{}},
			"signing-cabundle.yaml": &bintree{v3100ConfigmapCabundleControllerSigningCabundleYaml, map[string]*bintree{}},
			"svc.yaml": &bintree{v3100ConfigmapCabundleControllerSvcYaml, map[string]*bintree{}},
		}},
		"service-serving-cert-signer-controller": &bintree{nil, map[string]*bintree{
			"clusterrole.yaml": &bintree{v3100ServiceServingCertSignerControllerClusterroleYaml, map[string]*bintree{}},
			"clusterrolebinding.yaml": &bintree{v3100ServiceServingCertSignerControllerClusterrolebindingYaml, map[string]*bintree{}},
			"cm.yaml": &bintree{v3100ServiceServingCertSignerControllerCmYaml, map[string]*bintree{}},
			"defaultconfig.yaml": &bintree{v3100ServiceServingCertSignerControllerDefaultconfigYaml, map[string]*bintree{}},
			"deployment.yaml": &bintree{v3100ServiceServingCertSignerControllerDeploymentYaml, map[string]*bintree{}},
			"ns.yaml": &bintree{v3100ServiceServingCertSignerControllerNsYaml, map[string]*bintree{}},
			"sa.yaml": &bintree{v3100ServiceServingCertSignerControllerSaYaml, map[string]*bintree{}},
			"signing-secret.yaml": &bintree{v3100ServiceServingCertSignerControllerSigningSecretYaml, map[string]*bintree{}},
			"svc.yaml": &bintree{v3100ServiceServingCertSignerControllerSvcYaml, map[string]*bintree{}},
		}},
	}},
}}

// RestoreAsset restores an asset under the given directory
func RestoreAsset(dir, name string) error {
	data, err := Asset(name)
	if err != nil {
		return err
	}
	info, err := AssetInfo(name)
	if err != nil {
		return err
	}
	err = os.MkdirAll(_filePath(dir, filepath.Dir(name)), os.FileMode(0755))
	if err != nil {
		return err
	}
	err = ioutil.WriteFile(_filePath(dir, name), data, info.Mode())
	if err != nil {
		return err
	}
	err = os.Chtimes(_filePath(dir, name), info.ModTime(), info.ModTime())
	if err != nil {
		return err
	}
	return nil
}

// RestoreAssets restores an asset under the given directory recursively
func RestoreAssets(dir, name string) error {
	children, err := AssetDir(name)
	// File
	if err != nil {
		return RestoreAsset(dir, name)
	}
	// Dir
	for _, child := range children {
		err = RestoreAssets(dir, filepath.Join(name, child))
		if err != nil {
			return err
		}
	}
	return nil
}

func _filePath(dir, name string) string {
	cannonicalName := strings.Replace(name, "\\", "/", -1)
	return filepath.Join(append([]string{dir}, strings.Split(cannonicalName, "/")...)...)
}

