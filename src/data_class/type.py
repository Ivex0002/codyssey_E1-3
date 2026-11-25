from typing import TypeAlias, Literal

PatternMatrix: TypeAlias = list[list[float]]

PatternShape = Literal["x", "+"]

PATTERN_SHAPE_NAME: dict[PatternShape, str] = {
    "x": "X",
    "+": "Cross",
}
