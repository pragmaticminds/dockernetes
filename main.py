import datetime
from typing import Iterable, Optional

import docker
from docker.models.containers import Container
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

import utils

app = FastAPI()

"""
INFO:     None:0 - "GET /apis/networking.k8s.io HTTP/1.1" 404 Not Found
INFO:     None:0 - "GET /apis/apiextensions.k8s.io HTTP/1.1" 404 Not Found
INFO:     None:0 - "GET /api/v1/namespaces?limit=500 HTTP/1.1" 404 Not Found
INFO:     None:0 - "GET /apis/extensions HTTP/1.1" 404 Not Found
"""


@app.get("/api/v1/namespaces")
async def list_namespaces():
    # Get all namespaces
    # default + all compose projects
    namespaces = ["default"]

    client = docker.from_env()
    containers = client.containers.list(all=True)

    for container in containers:
        project = container.labels.get("com.docker.compose.project")
        if project and project not in namespaces:
            namespaces.append(project)

    return {
        "kind": "NamespaceList",
        "apiVersion": "v1",
        "metadata": {
            "resourceVersion": "38767485814"
        },
        "items": [
            {
                "metadata": {
                    "name": namespace,
                }} for namespace in namespaces
        ]}


@app.get("/api/v1/namespaces/{namespace}")
async def namespaces(namespace: str):
    return {}


@app.get("/api")
async def api():
    return {
        "kind": "APIVersions",
        "versions": [
            "v1"
        ],
        "serverAddressByClientCIDRs": [
            {
                "clientCIDR": "0.0.0.0/0",
                "serverAddress": "localhost:8080"
            }
        ]
    }


