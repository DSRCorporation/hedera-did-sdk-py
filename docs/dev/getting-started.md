# Getting started

## Prerequisites

- Python 3.12+

## Install from PyPi

TODO: update package namespace

```bash
pip install hedera-did-sdk-py
```

## Example usage

Here you can find basic SDK usage examples.

For more complex examples, please refer to SDK integration tests:

- [Hedera DID](https://github.com/hashgraph/did-sdk-py/blob/main/tests/integration/test_hedera_did.py)
- [AnonCreds registry](https://github.com/hashgraph/did-sdk-py/blob/main/tests/integration/test_hedera_anoncreds_registry.py)

### Create Hedera Client provider (for testnet)

```python
client_provider = HederaClientProvider(
    network_name="testnet",
    operator_config=OperatorConfig(account_id=OPERATOR_ID, private_key_der=OPERATOR_KEY_DER)
)
```

### Register new Hedera DID on testnet network and add DID service

```python
did = HederaDid(client_provider=client_provider, private_key_der=private_key_der)

await did.register()

await did.add_service(
    id_=f"{did.identifier}#service-1", service_type="LinkedDomains", service_endpoint="https://example.com/vcs"
)
```

### Resolve existing Hedera DID

```python
resolver = HederaDidResolver(client_provider)

resolution_result = await resolver.resolve(
    "did:hedera:testnet:zvAQyPeUecGck2EsxcsihxhAB6jZurFrBbj2gC7CNkS5o_0.0.5063027")
```

### Create AnonCreds credential schema and credential definition

```python
issuer_did = "did:hedera:testnet:zvAQyPeUecGck2EsxcsihxhAB6jZurFrBbj2gC7CNkS5o_0.0.5063027"
registry = HederaAnonCredsRegistry(client_provider)

schema = AnonCredsSchema(
    name="schema-name",
    issuer_id=issuer_did,
    attr_names=["name", "age"],
    version="1"
)

schema_registration_result = await registry.register_schema(schema, issuer_did, OPERATOR_KEY_DER)

cred_def = AnonCredsCredDef(
    schema_id=schema_registration_result.schema_state.schema_id,
    issuer_id=issuer_did,
    value=CredDefValue(primary=CredDefValuePrimary(...)),
    tag="cred-def-tag"
)

cred_def_registration_result = await registry.register_cred_def(cred_def, issuer_did, OPERATOR_KEY_DER)
```
