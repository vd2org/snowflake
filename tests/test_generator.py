# Copyright (C) 2021-2024 by Vd.
# This file is part of Snowflake package.
# Snowflake is released under the MIT License (see LICENSE).


from time import time

import pytest

from snowflake import Snowflake, SnowflakeGenerator
from snowflake import MAX_SEQ, MAX_INSTANCE


def test_generator():
    gen = SnowflakeGenerator.from_snowflake(Snowflake.parse(856165981072306191, 1288834974657))

    assert gen.epoch == 1288834974657

    val = next(gen)

    sf = Snowflake.parse(val, 1288834974657)

    assert sf.instance == 363
    assert sf.epoch == 1288834974657
    assert sf.seq == 0

    assert str(sf.timedelta) == "14917 days, 1:42:54.657000"

    assert sf.value == val

    assert int(sf) == val


def test_gen_many():
    gen = SnowflakeGenerator(MAX_INSTANCE - 1, epoch=4096)

    assert gen.epoch == 4096

    s = set()

    for _, val in zip(range(MAX_SEQ), gen):
        assert Snowflake.parse(val).timestamp > 0
        assert Snowflake.parse(val).instance == MAX_INSTANCE - 1
        s.add(val)

    assert len(s) == MAX_SEQ


def test_instance_overflow():
    SnowflakeGenerator(0)

    SnowflakeGenerator(MAX_INSTANCE)

    with pytest.raises(ValueError, match="instance must not be negative and must be less than 1023!"):
        SnowflakeGenerator(-1)

    with pytest.raises(ValueError, match="instance must not be negative and must be less than 1023!"):
        SnowflakeGenerator(MAX_INSTANCE + 1)


def test_seq_overflow():
    SnowflakeGenerator(0, seq=0)

    SnowflakeGenerator(0, seq=MAX_SEQ)

    with pytest.raises(ValueError, match="seq must not be negative and must be less than 4095!"):
        SnowflakeGenerator(0, seq=-1)

    with pytest.raises(ValueError, match="seq must not be negative and must be less than 4095!"):
        SnowflakeGenerator(0, seq=MAX_SEQ + 1)


def test_epoch_overflow():
    SnowflakeGenerator(0, epoch=0)

    SnowflakeGenerator(0, epoch=int(time() * 1000))

    with pytest.raises(ValueError, match=r"epoch must not be negative and must be lower than current time (\d+)!"):
        SnowflakeGenerator(0, epoch=-1)

    with pytest.raises(ValueError, match=r"epoch must not be negative and must be lower than current time (\d+)!"):
        SnowflakeGenerator(0, epoch=int(time() * 1000 + 10000))


def test_timestamp_overflow():
    SnowflakeGenerator(0, timestamp=0)

    SnowflakeGenerator(0, timestamp=int(time() * 1000))

    with pytest.raises(ValueError, match=r"timestamp must not be negative and must be less than (\d+)!"):
        SnowflakeGenerator(0, timestamp=-1)

    with pytest.raises(ValueError, match=r"timestamp must not be negative and must be less than (\d+)!"):
        SnowflakeGenerator(0, timestamp=int(time() * 1000 + 10000))