@app.get("/api/v1")
async def api_v1():
    return {
        "kind": "APIResourceList",
        "groupVersion": "v1",
        "resources": [
            {
                "name": "bindings",
                "singularName": "binding",
                "namespaced": True,
                "kind": "Binding",
                "verbs": [
                    "create"
                ]
            },
            {
                "name": "componentstatuses",
                "singularName": "componentstatus",
                "namespaced": False,
                "kind": "ComponentStatus",
                "verbs": [
                    "get",
                    "list"
                ],
                "shortNames": [
                    "cs"
                ]
            },
            {
                "name": "configmaps",
                "singularName": "configmap",
                "namespaced": True,
                "kind": "ConfigMap",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "cm"
                ],
                "storageVersionHash": "qFsyl6wFWjQ="
            },
            {
                "name": "endpoints",
                "singularName": "endpoints",
                "namespaced": True,
                "kind": "Endpoints",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "ep"
                ],
                "storageVersionHash": "fWeeMqaN/OA="
            },
            {
                "name": "events",
                "singularName": "event",
                "namespaced": True,
                "kind": "Event",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "ev"
                ],
                "storageVersionHash": "r2yiGXH7wu8="
            },
            {
                "name": "limitranges",
                "singularName": "limitrange",
                "namespaced": True,
                "kind": "LimitRange",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "limits"
                ],
                "storageVersionHash": "EBKMFVe6cwo="
            },
            {
                "name": "namespaces",
                "singularName": "namespace",
                "namespaced": False,
                "kind": "Namespace",
                "verbs": [
                    "create",
                    "delete",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "ns"
                ],
                "storageVersionHash": "Q3oi5N2YM8M="
            },
            {
                "name": "namespaces/finalize",
                "singularName": "",
                "namespaced": False,
                "kind": "Namespace",
                "verbs": [
                    "update"
                ]
            },
            {
                "name": "namespaces/status",
                "singularName": "",
                "namespaced": False,
                "kind": "Namespace",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "nodes",
                "singularName": "node",
                "namespaced": False,
                "kind": "Node",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "no"
                ],
                "storageVersionHash": "XwShjMxG9Fs="
            },
            {
                "name": "nodes/proxy",
                "singularName": "",
                "namespaced": False,
                "kind": "NodeProxyOptions",
                "verbs": [
                    "create",
                    "delete",
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "nodes/status",
                "singularName": "",
                "namespaced": False,
                "kind": "Node",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "persistentvolumeclaims",
                "singularName": "persistentvolumeclaim",
                "namespaced": True,
                "kind": "PersistentVolumeClaim",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "pvc"
                ],
                "storageVersionHash": "QWTyNDq0dC4="
            },
            {
                "name": "persistentvolumeclaims/status",
                "singularName": "",
                "namespaced": True,
                "kind": "PersistentVolumeClaim",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "persistentvolumes",
                "singularName": "persistentvolume",
                "namespaced": False,
                "kind": "PersistentVolume",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "pv"
                ],
                "storageVersionHash": "HN/zwEC+JgM="
            },
            {
                "name": "persistentvolumes/status",
                "singularName": "",
                "namespaced": False,
                "kind": "PersistentVolume",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "pods",
                "singularName": "pod",
                "namespaced": True,
                "kind": "Pod",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "po"
                ],
                "categories": [
                    "all"
                ],
                "storageVersionHash": "xPOwRZ+Yhw8="
            },
            {
                "name": "pods/attach",
                "singularName": "",
                "namespaced": True,
                "kind": "PodAttachOptions",
                "verbs": [
                    "create",
                    "get"
                ]
            },
            {
                "name": "pods/binding",
                "singularName": "",
                "namespaced": True,
                "kind": "Binding",
                "verbs": [
                    "create"
                ]
            },
            {
                "name": "pods/ephemeralcontainers",
                "singularName": "",
                "namespaced": True,
                "kind": "Pod",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "pods/eviction",
                "singularName": "",
                "namespaced": True,
                "group": "policy",
                "version": "v1",
                "kind": "Eviction",
                "verbs": [
                    "create"
                ]
            },
            {
                "name": "pods/exec",
                "singularName": "",
                "namespaced": True,
                "kind": "PodExecOptions",
                "verbs": [
                    "create",
                    "get"
                ]
            },
            {
                "name": "pods/log",
                "singularName": "",
                "namespaced": True,
                "kind": "Pod",
                "verbs": [
                    "get"
                ]
            },
            {
                "name": "pods/portforward",
                "singularName": "",
                "namespaced": True,
                "kind": "PodPortForwardOptions",
                "verbs": [
                    "create",
                    "get"
                ]
            },
            {
                "name": "pods/proxy",
                "singularName": "",
                "namespaced": True,
                "kind": "PodProxyOptions",
                "verbs": [
                    "create",
                    "delete",
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "pods/status",
                "singularName": "",
                "namespaced": True,
                "kind": "Pod",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "podtemplates",
                "singularName": "podtemplate",
                "namespaced": True,
                "kind": "PodTemplate",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "storageVersionHash": "LIXB2x4IFpk="
            },
            {
                "name": "replicationcontrollers",
                "singularName": "replicationcontroller",
                "namespaced": True,
                "kind": "ReplicationController",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "rc"
                ],
                "categories": [
                    "all"
                ],
                "storageVersionHash": "Jond2If31h0="
            },
            {
                "name": "replicationcontrollers/scale",
                "singularName": "",
                "namespaced": True,
                "group": "autoscaling",
                "version": "v1",
                "kind": "Scale",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "replicationcontrollers/status",
                "singularName": "",
                "namespaced": True,
                "kind": "ReplicationController",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "resourcequotas",
                "singularName": "resourcequota",
                "namespaced": True,
                "kind": "ResourceQuota",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "quota"
                ],
                "storageVersionHash": "8uhSgffRX6w="
            },
            {
                "name": "resourcequotas/status",
                "singularName": "",
                "namespaced": True,
                "kind": "ResourceQuota",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "secrets",
                "singularName": "secret",
                "namespaced": True,
                "kind": "Secret",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "storageVersionHash": "S6u1pOWzb84="
            },
            {
                "name": "serviceaccounts",
                "singularName": "serviceaccount",
                "namespaced": True,
                "kind": "ServiceAccount",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "sa"
                ],
                "storageVersionHash": "pbx9ZvyFpBE="
            },
            {
                "name": "serviceaccounts/token",
                "singularName": "",
                "namespaced": True,
                "group": "authentication.k8s.io",
                "version": "v1",
                "kind": "TokenRequest",
                "verbs": [
                    "create"
                ]
            },
            {
                "name": "services",
                "singularName": "service",
                "namespaced": True,
                "kind": "Service",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "svc"
                ],
                "categories": [
                    "all"
                ],
                "storageVersionHash": "0/CO1lhkEBI="
            },
            {
                "name": "services/proxy",
                "singularName": "",
                "namespaced": True,
                "kind": "ServiceProxyOptions",
                "verbs": [
                    "create",
                    "delete",
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "services/status",
                "singularName": "",
                "namespaced": True,
                "kind": "Service",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            }
        ]
    }


@app.get("/api/v1/nodes")
async def nodes():
    return {
        "kind": "NodeList",
        "apiVersion": "v1",
        "metadata": {
            "resourceVersion": "38729083751"
        },
        "items": [
            {
                "metadata": {
                    "name": "my-virtual-and-totally-not-existing-node",
                    "uid": "788b6ea8-29a0-4cf6-a51a-748a1540c651",
                    "resourceVersion": "38729082449",
                    "creationTimestamp": "2024-07-20T14:06:51Z",
                }
            }
        ]}


