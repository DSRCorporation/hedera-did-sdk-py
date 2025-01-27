from typing import cast

from did_sdk_py.did.did_document_operation import DidDocumentOperation
from did_sdk_py.did.hcs.events.owner.hcs_did_update_did_owner_event import HcsDidUpdateDidOwnerEvent
from did_sdk_py.did.hcs.hcs_did_message import HcsDidMessage
from did_sdk_py.did.hedera_did import HederaDid

from .common import DID_TOPIC_ID_1, DID_TOPIC_ID_2, IDENTIFIER


class TestHcsDidMessage:
    def test_valid_message(self, mock_client_provider, test_key):
        """Test valid message"""
        did = HederaDid(
            identifier=IDENTIFIER,
            private_key_der=test_key.private_key.toStringDER(),
            client_provider=mock_client_provider,
        )

        message = HcsDidMessage(
            DidDocumentOperation.CREATE,
            cast(str, did.identifier),
            HcsDidUpdateDidOwnerEvent(
                f"{did.identifier}#did-root-key",
                cast(str, did.identifier),
                test_key.private_key.getPublicKey(),
                test_key.key_type,
            ),
        )

        assert message.is_valid(DID_TOPIC_ID_1)

    def test_invalid_did(self, mock_client_provider, test_key):
        """Test Invalid Did"""
        did = HederaDid(
            identifier=IDENTIFIER,
            private_key_der=test_key.private_key.toStringDER(),
            client_provider=mock_client_provider,
        )

        message = HcsDidMessage(
            DidDocumentOperation.CREATE,
            "invalid_did###",
            HcsDidUpdateDidOwnerEvent(
                f"{did.identifier}#did-root-key",
                cast(str, did.identifier),
                test_key.private_key.getPublicKey(),
                test_key.key_type,
            ),
        )

        assert not message.is_valid()

    def test_invalid_topic(self, mock_client_provider, test_key):
        """Test Invalid Topic"""
        did = HederaDid(
            identifier=IDENTIFIER,
            private_key_der=test_key.private_key.toStringDER(),
            client_provider=mock_client_provider,
        )

        message = HcsDidMessage(
            DidDocumentOperation.CREATE,
            cast(str, did.identifier),
            HcsDidUpdateDidOwnerEvent(
                f"{did.identifier}#did-root-key",
                cast(str, did.identifier),
                test_key.private_key.getPublicKey(),
                test_key.key_type,
            ),
        )

        assert message.is_valid(DID_TOPIC_ID_1)
        assert not message.is_valid(DID_TOPIC_ID_2)
