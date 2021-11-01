import time

from diem import AuthKey, testnet, utils, diem_types, stdlib


def create_diem_script(currency, receiver_auth_key, metadata):
    return stdlib.encode_peer_to_peer_with_metadata_script(
        currency=utils.currency_code(currency),
        payee=receiver_auth_key.account_address(),
        amount=10000000,
        metadata=metadata,  # no requirement for metadata and metadata signature
        metadata_signature=b'',
    )


def create_diem_raw_txn(sender_auth_key, sender_account, script, currency, sequence_number=0):
    return diem_types.RawTransaction(
        sender=sender_auth_key.account_address(),
        sequence_number=sender_account.sequence_number + sequence_number,
        payload=diem_types.TransactionPayload__Script(script),
        max_gas_amount=1_000_000,
        gas_unit_price=0,
        gas_currency_code=currency,
        expiration_timestamp_secs=int(time.time()) + 30,
        chain_id=testnet.CHAIN_ID,
    )


def sign_and_wait_diem_txn(sender_private_key, raw_transaction, client):
    # sign transaction
    signature = sender_private_key.sign(utils.raw_transaction_signing_msg(raw_transaction))
    public_key_bytes = utils.public_key_bytes(sender_private_key.public_key())
    signed_txn = utils.create_signed_transaction(raw_transaction, public_key_bytes, signature)

    # submit transaction
    client.submit(signed_txn)

    # wait for transaction
    client.wait_for_transaction(signed_txn)