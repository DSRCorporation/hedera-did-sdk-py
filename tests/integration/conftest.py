import os

import pytest
from hedera import PrivateKey

from did_sdk_py import HederaClientProvider, OperatorConfig
from did_sdk_py.utils.keys import get_key_type

OPERATOR_ID: str = os.environ.get("OPERATOR_ID")  # pyright: ignore [reportAssignmentType]
OPERATOR_KEY_DER: str = os.environ.get("OPERATOR_KEY")  # pyright: ignore [reportAssignmentType]

if not OPERATOR_ID or not OPERATOR_KEY_DER:
    raise Exception(
        "OPERATOR_ID and OPERATOR_KEY env variables must be set and correspond with valid testnet account."
        "You can obtain them by creating developer account on https://portal.hedera.com/"
    )

OPERATOR_KEY = PrivateKey.fromString(OPERATOR_KEY_DER)

OPERATOR_KEY_TYPE = get_key_type(OPERATOR_KEY)


@pytest.fixture(scope="class")
def client_provider():
    client_provider = HederaClientProvider(
        network_name="testnet", operator_config=OperatorConfig(account_id=OPERATOR_ID, private_key_der=OPERATOR_KEY_DER)
    )
    yield client_provider
    client_provider.dispose()
