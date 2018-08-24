import json
import os
import requests
import urllib3


def tf_job_spec(OCP_SECRET, TF_GIT_BRANCH, SESHETA_GITHUB_ACCESS_TOKEN, BUILD_MAP):
    job = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": "tensorflow-release-job",
            "labels": {
                "app": "thoth",
                "component": "tensorflow-release"
            }
        },
        "spec": {
            "parallelism": 1,
            "completions": 1,
            "template": {
                "spec": {
                    "containers": [
                        {
                            "image": "quay.io/aicoe/tensorflow-release-job",
                            "name": "tensorflow-release-job",
                            "env": [
                                {
                                    "name": "OCP_URL",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "key": "OCP_URL",
                                            "name": OCP_SECRET
                                        }
                                    }
                                },
                                {
                                    "name": "OCP_NAMESPACE",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "key": "OCP_NAMESPACE",
                                            "name": OCP_SECRET
                                        }
                                    }
                                },
                                {
                                    "name": "OCP_TOKEN",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "key": "OCP_TOKEN",
                                            "name": OCP_SECRET
                                        }
                                    }
                                },
                                {
                                    "name": "TF_GIT_BRANCH",
                                    "value": TF_GIT_BRANCH
                                },
                                {
                                    "name": "GIT_TOKEN",
                                    "value": SESHETA_GITHUB_ACCESS_TOKEN
                                },
                                {
                                    "name": "BUILD_MAP",
                                    "value": BUILD_MAP
                                }
                            ],
                            "resources": {
                                "requests": {
                                    "memory": "1Gi",
                                    "cpu": "1"
                                },
                                "limits": {
                                    "memory": "1Gi",
                                    "cpu": "1"
                                }
                            }
                        }
                    ],
                    "restartPolicy": "Never",
                    "lookupPolicy": {
                        "local": True
                    }
                }
            }
        }
    }
    return job


def tf_release_job(job, url, namespace, headers):
    job_endpoint = '{}/apis/batch/v1/namespaces/{}/jobs'.format(url, namespace)
    job_response = requests.post(job_endpoint, json=job, headers=headers, verify=False)
    print("Status code for job POST request: ", job_response.status_code)
    if job_response.status_code == 201:
        return True
    else:
        print("Error for job POST request: ", job_response.text)
        return False

def release(tf_version):
    urllib3.disable_warnings()
    # Application Variable  
    TF_GIT_BRANCH = tf_version if 'r' in tf_version else 'r'+ tf_version
    OCP_SECRET = os.getenv('OCP_SECRET', '{}') 
    SESHETA_GITHUB_ACCESS_TOKEN = os.getenv('SESHETA_GITHUB_ACCESS_TOKEN', "")
    with open('config.json', 'r') as f:
        config_data = f.read()
    BUILD_MAP = json.dumps(json.loads(config_data))
    namespace = os.getenv('OCP_NAMESPACE', '')  # set default inplace default quotes
    url = os.getenv('OCP_URL', '')  # set default inplace default quotes
    access_token = os.getenv('OCP_TOKEN', '')  # set default inplace default quotes
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
        'Accept': 'application/json',
        'Connection': 'close'
    }
    # print("-------------------VARIABLES-------------------------")
    # print("OCP_SECRET: ", OCP_SECRET)
    # print("TF_GIT_BRANCH", TF_GIT_BRANCH)
    # print("SESHETA_GITHUB_ACCESS_TOKEN", SESHETA_GITHUB_ACCESS_TOKEN)
    # print("BUILD_MAP", BUILD_MAP)
    # print("namespace", namespace)
    # print("url", url)
    # print("access_token", access_token)
    # print("-----------------------------------------------------")
    job = tf_job_spec(OCP_SECRET, TF_GIT_BRANCH, SESHETA_GITHUB_ACCESS_TOKEN, BUILD_MAP)
    if job:
        tf_release_job(job, url, namespace, headers)
        return 202
    else:
        return 400

def custom_release(**opts):
    urllib3.disable_warnings()
    TF_GIT_BRANCH = 'r'+opts.pop('TENSORFLOW_VERSION')
    SESHETA_GITHUB_ACCESS_TOKEN = opts.pop('GITHUB_ACCESS_TOKEN')
    PY_VERSION = opts.pop('PY_VERSION')
    OS=opts.pop('OS') 
    BUILD_MAP= {py: {} for py in PY_VERSION}
    for key,value in BUILD_MAP.items():
        BUILD_MAP[key] = { OS : {k:v for k,v in opts.items()}}
    print("BUILD_MAP", BUILD_MAP)
    OCP_SECRET = os.getenv('OCP_SECRET', '{}') 
    namespace = os.getenv('OCP_NAMESPACE', '')  # set default inplace default quotes
    url = os.getenv('OCP_URL', '')  # set default inplace default quotes
    access_token = os.getenv('OCP_TOKEN', '')  # set default inplace default quotes
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token),
        'Accept': 'application/json',
        'Connection': 'close'
    }
    # print("-------------------VARIABLES-------------------------")
    # print("OCP_SECRET: ", OCP_SECRET)
    # print("TF_GIT_BRANCH", TF_GIT_BRANCH)
    # print("SESHETA_GITHUB_ACCESS_TOKEN", SESHETA_GITHUB_ACCESS_TOKEN)
    # print("BUILD_MAP", BUILD_MAP)
    # print("namespace", namespace)
    # print("url", url)
    # print("access_token", access_token)
    # print("-----------------------------------------------------")
    job = tf_job_spec(OCP_SECRET, TF_GIT_BRANCH, SESHETA_GITHUB_ACCESS_TOKEN, json.dumps(BUILD_MAP))
    if job:
        tf_release_job(job, url, namespace, headers)
        return 202
    else:
        return 400    