@app.get("/api/v1/namespaces/{namespace}/events")
async def events(namespace: str, fieldSelector: str = None):
    return {
        "kind": "EventList",
        "apiVersion": "v1",
        "metadata": {
            "resourceVersion": "38766738463"
        },
        "items": []
    }


# @app.get("/api/v1/namespaces/{namespace}/replicationcontrollers")
# async def replicationcontrollers(namespace: str):
#     return {"message": "Hello World"}


# @app.get("/api/v1/namespaces/{namespace}/services")
# async def services(namespace: str):
#     return {"message": "Hello World"}


@app.get("/apis")
async def apis():
    return {
        "kind": "APIGroupList",
        "apiVersion": "v1",
        "groups": [
            {
                "name": "apps",
                "versions": [
                    {
                        "groupVersion": "apps/v1",
                        "version": "v1"
                    }
                ],
                "preferredVersion": {
                    "groupVersion": "apps/v1",
                    "version": "v1"
                }
            },
        ]
    }


@app.get("/apis/apps/v1")
async def apps_v1():
    return {
        "kind": "APIResourceList",
        "apiVersion": "v1",
        "groupVersion": "apps/v1",
        "resources": [
            {
                "name": "controllerrevisions",
                "singularName": "controllerrevision",
                "namespaced": True,
                "kind": "ControllerRevision",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "storageVersionHash": "85nkx63pcBU="
            },
            {
                "name": "daemonsets",
                "singularName": "daemonset",
                "namespaced": True,
                "kind": "DaemonSet",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "ds"
                ],
                "categories": [
                    "all"
                ],
                "storageVersionHash": "dd7pWHUlMKQ="
            },
            {
                "name": "daemonsets/status",
                "singularName": "",
                "namespaced": True,
                "kind": "DaemonSet",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "deployments",
                "singularName": "deployment",
                "namespaced": True,
                "kind": "Deployment",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "deploy"
                ],
                "categories": [
                    "all"
                ],
                "storageVersionHash": "8aSe+NMegvE="
            },
            {
                "name": "deployments/scale",
                "singularName": "",
                "namespaced": True,
                "group": "autoscaling",
                "version": "v1",
                "kind": "Scale",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "deployments/status",
                "singularName": "",
                "namespaced": True,
                "kind": "Deployment",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "replicasets",
                "singularName": "replicaset",
                "namespaced": True,
                "kind": "ReplicaSet",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "rs"
                ],
                "categories": [
                    "all"
                ],
                "storageVersionHash": "P1RzHs8/mWQ="
            },
            {
                "name": "replicasets/scale",
                "singularName": "",
                "namespaced": True,
                "group": "autoscaling",
                "version": "v1",
                "kind": "Scale",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "replicasets/status",
                "singularName": "",
                "namespaced": True,
                "kind": "ReplicaSet",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "statefulsets",
                "singularName": "statefulset",
                "namespaced": True,
                "kind": "StatefulSet",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "sts"
                ],
                "categories": [
                    "all"
                ],
                "storageVersionHash": "H+vl74LkKdo="
            },
            {
                "name": "services",
                "singularName": "service",
                "namespaced": True,
                "kind": "Service",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "svc"
                ],
                "categories": [
                    "all"
                ],
                "storageVersionHash": "H+vl74LkKdo="
            },
            {
                "name": "pods",
                "singularName": "pod",
                "namespaced": True,
                "kind": "Pod",
                "verbs": [
                    "create",
                    "delete",
                    "deletecollection",
                    "get",
                    "list",
                    "patch",
                    "update",
                    "watch"
                ],
                "shortNames": [
                    "po"
                ],
                "categories": [
                    "all"
                ],
                "storageVersionHash": "H+vl74LkKdo="
            },
            {
                "name": "statefulsets/scale",
                "singularName": "",
                "namespaced": True,
                "group": "autoscaling",
                "version": "v1",
                "kind": "Scale",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            },
            {
                "name": "statefulsets/status",
                "singularName": "",
                "namespaced": True,
                "kind": "StatefulSet",
                "verbs": [
                    "get",
                    "patch",
                    "update"
                ]
            }
        ]
    }


# @app.get("/apis/apps/v1/namespaces/{namespace}/daemonsets")
# async def daemonsets(namespace: str):
#     return {"message": "Hello World"}
#
#
# @app.get("/apis/apps/v1/namespaces/{namespace}/deployments")
# async def deployments(namespace: str):
#     return {"message": "Hello World"}
#
#
# @app.get("/apis/apps/v1/namespaces/{namespace}/replicasets")
# async def replicasets(namespace: str):
#     return {"message": "Hello World"}
#
#
# @app.get("/apis/apps/v1/namespaces/{namespace}/services")
# async def apis_services(namespace: str):
#     return {"kind": "ServiceList", "apiVersion": "v1", "metadata": {"resourceVersion": "38729623520"}}


