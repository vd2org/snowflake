# Copyright (C) 2021-2024 by Vd.
# This file is part of Snowflake package.
# Snowflake is released under the MIT License (see LICENSE).


from datetime import tzinfo, timedelta

import pytest

from snowflake import Snowflake
from snowflake import MAX_TS, MAX_SEQ, MAX_INSTANCE


def test_parse():
    class UTC0531(tzinfo):
        _offset = timedelta(seconds=19860)
        _dst = timedelta(0)

        def utcoffset(self, dt):
            return self.__class__._offset

        def dst(self, dt):
            return self.__class__._dst

    sf = Snowflake.parse(856165981072306191, 1288834974657)

    assert sf.timestamp == 204125876682
    assert sf.instance == 363
    assert sf.epoch == 1288834974657
    assert sf.seq == 15

    assert sf.seconds == 1492960851.339
    assert sf.milliseconds == 1492960851339

    assert str(sf.datetime) == "2017-04-23 15:20:51.339000"
    assert str(sf.datetime_tz(UTC0531())) == "2017-04-23 20:51:51.339000+05:31"

    assert str(sf.timedelta) == "14917 days, 1:42:54.657000"

    assert sf.value == 856165981072306191

    assert int(sf) == 856165981072306191


def test_min():
    assert Snowflake(0, 0).value == 0


def test_max():
    assert Snowflake(MAX_TS, MAX_INSTANCE, seq=MAX_SEQ).value == 9223372036854775807


def test_timestamp_overflow():
    Snowflake(0, 0)

    Snowflake(MAX_TS, 0)

    with pytest.raises(ValueError, match="timestamp must not be negative and must be less than 2199023255551!"):
        Snowflake(MAX_TS + 1, 0)

    with pytest.raises(ValueError, match="timestamp must not be negative and must be less than 2199023255551!"):
        Snowflake(-1, 0)


def test_instance_overflow():
    Snowflake(0, 0)

    Snowflake(0, MAX_INSTANCE)

    with pytest.raises(ValueError, match="instance must not be negative and must be less than 1023!"):
        Snowflake(0, -1)

    with pytest.raises(ValueError, match="instance must not be negative and must be less than 1023!"):
        Snowflake(0, MAX_INSTANCE + 1)


def test_epoch_overflow():
    Snowflake(0, 0, epoch=0)

    with pytest.raises(ValueError, match="epoch must be greater than 0!"):
        Snowflake(0, 0, epoch=-1)


def test_seq_overflow():
    Snowflake(0, 0, seq=0)

    Snowflake(0, 0, seq=MAX_SEQ)

    with pytest.raises(ValueError, match="seq must not be negative and must be less than 4095!"):
        Snowflake(0, 0, seq=-1)

    with pytest.raises(ValueError, match="seq must not be negative and must be less than 4095!"):
        Snowflake(0, 0, seq=MAX_SEQ + 1)
