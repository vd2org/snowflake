# Copyright (C) 2021-2024 by Vd.
# This file is part of Snowflake package.
# Snowflake is released under the MIT License (see LICENSE).


from typing import Final, Tuple

from .snowflake import Snowflake, SnowflakeGenerator
from .snowflake import MAX_TS, MAX_SEQ, MAX_INSTANCE


VERSION: Final[str] = "v1.0.1"
__version__ = VERSION


def version() -> str:
    return VERSION


__all__: Final[Tuple[str, ...]] = (
    "Snowflake",
    "SnowflakeGenerator",
    "MAX_TS",
    "MAX_SEQ",
    "MAX_INSTANCE",
)
