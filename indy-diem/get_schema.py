import json
import requests
import codecs


def get_schema(sender_account: str, sender_seq_number: int, endpoint: str):
    data = {
        "jsonrpc": "2.0",
        "method": "get_account_transaction",
        "params": [sender_account, sender_seq_number, True],
        "id": 1
    }

    payload = json.dumps(data)
    post_headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    res = requests.post(endpoint, data=payload, headers=post_headers)
    res_string = json.loads(res.content.decode("utf-8"))

    print(res_string)

    res_metadata = res_string["result"]["events"][0]["data"]["metadata"]

    return codecs.decode(codecs.decode(res_metadata, 'hex'), 'UTF-8')
