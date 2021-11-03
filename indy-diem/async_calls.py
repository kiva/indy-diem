from indy import anoncreds


async def create_master_secret(prover):
    master_secret_id = await anoncreds.prover_create_master_secret(prover['wallet'], None)
    return master_secret_id


async def create_credential_offer(issuer_wallet, cred_def_id):
    cred_offer = await anoncreds.issuer_create_credential_offer(issuer_wallet, cred_def_id)
    return cred_offer


async def create_credential_req(prover):
    cred_req = await anoncreds.prover_create_credential_req(prover['wallet'], prover['did'], prover['cred_offer'],
                                                            prover['cred_def'], prover['master_secret_id'])
    return cred_req


async def create_credential(issuer):
    credential = await anoncreds.issuer_create_credential(issuer['wallet'], issuer['cred_offer'],
                                                          issuer['cred_req'], issuer['cred_values'], None, None)
    return credential


async def store_credential(prover):
    credential = await anoncreds.prover_store_credential(prover['wallet'], None, prover['cred_req_metadata'],
                                                         prover['cred'],
                                                         prover['cred_def'], None)
    return credential
