from docker.models.containers import Container


def d2k_status(container: Container):
    if container.status == "running":
        return "Running"
    elif container.status == "exited":
        if container.attrs["State"]["ExitCode"] != 0:
            return "Failed"
        else:
            return "Succeeded"
    else:
        return "Unknown"

def d2k_conditions(container: Container):
    if container.status == ("running"):
        return [
                    {
                        "type": "Initialized",
                        "status": "True",
                        "lastProbeTime": "2024-07-20T14:18:05Z",
                        "lastTransitionTime": "2024-07-20T14:18:05Z"
                    },
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastProbeTime": "2024-07-20T14:18:05Z",
                        "lastTransitionTime": "2024-07-20T14:19:23Z"
                    },
                    {
                        "type": "ContainersReady",
                        "status": "True",
                        "lastProbeTime": "2024-07-20T14:18:05Z",
                        "lastTransitionTime": "2024-07-20T14:19:23Z"
                    },
                    {
                        "type": "PodScheduled",
                        "status": "True",
                        "lastProbeTime": "2024-07-20T14:18:05Z",
                        "lastTransitionTime": "2024-07-20T14:18:05Z"
                    }
                ]
    return []



# Also map the docker restart policy to kubernetes
def d2k_restart_policy(docker_restart_policy: str):
    if docker_restart_policy == "no":
        return "Never"
    elif docker_restart_policy == "on-failure":
        # If failed
        return "OnFailure"
    elif docker_restart_policy == "always":
        return "Always"
    elif docker_restart_policy == "unless-stopped":
        return "Never"
    else:
        # The default
        return "Never"


def d2k_container_state(container: Container):
    if container.status == "running":
        response = {"running": {
            # TODO why is this empty sometimes?
            "startedAt": container.attrs["State"]["StartedAt"] if container.attrs["State"]["StartedAt"] is not None and
                                                                  container.attrs["State"][
                                                                      "StartedAt"] != "" else "2024-07-20T14:18:05Z",
        }}
        print("========")
        print(response)
        print("========")
        return response
    elif container.status == "exited":
        return {"terminated": {
            "exitCode": container.attrs["State"]["ExitCode"],
            "finishedAt": container.attrs["State"]["FinishedAt"],
            "startedAt": container.attrs["State"]["StartedAt"],
        }}


def d2k_started(container: Container):
    # If the container is started / running / not terminated
    if container.status == "running":
        return True
    elif container.status == "exited":
        return False
    else:
        return False


def d2k_ready(container: Container):
    # Container is running and healthy
    if container.status == "running":
        # CHeck if healthy
        if container.health == "healthy" or container.health == "unknown":
            return True
        else:
            return False
    return False


def d2k_env_variables(env_variables):
    response = []

    for env in env_variables:
        # Split on first occurence of "="
        key, value = env.split("=", 1)
        response.append({
            "name": key,
            "value": value
        })

    return response


