## made to be resuable and should be updated to use anon creds

import json
import requests


LOCAL_URL = "http://0.0.0.0:8124/wallet/did/create"
LOCAL_HEADERS = {'accept': 'application/json', 'Content-Type': 'application/json'}
LOCAL_DID_DATA = {
    "method": "sov",
    "options": {
        "key_type": "ed25519"
    }
}

LOCAL_SCHEMA_NAME = "kivatesting"


def create_schema(id: str, attr_names: list, name: str, version: str, submitter_did: str):
    data = {
        "id": id,
        "attrNames": attr_names,
        "name": name,
        "version": version,
        "submitterDid": submitter_did
    }

    req_metadata = {
        "submitterDid": submitter_did
    }

    schema = {
        "data": data,
        "reqMetadata": req_metadata
    }

    print("CREATING SCHEMA:\n" + str(schema) + "\n")
    return json.dumps(schema)


def create_did(endpoint, data, headers):
    payload = json.dumps(data)
    return requests.post(endpoint, data=payload, headers=headers)


def create_local_did():
    res = create_did(LOCAL_URL, LOCAL_DID_DATA, LOCAL_HEADERS)
    res_data = res.json()
    did = res_data["result"]["did"]
    print("\nYOUR DID: " + did + "\n")
    return did


def create_schema_name(did: str, schema_name: str, version: str):
    return did + ":" + schema_name + ":" + version

# for testing
def create_local_schema_name():
    did = create_local_did()
    print(did)
    return create_schema_name(did , LOCAL_SCHEMA_NAME, "1.0")