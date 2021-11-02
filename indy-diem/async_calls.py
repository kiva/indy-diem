from indy import anoncreds


async def create_master_secret(prover):
    master_secret_id = await anoncreds.prover_create_master_secret(prover['wallet'], None)
    return master_secret_id


async def create_credential_offer(issuer_wallet, cred_def_id):
    cred_offer = await anoncreds.issuer_create_credential_offer(issuer_wallet, cred_def_id)
    return cred_offer


async def create_credential_req(prover):
    await anoncreds.prover_create_credential_req(prover['wallet'], prover['did'], prover['cred_offer'],
                                                     prover['cred_def'], prover['master_secret_id'])