def d2k_container(container: Container):
    return {
        "metadata": {
            "name": container.name,
            "generateName": container.name,
            "namespace": container.labels.get("com.docker.compose.project", "default"),
            "uid": container.id,
            "resourceVersion": "1",
            # "creationTimestamp": "2024-07-20T14:18:05Z",
            "creationTimestamp": container.attrs["Created"],
            "labels": container.labels,
        },
        "spec": {
            "volumes": [
            ],
            "containers": [
                {
                    "name": container.name,
                    "image": container.image.attrs["RepoTags"][0] if len(container.image.attrs["RepoTags"]) > 0 else "",
                    "args": container.attrs["Args"],
                    "env": d2k_env_variables(container.attrs["Config"]["Env"]),
                    # "envFrom": [
                    #     {
                    #         "secretRef": {
                    #             "name": "ukonnwizard-secret-ukonnpirate"
                    #         }
                    #     },
                    #     {
                    #         "configMapRef": {
                    #             "name": "ukonnwizard-config-ukonnpirate"
                    #         }
                    #     }
                    # ],
                    # "resources": {
                    #     "limits": {
                    #         "cpu": "500m",
                    #         "memory": "250Mi"
                    #     },
                    #     "requests": {
                    #         "cpu": "500m",
                    #         "memory": "250Mi"
                    #     }
                    # },
                    # "volumeMounts": [
                    #     {
                    #         "name": "kube-api-access-dk87w",
                    #         "readOnly": True,
                    #         "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                    #     }
                    # ],
                    # "terminationMessagePath": "/dev/termination-log",
                    # "terminationMessagePolicy": "File",
                    # "imagePullPolicy": "IfNotPresent"
                }
            ],
            "restartPolicy": d2k_restart_policy(container.attrs["HostConfig"]["RestartPolicy"]["Name"]),
            # "terminationGracePeriodSeconds": 30,
            # "dnsPolicy": "ClusterFirst",
            # "serviceAccountName": "default",
            # "serviceAccount": "default",
            "nodeName": container.client.api.base_url,
            # "securityContext": {},
            # "imagePullSecrets": [
            #     {
            #         "name": "docker-credentials"
            #     }
            # ],
            # "schedulerName": "default-scheduler",
            # "tolerations": [
            #     {
            #         "key": "node.kubernetes.io/not-ready",
            #         "operator": "Exists",
            #         "effect": "NoExecute",
            #         "tolerationSeconds": 300
            #     },
            #     {
            #         "key": "node.kubernetes.io/unreachable",
            #         "operator": "Exists",
            #         "effect": "NoExecute",
            #         "tolerationSeconds": 300
            #     }
            # ],
            # "priority": 0,
            # "enableServiceLinks": True,
            # "preemptionPolicy": "PreemptLowerPriority"
        },
        "status": {
            "phase": d2k_status(container),
            "conditions": d2k_conditions(container),
            "hostIP": "127.0.0.1",
            "podIP": container.attrs["NetworkSettings"]["IPAddress"],
            # "podIPs": [
            #     {
            #         "ip": "10.219.109.12"
            #     }
            # ],
            "startTime": container.attrs["State"]["StartedAt"],
            "containerStatuses": [
                {
                    "name": container.name,
                    "state": d2k_container_state(container),
                    "started": d2k_started(container),
                    "ready": d2k_ready(container),
                    # "lastState": {},
                    # "ready": True,
                    # "restartCount": 0,
                    # "image": "docker.io/pragmaticindustriesgmbh/ukonn-wizard:c62b5cb823de6c913abdb418ca0970b1d0452b44",
                    # "imageID": "docker.io/pragmaticindustriesgmbh/ukonn-wizard@sha256:71b31c0090d2b294681ca407b490d0cf468aaa0d8ef2cbfddd54c031dde2c495",
                    # "containerID": "containerd://e92ec056c195112602bfe3fd2eba083d0fc99e758b5dbe88620a9ad2f7107810",
                    # "started": True
                }
            ],
            "qosClass": "Guaranteed"
        }
    }
    # return {
    #     "name": container.name,
    #     "image": container.image.attrs["RepoTags"][0],
    #     "args": container.attrs["Args"],
    #     "env": container.attrs["Config"]["Env"],
    #     "resources": {
    #         "limits": {
    #             "cpu": container.attrs["HostConfig"]["CpuQuota"],
    #             "memory": container.attrs["HostConfig"]["Memory"]
    #         },
    #         "requests": {
    #             "cpu": container.attrs["HostConfig"]["CpuQuota"],
    #             "memory": container.attrs["HostConfig"]["Memory"]
    #         }
    #     },
    #     "volumeMounts": [
    #         {
    #             "name": "kube-api-access-dk87w",
    #             "readOnly": True,
    #             "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
    #         }
    #     ],
    #     "terminationMessagePath": "/dev/termination-log",
    #     "terminationMessagePolicy": "File",
    #     "imagePullPolicy": "IfNotPresent"
    # }


