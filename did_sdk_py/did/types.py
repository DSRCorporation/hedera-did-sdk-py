from typing import Literal, TypeAlias

from did_resolver import DIDDocument, DIDResolutionResult
from did_resolver.resolver import DIDDocumentMetadata

DidServiceType: TypeAlias = Literal["LinkedDomains", "DIDCommMessaging"]

SupportedKeyType: TypeAlias = Literal["Ed25519VerificationKey2018", "EcdsaSecp256k1VerificationKey2019"]

VerificationRelationshipType: TypeAlias = Literal[
    "authentication", "assertionMethod", "keyAgreement", "capabilityInvocation", "capabilityDelegation"
]

__all__ = [
    "DIDResolutionResult",
    "DIDDocument",
    "DIDDocumentMetadata",
    "DidServiceType",
    "SupportedKeyType",
    "VerificationRelationshipType",
]
