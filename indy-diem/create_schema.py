import json


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

    print(schema)
    return json.dumps(schema)
