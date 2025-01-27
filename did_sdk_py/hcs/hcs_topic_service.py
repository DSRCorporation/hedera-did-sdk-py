from dataclasses import dataclass

from hedera import (
    Hbar,
    PrivateKey,
    PublicKey,
    TopicCreateTransaction,
    TopicId,
    TopicInfo,
    TopicInfoQuery,
    TopicUpdateTransaction,
)

from ..hedera_client_provider import HederaClientProvider
from .constants import MAX_TRANSACTION_FEE
from .utils import execute_hcs_query_async, execute_hcs_transaction_async, sign_hcs_transaction_async

TopicTransaction: type = TopicCreateTransaction | TopicUpdateTransaction


@dataclass(frozen=True)
class HcsTopicOptions:
    submit_key: PublicKey
    topic_memo: str | None = None
    admin_key: PublicKey | None = None
    max_transaction_fee_hbar: int | None = None


def _set_topic_transaction_options(transaction: TopicTransaction, topic_options: HcsTopicOptions) -> TopicTransaction:
    if topic_options.admin_key:
        transaction.setAdminKey(topic_options.admin_key)

    if topic_options.topic_memo:
        transaction.setTopicMemo(topic_options.topic_memo)

    max_transaction_fee = (
        Hbar(topic_options.max_transaction_fee_hbar) if topic_options.max_transaction_fee_hbar else MAX_TRANSACTION_FEE
    )
    transaction.setSubmitKey(topic_options.submit_key).setMaxTransactionFee(max_transaction_fee)

    return transaction


class HcsTopicService:
    def __init__(self, client_provider: HederaClientProvider):
        self._client = client_provider.get_client()

    async def create_topic(self, topic_options: HcsTopicOptions, signing_keys: list[PrivateKey]) -> str:
        transaction = _set_topic_transaction_options(TopicCreateTransaction(), topic_options).freezeWith(self._client)

        signed_transaction = await sign_hcs_transaction_async(transaction, signing_keys)
        transaction_receipt = await execute_hcs_transaction_async(signed_transaction, self._client)

        return transaction_receipt.topicId.toString()

    async def update_topic(self, topic_id: str, topic_options: HcsTopicOptions, signing_keys: list[PrivateKey]):
        transaction = _set_topic_transaction_options(
            TopicUpdateTransaction().setTopicId(TopicId.fromString(topic_id)), topic_options
        ).freezeWith(self._client)
        signed_transaction = await sign_hcs_transaction_async(transaction, signing_keys)
        await execute_hcs_transaction_async(signed_transaction, self._client)

    async def get_topic_info(self, topic_id: str) -> TopicInfo:
        return await execute_hcs_query_async(TopicInfoQuery().setTopicId(TopicId.fromString(topic_id)), self._client)
