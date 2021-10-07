import time

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from diem import AuthKey, testnet, identifier, utils, diem_types, stdlib

import get_events_example
from create_schema import create_schema_name, create_schema, create_local_did
from get_schema import get_schema

import json

from datetime import datetime

CURRENCY = "XUS"


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

indy_did = create_local_did()
schema_id = create_schema_name(indy_did, "kivatesting", "1.0")
schema = create_schema(schema_id,
                       ["undergrad", "last_name", "first_name", "birth_date", "postgrad", "expiry_date"],
                       "Degree",
                       "1.0",
                       indy_did
                       )

METADATA = str.encode(schema)

# create script
script = stdlib.encode_peer_to_peer_with_metadata_script(
    currency=utils.currency_code(CURRENCY),
    payee=receiver_auth_key.account_address(),
    amount=10000000,
    metadata=METADATA,  # no requirement for metadata and metadata signature
    metadata_signature=b'',
    )

# create transaction
raw_transaction = diem_types.RawTransaction(
    sender=sender_auth_key.account_address(),
    sequence_number=sender_account.sequence_number,
    payload=diem_types.TransactionPayload__Script(script),
    max_gas_amount=1_000_000,
    gas_unit_price=0,
    gas_currency_code=CURRENCY,
    expiration_timestamp_secs=int(time.time()) + 30,
    chain_id=testnet.CHAIN_ID,
    )

# sign transaction
signature = sender_private_key.sign(utils.raw_transaction_signing_msg(raw_transaction))
public_key_bytes = utils.public_key_bytes(sender_private_key.public_key())
signed_txn = utils.create_signed_transaction(raw_transaction, public_key_bytes, signature)

# submit transaction
client.submit(signed_txn)

# wait for transaction
client.wait_for_transaction(signed_txn)
print("Retrieving schema from Diem ledger:\n")
print(get_schema(utils.account_address_hex(sender_auth_key.account_address()), sender_account.sequence_number, "https://testnet.diem.com/v1"))



