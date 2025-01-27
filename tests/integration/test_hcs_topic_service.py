import pytest

from did_sdk_py import HederaClientProvider
from did_sdk_py.hcs import HcsTopicOptions, HcsTopicService

from .conftest import OPERATOR_KEY


@pytest.mark.flaky(retries=3, delay=1)
@pytest.mark.asyncio(loop_scope="session")
class TestHcsTopicService:
    async def test_creates_and_updates_hcs_topic(self, client_provider: HederaClientProvider):
        service = HcsTopicService(client_provider)

        topic_id = await service.create_topic(
            topic_options=HcsTopicOptions(submit_key=OPERATOR_KEY, admin_key=OPERATOR_KEY, topic_memo="topic_memo"),
            signing_keys=[OPERATOR_KEY],
        )

        topic_info = await service.get_topic_info(topic_id)
        assert topic_info.topicMemo == "topic_memo"

        await service.update_topic(
            topic_id,
            HcsTopicOptions(submit_key=OPERATOR_KEY, topic_memo="updated-topic-memo"),
            signing_keys=[OPERATOR_KEY],
        )

        topic_info = await service.get_topic_info(topic_id)
        assert topic_info.topicMemo == "updated-topic-memo"

    async def test_creates_immutable_topic_without_admin_key(self, client_provider: HederaClientProvider):
        service = HcsTopicService(client_provider)

        topic_id = await service.create_topic(
            topic_options=HcsTopicOptions(submit_key=OPERATOR_KEY, topic_memo="topic_memo"), signing_keys=[OPERATOR_KEY]
        )

        with pytest.raises(Exception, match="UNAUTHORIZED com.hedera.hashgraph.sdk.ReceiptStatusException"):
            await service.update_topic(
                topic_id,
                HcsTopicOptions(submit_key=OPERATOR_KEY, topic_memo="updated-topic-memo"),
                signing_keys=[OPERATOR_KEY],
            )