def generate_pod_entry(name: str, generate_name: str, namespace: str, uid: str, creation_timestamp: str, labels: dict,
                       annotations: dict, volumes: list, containers: list, restart_policy: str, status: str):
    return {
        "metadata": {
            "name": name,
            "generateName": generate_name,
            "namespace": namespace,
            "uid": uid,
            "resourceVersion": "38632266872",
            # "creationTimestamp": "2024-07-20T14:18:05Z",
            "creationTimestamp": creation_timestamp,
            "labels": labels,
            "annotations": annotations,
            # "ownerReferences": [
            #     {
            #         "apiVersion": "apps/v1",
            #         "kind": "ReplicaSet",
            #         "name": "celery-beat-ukonnpirate-56497b4567",
            #         "uid": "0fa0a6be-3b97-4a53-8216-e1dcd245a99c",
            #         "controller": True,
            #         "blockOwnerDeletion": True
            #     }
            # ],
        },
        "spec": {
            "volumes": [
                # {
                #     "name": "kube-api-access-dk87w",
                #     "projected": {
                #         "sources": [
                #             {
                #                 "serviceAccountToken": {
                #                     "expirationSeconds": 3607,
                #                     "path": "token"
                #                 }
                #             },
                #             {
                #                 "configMap": {
                #                     "name": "kube-root-ca.crt",
                #                     "items": [
                #                         {
                #                             "key": "ca.crt",
                #                             "path": "ca.crt"
                #                         }
                #                     ]
                #                 }
                #             },
                #             {
                #                 "downwardAPI": {
                #                     "items": [
                #                         {
                #                             "path": "namespace",
                #                             "fieldRef": {
                #                                 "apiVersion": "v1",
                #                                 "fieldPath": "metadata.namespace"
                #                             }
                #                         }
                #                     ]
                #                 }
                #             }
                #         ],
                #         "defaultMode": 420
                #     }
                # }
            ],
            "containers": [
                {
                    "name": name,
                    "image": "pragmaticindustriesgmbh/ukonn-wizard:c62b5cb823de6c913abdb418ca0970b1d0452b44",
                    "args": [
                        "celery-beat"
                    ],
                    "envFrom": [
                        {
                            "secretRef": {
                                "name": "ukonnwizard-secret-ukonnpirate"
                            }
                        },
                        {
                            "configMapRef": {
                                "name": "ukonnwizard-config-ukonnpirate"
                            }
                        }
                    ],
                    "resources": {
                        "limits": {
                            "cpu": "500m",
                            "memory": "250Mi"
                        },
                        "requests": {
                            "cpu": "500m",
                            "memory": "250Mi"
                        }
                    },
                    "volumeMounts": [
                        {
                            "name": "kube-api-access-dk87w",
                            "readOnly": True,
                            "mountPath": "/var/run/secrets/kubernetes.io/serviceaccount"
                        }
                    ],
                    "terminationMessagePath": "/dev/termination-log",
                    "terminationMessagePolicy": "File",
                    "imagePullPolicy": "IfNotPresent"
                }
            ],
            "restartPolicy": restart_policy,
            # "terminationGracePeriodSeconds": 30,
            # "dnsPolicy": "ClusterFirst",
            # "serviceAccountName": "default",
            # "serviceAccount": "default",
            "nodeName": "this-node-does-not-exist-as-well",
            # "securityContext": {},
            # "imagePullSecrets": [
            #     {
            #         "name": "docker-credentials"
            #     }
            # ],
            # "schedulerName": "default-scheduler",
            # "tolerations": [
            #     {
            #         "key": "node.kubernetes.io/not-ready",
            #         "operator": "Exists",
            #         "effect": "NoExecute",
            #         "tolerationSeconds": 300
            #     },
            #     {
            #         "key": "node.kubernetes.io/unreachable",
            #         "operator": "Exists",
            #         "effect": "NoExecute",
            #         "tolerationSeconds": 300
            #     }
            # ],
            # "priority": 0,
            # "enableServiceLinks": True,
            # "preemptionPolicy": "PreemptLowerPriority"
        },
        "status": {
            "phase": status,
            "conditions": [
                {
                    "type": "Initialized",
                    "status": "True",
                    "lastProbeTime": "2024-07-20T14:18:05Z",
                    "lastTransitionTime": "2024-07-20T14:18:05Z"
                },
                {
                    "type": "Ready",
                    "status": "True",
                    "lastProbeTime": "2024-07-20T14:18:05Z",
                    "lastTransitionTime": "2024-07-20T14:19:23Z"
                },
                {
                    "type": "ContainersReady",
                    "status": "True",
                    "lastProbeTime": "2024-07-20T14:18:05Z",
                    "lastTransitionTime": "2024-07-20T14:19:23Z"
                },
                {
                    "type": "PodScheduled",
                    "status": "True",
                    "lastProbeTime": "2024-07-20T14:18:05Z",
                    "lastTransitionTime": "2024-07-20T14:18:05Z"
                }
            ],
            "hostIP": "212.227.162.30",
            "podIP": "10.219.109.12",
            "podIPs": [
                {
                    "ip": "10.219.109.12"
                }
            ],
            "startTime": "2024-07-20T14:18:05Z",
            "containerStatuses": [
                {
                    "name": "celery-beat",
                    "state": {
                        "running": {
                            "startedAt": "2024-07-20T14:19:23Z"
                        }
                    },
                    "lastState": {},
                    "ready": True,
                    "restartCount": 0,
                    "image": "docker.io/pragmaticindustriesgmbh/ukonn-wizard:c62b5cb823de6c913abdb418ca0970b1d0452b44",
                    "imageID": "docker.io/pragmaticindustriesgmbh/ukonn-wizard@sha256:71b31c0090d2b294681ca407b490d0cf468aaa0d8ef2cbfddd54c031dde2c495",
                    "containerID": "containerd://e92ec056c195112602bfe3fd2eba083d0fc99e758b5dbe88620a9ad2f7107810",
                    "started": True
                }
            ],
            "qosClass": "Guaranteed",
        }
    }
