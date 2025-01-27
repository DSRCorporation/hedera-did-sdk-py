import pytest
from hedera import JInstant

from did_sdk_py.utils.timestamp import Timestamp


class TestTimestamp:
    def test_generate(self):
        timestamp = Timestamp.generate()

        assert isinstance(timestamp, Timestamp)
        assert timestamp.seconds > 0
        assert timestamp.nanos > 0

    def test_generate_without_collisions(self):
        timestamp_1 = Timestamp.generate()
        timestamp_2 = Timestamp.generate()
        timestamp_3 = Timestamp.generate()

        assert timestamp_1 != timestamp_2 and timestamp_1 != timestamp_3 and timestamp_2 != timestamp_3

    def test_from_jinstant(self):
        jinstant = JInstant.ofEpochSecond(1, 10)
        timestamp = Timestamp.from_jinstant(jinstant)

        assert isinstance(timestamp, Timestamp)
        assert timestamp.seconds == 1
        assert timestamp.nanos == 10

    def test_to_jinstant(self):
        timestamp = Timestamp(1, 10)
        jinstant = timestamp.to_jinstant()

        assert isinstance(jinstant, JInstant)
        assert jinstant.getEpochSecond() == 1
        assert jinstant.getNano() == 10

    @pytest.mark.parametrize(
        "seconds, nanos, expected_str",
        [
            (0, 0, "0.000000000"),
            (1, 1, "1.000000001"),
            (1, 10, "1.000000010"),
            (1123, 100, "1123.000000100"),
            (1123, 101, "1123.000000101"),
            (123456, 100100101, "123456.100100101"),
        ],
    )
    def test_to_str(self, seconds: int, nanos: int, expected_str: str):
        assert str(Timestamp(seconds, nanos)) == expected_str

    @pytest.mark.parametrize(
        "timestamp_1, timestamp_2, expected_comparison_result",
        [
            (Timestamp(0, 0), Timestamp(0, 0), True),
            (Timestamp(1, 10), Timestamp(1, 10), True),
            (Timestamp(1, 10), Timestamp(1, 11), False),
            (Timestamp(1, 10), Timestamp(2, 10), False),
            (Timestamp(1, 20), Timestamp(3, 40), False),
        ],
    )
    def test_eq(self, timestamp_1: Timestamp, timestamp_2: Timestamp, expected_comparison_result: bool):
        comparison_result = timestamp_1 == timestamp_2
        assert comparison_result == expected_comparison_result
