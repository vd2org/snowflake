# Copyright (C) 2021-2024 by Vd.
# This file is part of Snowflake package.
# Snowflake is released under the MIT License (see LICENSE).


from dataclasses import dataclass
from datetime import datetime, timedelta, tzinfo
from time import time
from typing import Final, Optional, Tuple


__all__: Final[Tuple[str, ...]] = (
    'Snowflake',
    'SnowflakeGenerator',
    'MAX_TS',
    'MAX_INSTANCE',
    'MAX_SEQ',
)


MAX_TS: Final[int] = 0b11111111111111111111111111111111111111111
MAX_INSTANCE: Final[int] = 0b1111111111
MAX_SEQ: Final[int] = 0b111111111111


@dataclass(frozen=True, slots=True)
class Snowflake:
    timestamp: int
    instance: int
    epoch: int = 0
    seq: int = 0

    def __post_init__(self):
        if self.epoch < 0:
            raise ValueError(f"epoch must be greater than 0!")

        if self.timestamp < 0 or self.timestamp > MAX_TS:
            raise ValueError(f"timestamp must not be negative and must be less than {MAX_TS}!")

        if self.instance < 0 or self.instance > MAX_INSTANCE:
            raise ValueError(f"instance must not be negative and must be less than {MAX_INSTANCE}!")

        if self.seq < 0 or self.seq > MAX_SEQ:
            raise ValueError(f"seq must not be negative and must be less than {MAX_SEQ}!")

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

    def datetime_tz(self, tz: Optional[tzinfo] = None) -> 'datetime':
        return datetime.fromtimestamp(self.seconds, tz=tz)

    @property
    def timedelta(self) -> timedelta:
        return timedelta(milliseconds=self.epoch)

    @property
    def value(self) -> int:
        return self.timestamp << 22 | self.instance << 12 | self.seq

    def __int__(self) -> int:
        return self.value


class SnowflakeGenerator:
    __slots__: Final[Tuple[str, ...]] = (
        "_epo",
        "_ts",
        "_inf",
        "_seq"
    )
    def __init__(self, instance: int, *, seq: int = 0, epoch: int = 0, timestamp: Optional[int] = None):

        current = (time() * 1000.).__int__()

        if current - epoch >= MAX_TS:
            raise OverflowError(f"The maximum current timestamp has been reached in selected epoch,"
                                f"so Snowflake cannot generate more IDs!")

        _timestamp: int = timestamp or current

        if _timestamp < 0 or _timestamp > current:
            raise ValueError(f"timestamp must not be negative and must be less than {current}!")

        if epoch < 0 or epoch > current:
            raise ValueError(f"epoch must not be negative and must be lower than current time {current}!")

        self._epo: int = epoch
        self._ts: int = _timestamp - self._epo

        if instance < 0 or instance > MAX_INSTANCE:
            raise ValueError(f"instance must not be negative and must be less than {MAX_INSTANCE}!")

        if seq < 0 or seq > MAX_SEQ:
            raise ValueError(f"seq must not be negative and must be less than {MAX_SEQ}!")

        self._inf: int = instance << 12
        self._seq: int = seq

    @classmethod
    def from_snowflake(cls, sf: Snowflake) -> 'SnowflakeGenerator':
        return cls(sf.instance, seq=sf.seq, epoch=sf.epoch, timestamp=sf.timestamp)

    @property
    def epoch(self) -> int:
        return self._epo

    def __iter__(self):
        return self

    def __next__(self) -> Optional[int]:
        current = (time() * 1000.).__int__() - self._epo

        if current >= MAX_TS:
            raise OverflowError(f"The maximum current timestamp has been reached in selected epoch,"
                                f"so Snowflake cannot generate more IDs!")

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