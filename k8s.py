from kubernetes import client, config
from kubernetes.stream import stream
import requests
import json
import time
import unittest
import uuid
import ast

#from kubernetes.client import api_client
from kubernetes.client.apis import core_v1_api
from kubernetes.stream import stream
from kubernetes.stream.ws_client import ERROR_CHANNEL
# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
api = core_v1_api.CoreV1Api()


exec_command = ['/bin/sh',
                '-c',
                'curl -u user:ZCLw9NBayhrYAA3n http://127.0.0.1:15672/api/nodes']
resp = stream(api.connect_get_namespaced_pod_exec, 'api-staging-0', 'staging',
                                            command=exec_command,
                                            stdout=True, tty=False)

#j =resp.replace("\'", "\"")
#repl = json.dumps(j)
x = resp.replace("'", '"')
j = json.loads(resp)
print(j)


#print(parsed_mem['mem_used'])
