import pytest

from did_sdk_py.did.hcs.events.document.hcs_did_delete_event import HcsDidDeleteEvent
from did_sdk_py.did.hcs.events.hcs_did_event_target import HcsDidEventTarget


@pytest.fixture()
def event():
    return HcsDidDeleteEvent()


class TestHcsDidDeleteEvent:
    def test_targets_did_doc(self, event):
        "targets DID document" ""
        assert event.event_target == HcsDidEventTarget.DOCUMENT

    def test_retuns_event_object(self, event):
        """returns event object"""
        event_from_json = event.from_json_payload({"Document": {}})

        assert isinstance(event_from_json, HcsDidDeleteEvent)
