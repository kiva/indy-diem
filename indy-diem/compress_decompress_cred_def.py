import json
import zlib

from base64 import b64encode, b64decode


def compress_cred_def(schema_and_cred_def):
    cred_def = json.dumps(schema_and_cred_def[1])
    cred_def = json.loads(cred_def)
    cred_def_encoded = cred_def.encode('utf-8')
    cred_def_compressed = zlib.compress(cred_def_encoded)
    cred_def_b64 = b64encode(cred_def_compressed)
    cred_def_ascii = cred_def_b64.decode('ascii')

    return {'b64': cred_def_ascii}


def clean_up_cred_def_res(cred_def_res):
    cred_def_res = cred_def_res.replace('\t', '')
    cred_def_res = cred_def_res.replace('\n', '')
    cred_def_res = cred_def_res.replace(',}', '}')
    cred_def_res = cred_def_res.replace(',]', ']')

    return eval(cred_def_res)


def decompress_cred_def(filtered_cred_def):
    return json.loads(zlib.decompress(b64decode(filtered_cred_def['b64'])))
