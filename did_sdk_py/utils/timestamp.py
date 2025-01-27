import random
import time
from dataclasses import dataclass

from hedera import JInstant

# Used to improve collision-safety (approach is based on JS SDK implementation)
generated_ids: set[str] = set()


@dataclass
class Timestamp:
    seconds: float
    nanos: float

    @classmethod
    def generate(cls):
        jitter = random.randint(0, 5000) + 8000  # noqa: S311
        now = int(time.time() * 1000) - jitter
        seconds = now // 1000
        nanos = (now % 1000) * 1000000 + random.randint(0, 1000000)  # noqa: S311

        timestamp = cls(seconds, nanos)
        if str(timestamp) in generated_ids:
            return Timestamp.generate()
        else:
            generated_ids.add(str(timestamp))
            return timestamp

    @classmethod
    def from_jinstant(cls, jinstant: JInstant):
        return cls(jinstant.getEpochSecond(), jinstant.getNano())

    def to_jinstant(self) -> JInstant:
        return JInstant.ofEpochSecond(self.seconds, self.nanos)

    def __str__(self):
        zero_padded_nanos = str(self.nanos).rjust(9, "0")
        return f"{self.seconds!s}.{zero_padded_nanos}"

    def __eq__(self, other):
        return self.seconds == other.seconds and self.nanos == other.nanos
