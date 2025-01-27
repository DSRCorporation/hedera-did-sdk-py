from hedera import PrivateKey, PublicKey

from ..did.types import SupportedKeyType


def get_key_type(private_key: PrivateKey | PublicKey) -> SupportedKeyType:
    if private_key.isED25519():
        return "Ed25519VerificationKey2018"

    elif private_key.isECDSA():
        return "EcdsaSecp256k1VerificationKey2019"

    else:
        raise Exception("Unknown key type")
