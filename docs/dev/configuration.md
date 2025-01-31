# Configuration

At the moment, SDK comes with following configuration capabilities:

- Hedera Client configuration
- Cache implementation (optional)
- Logger configuration (optional)

## Hedera Client configuration

Configuration consists from two parts:

- Network configuration
  - Basic configuration is lightweight and consists from selection of specific network ("mainnet", "testnet", "
    previewnet"), complex parts are handled by Hedera Python SDK
  - Custom configuration can be provided, if necessary
- Hedera operator (account) configuration
  - Essentially, account "credentials" that will be used for Hedera network integration and paying fees
  - Needs to be provided explicitly and can be changed for specific Hedera Client instance via provider class

### Examples

#### Create client provider for Testnet and change operator config

```python
client_provider = HederaClientProvider(
    network_name="testnet",
    operator_config=OperatorConfig(account_id=OPERATOR_ID, private_key_der=OPERATOR_KEY_DER)
)

client_provider.set_operator_config(OperatorConfig(account_id=NEW_OPERATOR_ID, private_key_der=NEW_OPERATOR_KEY_DER))
```

#### Create client provider with custom network config

```python
TESTNET_NODES = {
    "0.0.4": "3.212.6.13:50212",
    "0.0.3": "34.94.106.61:50212",
    "0.0.8": "34.106.102.218:50212",
    "0.0.5": "35.245.27.193:50212",
    "0.0.7": "54.176.199.109:50212",
}

client_provider = HederaClientProvider(
    network_name="custom",
    operator_config=OperatorConfig(account_id=OPERATOR_ID, private_key_der=OPERATOR_KEY_DER),
    network_config=NetworkConfig(name="testnet", nodes=TESTNET_NODES, mirror_network="testnet"),
)
```

## Cache implementation

SDK utilizes cache to optimize read operations and provides an option to customize cache implementation (individually
for each resolver instance).

By default, [in-memory cache implementation](modules/common.md#did_sdk_py.utils.cache.MemoryCache) is used.

You can create custom cache implementation by inheriting [Cache base class](modules/common.md#did_sdk_py.utils.cache.Cache).
Custom cache instance needs to be provided in resolver constructor arguments.

Resolver classes that accept custom cache implementation:

- [HederaDidResolver](modules/did.md#did_sdk_py.did.hedera_did_resolver.HederaDidResolver)
- [HederaAnonCredsRegistry](modules/anoncreds.md#did_sdk_py.anoncreds.hedera_anoncreds_registry.HederaAnonCredsRegistry)

### Example

```python
custom_cache_instance = CustomCache[str, object]()

resolver = HederaDidResolver(client_provider, custom_cache_instance)
```

## Logger configuration

Logger configuration supports following properties that can be set with environment variables:

- Log level
  - Env variable name: `HEDERA_DID_SDK_LOG_LEVEL`
  - Currently supported values: "DEBUG", "INFO", "WARN", "ERROR"
- Log format (in string representation)
  - Env variable name: `HEDERA_DID_SDK_LOG_FORMAT`
  - For uniformity purposes, the SDK expects format string to correspond with Java (
    `ch.qos.logback:logback-classic`) [pattern](https://logback.qos.ch/manual/layouts.html#ClassicPatternLayout)
