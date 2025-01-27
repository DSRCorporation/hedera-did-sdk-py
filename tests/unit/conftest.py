from dataclasses import dataclass

import pytest
from hedera import PrivateKey, PublicKey
from pytest_mock import MockerFixture

from did_sdk_py import HederaClientProvider
from did_sdk_py.did.types import SupportedKeyType
from did_sdk_py.utils.cache import MemoryCache

PRIVATE_KEY = PrivateKey.generateED25519()


@dataclass
class TestKey:
    public_key: PublicKey
    private_key: PrivateKey
    key_type: SupportedKeyType
    public_key_base58: str
    public_key_base58_multibase: str


@pytest.fixture
def mock_client_provider(mocker: MockerFixture):
    MockHederaClientProvider = mocker.patch("did_sdk_py.HederaClientProvider", autospec=HederaClientProvider)
    return MockHederaClientProvider.return_value


@pytest.fixture
def mock_cache_instance(mocker: MockerFixture):
    MockMemoryCache = mocker.patch("did_sdk_py.utils.cache.Cache", autospec=MemoryCache[str, object])
    return MockMemoryCache.return_value


@pytest.fixture(
    params=[
        TestKey(
            PublicKey.fromStringDER(
                "302d300706052b8104000a0322000315e4bd693a096c1e7b9b46c2d09880873784d099ed44ee3f87670136baa68082"
            ),
            PrivateKey.fromStringDER(
                "3030020100300706052b8104000a042204205f817e1c0b24d0b25ef2976db00e42d42067c8a919bf9d07e2aac295e1300b04"
            ),
            "EcdsaSecp256k1VerificationKey2019",
            "vAQyPeUecGck2EsxcsihxhAB6jZurFrBbj2gC7CNkS5o",
            "zvAQyPeUecGck2EsxcsihxhAB6jZurFrBbj2gC7CNkS5o",
        ),
        TestKey(
            PublicKey.fromStringDER(
                "302a300506032b6570032100f32f7379f50d72ca6d501da611e2723b24528802983d16b5990255419e2eb2db"
            ),
            PrivateKey.fromStringDER(
                "302e020100300506032b657004220420e4f76aa303bfbf350ad080b879173b31977e5661d51ff5932f6597e2bb6680ff"
            ),
            "Ed25519VerificationKey2018",
            "HNJ37tiLbGxD7XPvnTkaZCAV3PCe5P4HJFGMGUkVVZAJ",
            "zHNJ37tiLbGxD7XPvnTkaZCAV3PCe5P4HJFGMGUkVVZAJ",
        ),
    ]
)
def test_key(request):
    return request.param
