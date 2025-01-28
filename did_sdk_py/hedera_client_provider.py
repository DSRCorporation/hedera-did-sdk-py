from dataclasses import dataclass
from typing import Literal

from hedera_sdk_python.account.account_id import AccountId
from hedera_sdk_python.client.client import Client
from hedera_sdk_python.client.network import Network
from hedera_sdk_python.crypto.private_key import PrivateKey

from .utils.serializable import Serializable

NetworkName = Literal["mainnet", "testnet", "previewnet"]


@dataclass(frozen=True)
class OperatorConfig:
    """Hedera operator config.

    Attributes:
        account_id: Hedera operator (account) ID
        private_key_der: Hedera operator private key encoded in DER format
    """

    account_id: str
    private_key_der: str


@dataclass(frozen=True)
class NetworkConfig(Serializable):
    """Hedera network config.

    Should be used only for customization purposes, if it's not needed - use default configurations instead.
    """

    name: NetworkName
    nodes: dict[str, str]
    mirror_network: str | list[str]

    @classmethod
    def from_json_payload(cls, payload: dict):
        raise Exception("Not implemented")

    def get_json_payload(self):
        return {"network": self.nodes, "mirrorNetwork": self.mirror_network}


class HederaClientProvider:
    """
    Provider class for managing Hedera network client instance.

    Used to create client instances with either default Hedera network configurations or custom ones.

    Args:
        network_name: Hedera network name ("mainnet", "testnet", "previewnet", "custom")
        operator_config: Hedera account/operator config
        network_config: Custom network config, requires "network_name" to be set to "custom"
    """

    def __init__(
        self,
        network_name: Literal[NetworkName, "custom"],
        operator_config: OperatorConfig | None = None,
        network_config: NetworkConfig | None = None,
    ):
        if network_name == "custom":
            if not network_config:
                raise Exception("Network config is required for custom network configuration")
            # Native Python SDK supports only single node in custom network
            node_account_id, node_address = network_config.nodes.popitem()

            self._client = Client(Network(node_account_id=node_account_id, node_address=node_address))
        elif network_config:
            raise Exception("Network config is supported only for custom network configuration")
        else:
            self._client = Client(Network(network=network_name))

        if operator_config:
            self.set_operator_config(operator_config)

        self._disposed = False

    def set_operator_config(self, operator_config: OperatorConfig):
        """
        Set operator config for Hedera client instance.

        Args:
            operator_config: Operator config to set
        """
        self._client.set_operator(
            AccountId.from_string(operator_config.account_id), PrivateKey.from_string(operator_config.private_key_der)
        )

    def get_client(self):
        """Get Hedera client instance."""
        if self._disposed:
            raise Exception("Client provider has been disposed")
        return self._client

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()

    def dispose(self):
        """Dispose (close) Hedera client instance."""
        # Not implemented in Native SDK for some reason
        # self._client.close()
        self._disposed = True