@app.get("/api/v1/pods")
async def api_pods(resourceVersion: str = None):
    """
    This is used by k9s to list the pods.
    :return:
    """
    return generate_podlist_from_docker()


@app.get("/apis/apps/v1/namespaces/{namespace}/pods")
async def apis_pods(namespace: str):
    """
    Is this even used?
    """
    return generate_podlist_from_docker(namespace)


@app.get("/api/v1/namespaces/{namespace}/pods")
async def pods(namespace: str):
    """
    This is used by kubectl
    """
    return generate_podlist_from_docker(namespace)


def generate_podlist_from_docker(namespace: Optional[str] = None):
    client = docker.from_env()
    containers: Iterable[Container] = client.containers.list(all=True)

    pods = []

    for container in containers:
        if namespace and container.labels.get("com.docker.compose.project", "default") != namespace:
            continue
        pod = utils.d2k_container(container)

        pods.append(pod)

    return {"kind": "PodList", "apiVersion": "v1", "metadata": {"resourceVersion": "38729623520"}, "items": pods}


def demo_pod_response(pod_name: str):
    return {
        "kind": "Pod",
        "apiVersion": "v1",
        "metadata": {
            "name": pod_name,
            "generateName": "alertmanager-kube-prometheus-stack-1628-alertmanager-",
            "namespace": "default",
            "uid": "708bf334-c513-4080-a392-24a4523c9ee0",
            "resourceVersion": "38632272059",
            "creationTimestamp": "2024-07-20T14:18:06Z",
            "labels": {
                "alertmanager": "kube-prometheus-stack-1628-alertmanager",
                "app": "alertmanager",
                "app.kubernetes.io/instance": "kube-prometheus-stack-1628-alertmanager",
                "app.kubernetes.io/managed-by": "prometheus-operator",
                "app.kubernetes.io/name": "alertmanager",
                "app.kubernetes.io/version": "0.22.2",
                "apps.kubernetes.io/pod-index": "0",
                "controller-revision-hash": "alertmanager-kube-prometheus-stack-1628-alertmanager-86bbf55859",
                "statefulset.kubernetes.io/pod-name": "alertmanager-kube-prometheus-stack-1628-alertmanager-0"
            },
            "annotations": {
                "cni.projectcalico.org/containerID": "c3d526ba1c95f8691cf56ceaa43d6c1399d36ee6bfd9d5b0c2f319bcaab0c5af",
                "cni.projectcalico.org/podIP": "10.219.186.224/32",
                "cni.projectcalico.org/podIPs": "10.219.186.224/32",
                "kubectl.kubernetes.io/default-container": "alertmanager"
            },
            "ownerReferences": [
                {
                    "apiVersion": "apps/v1",
                    "kind": "StatefulSet",
                    "name": "alertmanager-kube-prometheus-stack-1628-alertmanager",
                    "uid": "767aff72-3a91-4549-8d16-75e70cade505",
                    "controller": True,
                    "blockOwnerDeletion": True
                }
            ],
            "managedFields": [
                {
                    "manager": "kube-controller-manager",
                    "operation": "Update",
                    "apiVersion": "v1",
                    "time": "2024-07-20T14:18:06Z",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {
                        "f:metadata": {
                            "f:annotations": {
                                ".": {},
                                "f:kubectl.kubernetes.io/default-container": {}
                            },
                            "f:generateName": {},
                            "f:labels": {
                                ".": {},
                                "f:alertmanager": {},
                                "f:app": {},
                                "f:app.kubernetes.io/instance": {},
                                "f:app.kubernetes.io/managed-by": {},
                                "f:app.kubernetes.io/name": {},
                                "f:app.kubernetes.io/version": {},
                                "f:apps.kubernetes.io/pod-index": {},
                                "f:controller-revision-hash": {},
                                "f:statefulset.kubernetes.io/pod-name": {}
                            },
                            "f:ownerReferences": {
                                ".": {},
                                "k:{\"uid\":\"767aff72-3a91-4549-8d16-75e70cade505\"}": {}
                            }
                        },
                        "f:spec": {
                            "f:containers": {
                                "k:{\"name\":\"alertmanager\"}": {
                                    ".": {},
                                    "f:args": {},
                                    "f:env": {
                                        ".": {},
                                        "k:{\"name\":\"POD_IP\"}": {
                                            ".": {},
                                            "f:name": {},
                                            "f:valueFrom": {
                                                ".": {},
                                                "f:fieldRef": {}
                                            }
                                        }
                                    },
                                    "f:image": {},
                                    "f:imagePullPolicy": {},
                                    "f:livenessProbe": {
                                        ".": {},
                                        "f:failureThreshold": {},
                                        "f:httpGet": {
                                            ".": {},
                                            "f:path": {},
                                            "f:port": {},
                                            "f:scheme": {}
                                        },
                                        "f:periodSeconds": {},
                                        "f:successThreshold": {},
                                        "f:timeoutSeconds": {}
                                    },
                                    "f:name": {},
                                    "f:ports": {
                                        ".": {},
                                        "k:{\"containerPort\":9093,\"protocol\":\"TCP\"}": {
                                            ".": {},
                                            "f:containerPort": {},
                                            "f:name": {},
                                            "f:protocol": {}
                                        },
                                        "k:{\"containerPort\":9094,\"protocol\":\"TCP\"}": {
                                            ".": {},
                                            "f:containerPort": {},
                                            "f:name": {},
                                            "f:protocol": {}
                                        },
                                        "k:{\"containerPort\":9094,\"protocol\":\"UDP\"}": {
                                            ".": {},
                                            "f:containerPort": {},
                                            "f:name": {},
                                            "f:protocol": {}
                                        }
                                    },
                                    "f:readinessProbe": {
                                        ".": {},
                                        "f:failureThreshold": {},
                                        "f:httpGet": {
                                            ".": {},
                                            "f:path": {},
                                            "f:port": {},
                                            "f:scheme": {}
                                        },
                                        "f:initialDelaySeconds": {},
                                        "f:periodSeconds": {},
                                        "f:successThreshold": {},
                                        "f:timeoutSeconds": {}
                                    },
                                    "f:resources": {
                                        ".": {},
                                        "f:requests": {
                                            ".": {},
                                            "f:memory": {}
                                        }
                                    },
                                    "f:terminationMessagePath": {},
                                    "f:terminationMessagePolicy": {},
                                    "f:volumeMounts": {
                                        ".": {},
                                        "k:{\"mountPath\":\"/alertmanager\"}": {
                                            ".": {},
                                            "f:mountPath": {},
                                            "f:name": {}
                                        },
                                        "k:{\"mountPath\":\"/etc/alertmanager/certs\"}": {
                                            ".": {},
                                            "f:mountPath": {},
                                            "f:name": {},
                                            "f:readOnly": {}
                                        },
                                        "k:{\"mountPath\":\"/etc/alertmanager/config\"}": {
                                            ".": {},
                                            "f:mountPath": {},
                                            "f:name": {}
                                        }
                                    }
                                },
                                "k:{\"name\":\"config-reloader\"}": {
                                    ".": {},
                                    "f:args": {},
                                    "f:command": {},
                                    "f:env": {
                                        ".": {},
                                        "k:{\"name\":\"POD_NAME\"}": {
                                            ".": {},
                                            "f:name": {},
                                            "f:valueFrom": {
                                                ".": {},
                                                "f:fieldRef": {}
                                            }
                                        },
                                        "k:{\"name\":\"SHARD\"}": {
                                            ".": {},
                                            "f:name": {},
                                            "f:value": {}
                                        }
                                    },
                                    "f:image": {},
                                    "f:imagePullPolicy": {},
                                    "f:name": {},
                                    "f:resources": {
                                        ".": {},
                                        "f:limits": {
                                            ".": {},
                                            "f:cpu": {},
                                            "f:memory": {}
                                        },
                                        "f:requests": {
                                            ".": {},
                                            "f:cpu": {},
                                            "f:memory": {}
                                        }
                                    },
                                    "f:terminationMessagePath": {},
                                    "f:terminationMessagePolicy": {},
                                    "f:volumeMounts": {
                                        ".": {},
                                        "k:{\"mountPath\":\"/etc/alertmanager/config\"}": {
                                            ".": {},
                                            "f:mountPath": {},
                                            "f:name": {},
                                            "f:readOnly": {}
                                        }
                                    }
                                }
                            },
                            "f:dnsPolicy": {},
                            "f:enableServiceLinks": {},
                            "f:hostname": {},
                            "f:restartPolicy": {},
                            "f:schedulerName": {},
                            "f:securityContext": {
                                ".": {},
                                "f:fsGroup": {},
                                "f:runAsGroup": {},
                                "f:runAsNonRoot": {},
                                "f:runAsUser": {}
                            },
                            "f:serviceAccount": {},
                            "f:serviceAccountName": {},
                            "f:subdomain": {},
                            "f:terminationGracePeriodSeconds": {},
                            "f:volumes": {
                                ".": {},
                                "k:{\"name\":\"alertmanager-kube-prometheus-stack-1628-alertmanager-db\"}": {
                                    ".": {},
                                    "f:emptyDir": {},
                                    "f:name": {}
                                },
                                "k:{\"name\":\"config-volume\"}": {
                                    ".": {},
                                    "f:name": {},
                                    "f:secret": {
                                        ".": {},
                                        "f:defaultMode": {},
                                        "f:secretName": {}
                                    }
                                },
                                "k:{\"name\":\"tls-assets\"}": {
                                    ".": {},
                                    "f:name": {},
                                    "f:secret": {
                                        ".": {},
                                        "f:defaultMode": {},
                                        "f:secretName": {}
                                    }
                                }
                            }
                        }
                    }
                },
                {
                    "manager": "calico",
                    "operation": "Update",
                    "apiVersion": "v1",
                    "time": "2024-07-20T14:18:12Z",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {
                        "f:metadata": {
                            "f:annotations": {
                                "f:cni.projectcalico.org/containerID": {},
                                "f:cni.projectcalico.org/podIP": {},
                                "f:cni.projectcalico.org/podIPs": {}
                            }
                        }
                    },
                    "subresource": "status"
                },
                {
                    "manager": "kubelet",
                    "operation": "Update",
                    "apiVersion": "v1",
                    "time": "2024-07-20T14:19:42Z",
                    "fieldsType": "FieldsV1",
                    "fieldsV1": {
                        "f:status": {
                            "f:conditions": {
                                "k:{\"type\":\"ContainersReady\"}": {
                                    ".": {},
                                    "f:lastProbeTime": {},
                                    "f:lastTransitionTime": {},
                                    "f:status": {},
                                    "f:type": {}
                                },
                                "k:{\"type\":\"Initialized\"}": {
                                    ".": {},
                                    "f:lastProbeTime": {},
                                    "f:lastTransitionTime": {},
                                    "f:status": {},
                                    "f:type": {}
                                },
                                "k:{\"type\":\"Ready\"}": {
                                    ".": {},
                                    "f:lastProbeTime": {},
                                    "f:lastTransitionTime": {},
                                    "f:status": {},
                                    "f:type": {}
                                }
                            },
                            "f:containerStatuses": {},
                            "f:hostIP": {},
                            "f:phase": {},
                            "f:podIP": {},
                            "f:podIPs": {
                                ".": {},
                                "k:{\"ip\":\"10.219.186.224\"}": {
                                    ".": {},
                                    "f:ip": {}
                                }
                            },
                            "f:startTime": {}
                        }
                    },
                    "subresource": "status"
                }
            ]
        },
        "spec": {
            "volumes": [
                {
                    "name": "config-volume",
                    "secret": {
                        "secretName": "alertmanager-kube-prometheus-stack-1628-alertmanager-generated",
                        "defaultMode": 420
                    }
                },
                {
                    "name": "tls-assets",
                    "secret": {
                        "secretName": "alertmanager-kube-prometheus-stack-1628-alertmanager-tls-assets",
                        "defaultMode": 420
                    }
                },
                {
                    "name": "alertmanager-kube-prometheus-stack-1628-alertmanager-db",
                    "emptyDir": {}
                },
                {
                    "name": "kube-api-access-jz4td",
                    "projected": {
                        "sources": [
                            {
                                "serviceAccountToken": {
                                    "expirationSeconds": 3607,
                                    "path": "token"
                                }
                            },
                            {
                                "configMap": {
                                    "name": "kube-root-ca.crt",
                                    "items": [
                                        {
                                            "key": "ca.crt",
                                            "path": "ca.crt"
                                        }
                                    ]
                                }
                            },
                            {
                                "downwardAPI": {
                                    "items": [
                                        {
                                            "path": "namespace",
                                            "fieldRef": {
                                                "apiVersion": "v1",
                                                "fieldPath": "metadata.namespace"
                                            }
                                        }
                                    ]
                                }
                            }
                        ],
                        "defaultMode": 420
                    }
                }
            ],
            "containers": [
                {
                    "name": "alertmanager",
                    "image": "quay.io/prometheus/alertmanager:v0.22.2",
                    "args": [
                        "--config.file=/etc/alertmanager/config/alertmanager.yaml",
                        "--storage.path=/alertmanager",
                        "--data.retention=120h",
                        "--cluster.listen-address=",
                        "--web.listen-address=:9093",
                        "--web.external-url=http://kube-prometheus-stack-1628-alertmanager.default:9093",
                        "--web.route-prefix=/",
                        "--cluster.peer=alertmanager-kube-prometheus-stack-1628-alertmanager-0.alertmanager-operated:9094",
                        "--cluster.reconnect-timeout=5m"
                    ],
                    "ports": [
                        {
                            "name": "web",
                            "containerPort": 9093,
                            "protocol": "TCP"
                        },
                        {
                            "name": "mesh-tcp",
                            "containerPort": 9094,
                            "protocol": "TCP"
                        },
                        {
                            "name": "mesh-udp",
                            "containerPort": 9094,
                            "protocol": "UDP"
                        }
                    ],
                    "env": [
                        {
                            "name": "POD_IP",
                            "valueFrom": {
                                "fieldRef": {
                                    "apiVersion": "v1",
                                    "fieldPath": "status.podIP"
                                }
                            }
                        }
                    ],
                    "resources": {
                        "requests": {
                            "memory": "200Mi"
                        }
                    },
                    "volumeMounts": [
                        {
                            "name": "config-volume",
                            "mountPath": "/etc/alertmanager/config"
                        },
                        {
                            "name": "tls-assets",
                            "readOnly": True,
                            "mountPath": "/etc/alertmanager/certs"
                        },
                        {
                            "name": "alertmanager-kube-prometheus-stack-1628-alertmanager-db",
                            "mountPath": "/alertmanager"
                        },
                        {
                            "name": "kube-api-access-jz4td",
                            "readOnly": True,
                            "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                        }
                    ],
                    "livenessProbe": {
                        "httpGet": {
                            "path": "/-/healthy",
                            "port": "web",
                            "scheme": "HTTP"
                        },
                        "timeoutSeconds": 3,
                        "periodSeconds": 10,
                        "successThreshold": 1,
                        "failureThreshold": 10
                    },
                    "readinessProbe": {
                        "httpGet": {
                            "path": "/-/ready",
                            "port": "web",
                            "scheme": "HTTP"
                        },
                        "initialDelaySeconds": 3,
                        "timeoutSeconds": 3,
                        "periodSeconds": 5,
                        "successThreshold": 1,
                        "failureThreshold": 10
                    },
                    "terminationMessagePath": "/dev/termination-log",
                    "terminationMessagePolicy": "FallbackToLogsOnError",
                    "imagePullPolicy": "IfNotPresent"
                },
                {
                    "name": "config-reloader",
                    "image": "quay.io/prometheus-operator/prometheus-config-reloader:v0.49.0",
                    "command": [
                        "/bin/prometheus-config-reloader"
                    ],
                    "args": [
                        "--listen-address=:8080",
                        "--reload-url=http://127.0.0.1:9093/-/reload",
                        "--watched-dir=/etc/alertmanager/config"
                    ],
                    "env": [
                        {
                            "name": "POD_NAME",
                            "valueFrom": {
                                "fieldRef": {
                                    "apiVersion": "v1",
                                    "fieldPath": "metadata.name"
                                }
                            }
                        },
                        {
                            "name": "SHARD",
                            "value": "-1"
                        }
                    ],
                    "resources": {
                        "limits": {
                            "cpu": "100m",
                            "memory": "50Mi"
                        },
                        "requests": {
                            "cpu": "100m",
                            "memory": "50Mi"
                        }
                    },
                    "volumeMounts": [
                        {
                            "name": "config-volume",
                            "readOnly": True,
                            "mountPath": "/etc/alertmanager/config"
                        },
                        {
                            "name": "kube-api-access-jz4td",
                            "readOnly": True,
                            "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                        }
                    ],
                    "terminationMessagePath": "/dev/termination-log",
                    "terminationMessagePolicy": "FallbackToLogsOnError",
                    "imagePullPolicy": "IfNotPresent"
                }
            ],
            "restartPolicy": "Always",
            "terminationGracePeriodSeconds": 120,
            "dnsPolicy": "ClusterFirst",
            "serviceAccountName": "kube-prometheus-stack-1628-alertmanager",
            "serviceAccount": "kube-prometheus-stack-1628-alertmanager",
            "nodeName": "large-memory-pool-7kgfmdqgoi",
            "securityContext": {
                "runAsUser": 1000,
                "runAsGroup": 2000,
                "runAsNonRoot": True,
                "fsGroup": 2000
            },
            "hostname": "alertmanager-kube-prometheus-stack-1628-alertmanager-0",
            "subdomain": "alertmanager-operated",
            "schedulerName": "default-scheduler",
            "tolerations": [
                {
                    "key": "node.kubernetes.io/not-ready",
                    "operator": "Exists",
                    "effect": "NoExecute",
                    "tolerationSeconds": 300
                },
                {
                    "key": "node.kubernetes.io/unreachable",
                    "operator": "Exists",
                    "effect": "NoExecute",
                    "tolerationSeconds": 300
                }
            ],
            "priority": 0,
            "enableServiceLinks": True,
            "preemptionPolicy": "PreemptLowerPriority"
        },
        "status": {
            "phase": "Running",
            "conditions": [
                {
                    "type": "Initialized",
                    "status": "True",
                    "lastProbeTime": None,
                    "lastTransitionTime": "2024-07-20T14:18:06Z"
                },
                {
                    "type": "Ready",
                    "status": "True",
                    "lastProbeTime": None,
                    "lastTransitionTime": "2024-07-20T14:19:42Z"
                },
                {
                    "type": "ContainersReady",
                    "status": "True",
                    "lastProbeTime": None,
                    "lastTransitionTime": "2024-07-20T14:19:42Z"
                },
                {
                    "type": "PodScheduled",
                    "status": "True",
                    "lastProbeTime": None,
                    "lastTransitionTime": "2024-07-20T14:18:06Z"
                }
            ],
            "hostIP": "85.215.249.199",
            "podIP": "10.219.186.224",
            "podIPs": [
                {
                    "ip": "10.219.186.224"
                }
            ],
            "startTime": "2024-07-20T14:18:06Z",
            "containerStatuses": [
                {
                    "name": "alertmanager",
                    "state": {
                        "running": {
                            "startedAt": "2024-07-20T14:19:39Z"
                        }
                    },
                    "lastState": {},
                    "ready": True,
                    "restartCount": 0,
                    "image": "quay.io/prometheus/alertmanager:v0.22.2",
                    "imageID": "quay.io/prometheus/alertmanager@sha256:624c1a5063c7c80635081a504c3e1b020d89809651978eb5d0b652a394f3022d",
                    "containerID": "containerd://9c7b420baaad4ab35470b261e89931d3a29be45080d5ae48e29031a4c3d9c66b",
                    "started": True
                },
                {
                    "name": "config-reloader",
                    "state": {
                        "running": {
                            "startedAt": "2024-07-20T14:19:39Z"
                        }
                    },
                    "lastState": {},
                    "ready": True,
                    "restartCount": 0,
                    "image": "quay.io/prometheus-operator/prometheus-config-reloader:v0.49.0",
                    "imageID": "quay.io/prometheus-operator/prometheus-config-reloader@sha256:61bd63e7bc1aaebd39983d2c118a453e59427ccaa1b188cbadd4d0bded415d17",
                    "containerID": "containerd://5fbacdb344273198babe0e693e794bda4f264b44dac484c97e40b165e616c0e7",
                    "started": True
                }
            ],
            "qosClass": "Burstable"
        }
    }


@app.get("/api/v1/namespaces/{namespace}/pods/{pod}")
async def pods(namespace: str, pod: str):
    """
    Details for a pod
    """
    # return demo_pod_response()

    client = docker.from_env()
    containers: Iterable[Container] = client.containers.list(all=True)

    for container in containers:
        if container.name != pod:
            continue
        return {
            "kind": "Pod",
            "apiVersion": "v1",
            **utils.d2k_container(container)
        }
    raise Exception("Pod not found")


@app.get("/api/v1/namespaces/{namespace}/pods/{pod}/log", response_class=PlainTextResponse, )
async def pod_logs(namespace: str, pod: str, container: str = ""):
    """
    Details for a pod
    """

    client = docker.from_env()
    containers: Iterable[Container] = client.containers.list(all=True)

    for container in containers:
        if container.name != pod:
            continue
        return container.logs().decode("utf-8")
    raise Exception("Pod not found")


@app.get("/version")
async def version():
    return {
        "major": "1",
        "minor": "28",
        "gitVersion": "v1.28.4",
        "gitCommit": "bae2c62678db2b5053817bc97181fcc2e8388103",
        "gitTreeState": "clean",
        "buildDate": "2023-11-15T16:48:54Z",
        "goVersion": "go1.20.11",
        "compiler": "gc",
        "platform": "linux/amd64"
    }


@app.post("/apis/authorization.k8s.io/v1/selfsubjectaccessreviews", status_code=201)
async def selfsubjectaccessreviews(request: Request):
    """
    This is used by k9s to check the permissions of the current user.
    """
    req = await request.json()

    timestring = datetime.datetime.now()

    # We need to format the time according to kubernetes, e.g 2006-01-02T15:04:05Z
    timestring = timestring.strftime("%Y-%m-%dT%H:%M:%SZ")

    response = {
        "kind": "SelfSubjectAccessReview",
        "apiVersion": "authorization.k8s.io/v1",
        "metadata": {
            "creationTimestamp": timestring,
        },
        "spec": {
            "resourceAttributes": req["spec"]["resourceAttributes"]
        },
        "status": {
            "allowed": True,
            "denied": False
        }
    }

    return response
