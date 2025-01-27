import logging
from collections.abc import Callable

from hedera import Client, JDuration, MirrorResponse, PyConsumer, TopicId, TopicMessageQuery

from ..utils.pyjnius import ErrorHandlerBiConsumer, Runnable
from ..utils.timestamp import Timestamp
from .hcs_message import HcsMessage, HcsMessageWithResponseMetadata

LOGGER = logging.getLogger(__name__)


class HcsTopicListener:
    def __init__(
        self,
        topic_id: str,
        message_class: type[HcsMessage],
        include_response_metadata: bool = False,
    ):
        self.topic_id = topic_id
        self._message_class = message_class
        self._include_response_metadata = include_response_metadata
        self._filters = []
        self._subscription_handle = None
        self._invalid_message_handler = None

        # IMPORTANT
        # We need to store 'PythonJavaClass' reference as long as it can be used by Java to prevent it being cleaned up by Python GC
        # Otherwise, intermittent segmentation faults and other hard-to-debug issues are possible
        self._java_consumer_reference: PyConsumer | None = None

        self._query = (
            TopicMessageQuery()
            .setTopicId(TopicId.fromString(topic_id))
            .setStartTime((Timestamp(0, 0)).to_jinstant())
            .setMaxBackoff(JDuration.ofMillis(2000))
            .setMaxAttempts(5)
        )

    def set_start_time(self, start_time: Timestamp):
        self._query.setStartTime(start_time.to_jinstant())
        return self

    def set_end_time(self, end_time: Timestamp):
        self._query.setEndTime(end_time.to_jinstant())
        return self

    def set_limit(self, limit: int):
        self._query.setLimit(limit)
        return self

    def set_completion_handler(self, completion_handler: Runnable):
        self._query.setCompletionHandler(completion_handler)
        return self

    def add_filter(self, response_filter: Callable[[MirrorResponse], bool]):
        self._filters.append(response_filter)
        return self

    def set_error_handler(self, error_handler: ErrorHandlerBiConsumer):
        self._query.setErrorHandler(error_handler)
        return self

    def set_invalid_message_handler(self, invalid_message_handler: Callable[[MirrorResponse, str], None]):
        self._invalid_message_handler = invalid_message_handler
        return self

    def subscribe(self, client: Client, receiver: Callable[[HcsMessage | HcsMessageWithResponseMetadata], None]):
        def handle_message(response):
            self._handle_response(response, receiver)

        self._java_consumer_reference = PyConsumer(handle_message)

        self._subscription_handle = self._query.subscribe(client, self._java_consumer_reference)

    def unsubscribe(self):
        if self._subscription_handle:
            self._subscription_handle.unsubscribe()
        self._java_consumer_reference = None

    def _handle_response(
        self, response: MirrorResponse, receiver: Callable[[HcsMessage | HcsMessageWithResponseMetadata], None]
    ):
        if len(self._filters) > 0:
            for response_filter in self._filters:
                if not response_filter(response):
                    self._report_invalid_message(response, "Message response was rejected by user-defined filter")
                    return

        message = self._extract_message(response)
        if not message:
            self._report_invalid_message(response, "Extracting message from the mirror response failed")
            return

        if not message.is_valid(self.topic_id):
            self._report_invalid_message(response, "Extracted message is invalid")
            return

        if self._include_response_metadata:
            receiver(
                HcsMessageWithResponseMetadata(
                    message=message,
                    sequence_number=response.sequence_number,
                    consensus_timestamp=Timestamp.from_jinstant(response.timestamp),
                )
            )
        else:
            receiver(message)

    def _extract_message(self, response: MirrorResponse) -> HcsMessage | None:
        try:
            return self._message_class.from_json(response.contents)
        except Exception as error:
            LOGGER.warning(f"Failed to extract HCS message from response: {error!s}")

    def _report_invalid_message(self, response: MirrorResponse, reason: str):
        LOGGER.warning(f"Got invalid message: {response.contents}, reason: {reason}")
        if self._invalid_message_handler:
            self._invalid_message_handler(response, reason)
