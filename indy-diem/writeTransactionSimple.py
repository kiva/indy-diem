import asyncio
import json
import time
import zlib

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from diem import AuthKey, testnet, utils, diem_types, stdlib
from indy import anoncreds, wallet
from indy import pool
from get_schema import get_schema
from base64 import b64encode, b64decode
from diem_txn import create_diem_script, create_diem_raw_txn, sign_and_wait_diem_txn
from compress_decompress_cred_def import compress_cred_def, clean_up_cred_def_res, decompress_cred_def
PROTOCOL_VERSION = 2
CURRENCY = "XUS"


async def create_schema():
    issuer = {
        'did': 'NcYxiDXkpYi6ov5FcYDi1e',
        'wallet_config': json.dumps({'id': 'issuer_wallet'}),
        'wallet_credentials': json.dumps({'key': 'issuer_wallet_key'})
    }
    prover = {
        'did': 'VsKV7grR1BUE29mG2Fm2kX',
        'wallet_config': json.dumps({"id": "prover_wallet"}),
        'wallet_credentials': json.dumps({"key": "issuer_wallet_key"})
    }
    verifier = {}
    store = {}

    # Set protocol version 2 to work with Indy Node 1.4
    await pool.set_protocol_version(PROTOCOL_VERSION)

    # 1. Create Issuer Wallet and Get Wallet Handle
    await wallet.create_wallet(issuer['wallet_config'], issuer['wallet_credentials'])
    issuer['wallet'] = await wallet.open_wallet(issuer['wallet_config'], issuer['wallet_credentials'])

    # 2. Create Prover Wallet and Get Wallet Handle
    await wallet.create_wallet(prover['wallet_config'], prover['wallet_credentials'])
    prover['wallet'] = await wallet.open_wallet(prover['wallet_config'], prover['wallet_credentials'])

    # 3. Issuer create Credential Schema
    schema = {
        'name': 'gvt',
        'version': '1.0',
        'attributes': '["age", "sex"]'
    }

    issuer['schema_id'], issuer['schema'] = await anoncreds.issuer_create_schema(issuer['did'], schema['name'],
                                                                                 schema['version'],
                                                                                 schema['attributes'])
    cred_def = {
        'tag': 'cred_def_tag',
        'type': 'CL',
        'config': json.dumps({"support_revocation": False})
    }

    issuer['cred_def_id'], issuer['cred_def'] = await anoncreds.issuer_create_and_store_credential_def(
        issuer['wallet'], issuer['did'], issuer['schema'], cred_def['tag'], cred_def['type'], cred_def['config'])
    store[issuer['cred_def_id']] = issuer['cred_def']

    time.sleep(1)

    return issuer['schema'], issuer['cred_def']


loop = asyncio.get_event_loop()

schema_and_cred_def = loop.run_until_complete(create_schema())
loop.close()
# connect to testnet
client = testnet.create_client()

# generate private key for sender account
sender_private_key = Ed25519PrivateKey.generate()

# generate auth key for sender account
sender_auth_key = AuthKey.from_public_key(sender_private_key.public_key())
print(f"Generated sender address: {utils.account_address_hex(sender_auth_key.account_address())}")

# create sender account
faucet = testnet.Faucet(client)
testnet.Faucet.mint(faucet, sender_auth_key.hex(), 100000000, "XUS")

# get sender account
sender_account = client.get_account(sender_auth_key.account_address())

# generate private key for receiver account
receiver_private_key = Ed25519PrivateKey.generate()

# generate auth key for receiver account
receiver_auth_key = AuthKey.from_public_key(receiver_private_key.public_key())
print(f"Generated receiver address: {utils.account_address_hex(receiver_auth_key.account_address())}")

# create receiver account
faucet = testnet.Faucet(client)
faucet.mint(receiver_auth_key.hex(), 10000000, CURRENCY)

loop = asyncio.get_event_loop()

METADATA = str.encode(schema_and_cred_def[0])

# create script
script = create_diem_script(CURRENCY, receiver_auth_key, METADATA)

# create transaction
raw_transaction = create_diem_raw_txn(sender_auth_key, sender_account, script, CURRENCY)

sign_and_wait_diem_txn(sender_private_key, raw_transaction, client)

print("Retrieving schema from Diem ledger:\n")
print(get_schema(utils.account_address_hex(sender_auth_key.account_address()), sender_account.sequence_number,
                 "https://testnet.diem.com/v1"))


cred_def_dict = compress_cred_def(schema_and_cred_def)

METADATA_CRED_DEF = str.encode(str(cred_def_dict))

# create script
script = create_diem_script(CURRENCY, receiver_auth_key, METADATA_CRED_DEF)

# create transaction
raw_transaction = create_diem_raw_txn(sender_auth_key, sender_account, script, CURRENCY, 1)

sign_and_wait_diem_txn(sender_private_key, raw_transaction, client)

print("Retrieving schema from Diem ledger:\n")
cred_def_res = get_schema(utils.account_address_hex(sender_auth_key.account_address()), sender_account.sequence_number+1,
                 "https://testnet.diem.com/v1")

filtered_cred_def = clean_up_cred_def_res(cred_def_res)

print(decompress_cred_def(filtered_cred_def))
