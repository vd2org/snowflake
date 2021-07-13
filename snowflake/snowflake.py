# Copyright (C) 2021 by Ivan.
# This file is part of Snowflake package.
# Snowflake is released under the MIT License (see LICENSE).


from dataclasses import dataclass
from time import time
from typing import Optional
from datetime import datetime, timedelta, tzinfo

__all__ = ('Snowflake', 'SnowflakeGenerator')

MAX_TS = 0b11111111111111111111111111111111111111111
MAX_INSTANCE = 0b1111111111
MAX_SEQ = 0b111111111111


@dataclass(frozen=True)
class Snowflake:
    timestamp: int
    instance: int
    epoch: int = 0
    seq: int = 0

    def __post_init__(self):
        if self.epoch < 0:
            raise ValueError(f"epoch must be greater than 0!")

        if self.timestamp < 0 or self.timestamp > MAX_TS:
            raise ValueError(f"timestamp must be greater than 0 and less than {MAX_TS}!")

        if self.instance < 0 or self.instance > MAX_INSTANCE:
            raise ValueError(f"instance must be greater than 0 and less than {MAX_INSTANCE}!")

        if self.seq < 0 or self.seq > MAX_SEQ:
            raise ValueError(f"seq must be greater than 0 and less than {MAX_SEQ}!")

    @classmethod
    def parse(cls, snowflake: int, epoch: int = 0) -> 'Snowflake':
        return cls(
            epoch=epoch,
            timestamp=snowflake >> 22,
            instance=snowflake >> 12 & MAX_INSTANCE,
            seq=snowflake & MAX_SEQ
        )

    @property
    def milliseconds(self) -> int:
        return self.timestamp + self.epoch

    @property
    def seconds(self) -> float:
        return self.milliseconds / 1000

    @property
    def datetime(self) -> datetime:
        return datetime.utcfromtimestamp(self.seconds)

    def datetime_tz(self, tz: Optional[tzinfo] = None) -> datetime:
        return datetime.fromtimestamp(self.seconds, tz=tz)

    @property
    def timedelta(self) -> timedelta:
        return timedelta(milliseconds=self.epoch)

    @property
    def value(self) -> int:
        return self.timestamp << 22 | self.instance << 12 | self.seq


class SnowflakeGenerator:
    def __init__(self, instance: int, *, seq: int = 0, epoch: int = 0, timestamp: Optional[int] = None):

        current = int(time() * 1000)

        if current >= MAX_TS:
            raise OverflowError(f"The maximum timestamp has been reached in selected epoch,"
                                f"so Snowflake cannot generate more IDs!")

        timestamp = timestamp or current

        if timestamp < 0 or timestamp > current:
            raise ValueError(f"timestamp must be greater than 0 and less than {current}!")

        if epoch < 0 or epoch > current:
            raise ValueError(f"epoch must be greater than 0 and lower than current time {current}!")

        self._epo = epoch
        self._ts = timestamp - self._epo

        if instance < 0 or instance > MAX_INSTANCE:
            raise ValueError(f"instance must be greater than 0 and less than {MAX_INSTANCE}!")

        if seq < 0 or seq > MAX_SEQ:
            raise ValueError(f"seq must be greater than 0 and less than {MAX_SEQ}!")

        self._inf = instance << 12
        self._seq = seq

    @classmethod
    def from_snowflake(cls, sf: Snowflake) -> 'SnowflakeGenerator':
        return cls(sf.instance, seq=sf.seq, epoch=sf.epoch, timestamp=sf.timestamp)

    @property
    def epoch(self) -> int:
        return self._epo

    def __iter__(self):
        return self

    def __next__(self) -> Optional[int]:
        current = int(time() * 1000) - self._epo

        if self._ts == current:
            if self._seq == MAX_SEQ:
                return None
            self._seq += 1
        elif self._ts > current:
            return None
        else:
            self._seq = 0

        self._ts = current

        return self._ts << 22 | self._inf | self._seq
