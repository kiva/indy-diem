import time
import json 
from random import randrange
from threading import Thread
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from diem import AuthKey, utils, stdlib, diem_types
from datetime import datetime

import localnet

CURRENCY = "XUS"


# connect to testnet
client = localnet.create_client()

# generate private key for sender account
sender_private_key = Ed25519PrivateKey.generate()

print("the private key" + str(sender_private_key))
# generate auth key for sender account
sender_auth_key = AuthKey.from_public_key(sender_private_key.public_key())
print(f"Generated sender address: {utils.account_address_hex(sender_auth_key.account_address())}")

# create sender account
faucet = localnet.Faucet(client)
faucet.gen_account()
# localnet.Faucet.mint(faucet, sender_auth_key.hex(), 100000000, "XUS")

# # get sender account
# sender_account = client.get_account(sender_auth_key.account_address())

# # generate private key for receiver account
# receiver_private_key = Ed25519PrivateKey.generate()

# # generate auth key for receiver account
# receiver_auth_key = AuthKey.from_public_key(receiver_private_key.public_key())
# print(f"Generated receiver address: {utils.account_address_hex(receiver_auth_key.account_address())}")

# # create receiver account
# faucet = localnet.Faucet(client)
# faucet.mint(receiver_auth_key.hex(), 10000000, CURRENCY)



# METADATA = str.encode("{did:mydid101}")

# INDY_VERSION = 1
# INDY_TXN = "NYM"
# PROTOCOL_VERSION = 1
# PHOTO = "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAFCAYAAABxeg0vAAAAAXNSR0IArs4c6QAAAIRlWElmTU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAIdpAAQAAAABAAAAWgAAAAAAAABIAAAAAQAAAEgAAAABAAOgAQADAAAAAQABAACgAgAEAAAAAQAAAAygAwAEAAAAAQAAAAUAAAAA7Sb1LwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KGV7hBwAAAM9JREFUCB11jj1KQ3EQxGf2/8CQNFpKwCpYxkof1j5SeYQUCSR4iDRCvIGdpSSdvRZ2T6zs0gaxsFFIIB+QJtlxcwCn2pkfu7PojYpB97GVI9QfXZ2Hv9vP/4m9cfERcOi++0pZunDHSUosUau8+WLTZKZ5ZJcUq05MMghTxXGzNIvwnVDdd7rRcnNKYw7HEaQVwF8TOgbikNRZBN+Sr2O5HuA2Wu4B/wn/uWcwL0U/sGgoJeuQyBw8jvdeHtqvE9/6k2jPXqsODGhAdk1w/AchelJz2P+enAAAAABJRU5ErkJggg=="
# ACCOUNT= str(sender_account)
# REQ_ID = 1
    

# def defaultconverter(o):
#     if isinstance(o, datetime.datetime):
#         return o.__str__()

# INDY_TXN = json.dumps({
#     "ver": INDY_VERSION,
#     "txn": {
#         "type": INDY_VERSION,
#         "protocolVersion": PROTOCOL_VERSION,
#         "data": {
#             "photo~attach": PHOTO,
#             },
#             "metadata": {
#                 "reqId": 1,
#                 "from": ACCOUNT,
#                 "endorser": None,
#                 "digest": None,
#                 "payloadDigest": None,
#                 "taaAcceptance": {
#                     "taaDigest": None,
#                     "mechanism": None,
#                     "time": None
#                     } 
#                 },
#         },
#     "txnMetadata": {
#         "txnTime": str(datetime.utcnow()),
#         "seqNo": None,
#         "txnId": None
#         },
#     "reqSignature": {
#         "type": None,
#         "values": [{
#             "from": None,
#             "value": None
#             }]
#         }
# }, default=defaultconverter)


# METADATA = str.encode(INDY_TXN)

# # create script
# script = stdlib.encode_peer_to_peer_with_metadata_script(
#     currency=utils.currency_code(CURRENCY),
#     payee=receiver_auth_key.account_address(),
#     amount=1000033,
#     metadata=METADATA,  # no requirement for metadata and metadata signature
#     metadata_signature=b'',
#     )

# # create transaction
# raw_transaction = diem_types.RawTransaction(
#     sender=sender_auth_key.account_address(),
#     sequence_number=sender_account.sequence_number,
#     payload=diem_types.TransactionPayload__Script(script),
#     max_gas_amount=1_000_333,
#     gas_unit_price=0,
#     gas_currency_code=CURRENCY,
#     expiration_timestamp_secs=int(time.time()) + 30,
#     chain_id=localnet.CHAIN_ID,
#     )

# # sign transaction
# signature = sender_private_key.sign(utils.raw_transaction_signing_msg(raw_transaction))
# public_key_bytes = utils.public_key_bytes(sender_private_key.public_key())
# signed_txn = utils.create_signed_transaction(raw_transaction, public_key_bytes, signature)

# # submit transaction
# print(client.submit(signed_txn))

# # wait for transaction
# client.wait_for_transaction(signed_txn)


# print("DONE WITH THIS")
