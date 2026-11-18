from enum import Enum
from typing import Literal, TypeAlias

PatternKey: TypeAlias = Literal["filter_a", "filter_b", "pattern"]

PatternInputData: TypeAlias = dict[PatternKey, list[list[float]]]


class PatternEnum(Enum):
    FILTER_A = ("filter_a", "필터 A")
    FILTER_B = ("filter_b", "필터 B")
    PATTERN = ("pattern", "패턴")

    def __init__(self, key: PatternKey, display_name: str) -> None:
        self.key: PatternKey = key
        self.display_name: str = display_name
