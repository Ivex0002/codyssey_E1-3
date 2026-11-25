from typing import TypeAlias, Literal

PatternMatrix: TypeAlias = list[list[float]]

PatternShape: TypeAlias = Literal["x", "+"]

# 런타임 값 검증용
PATTERN_SHAPES: tuple[PatternShape, ...] = ("x", "+")

PATTERN_SHAPE_NAME: dict[PatternShape, str] = {
    "x": "X",
    "+": "Cross",
}
