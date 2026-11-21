from dataclasses import dataclass
from typing import Literal

# from util import pattern_generator, validate_pattern
from util.pattern.pattern_generator import pattern_generator
from util.validate.validate_pattern import validate_pattern

PatternShape = Literal["x", "+"]


@dataclass
class SimplePattern:
    size: int
    shape: PatternShape

    def __post_init__(self):
        if not validate_pattern.size(self.size):
            raise ValueError("size는 3 이상의 홀수여야 합니다.")

        if not validate_pattern.shape(self.shape):
            raise ValueError("shape는 'x' 또는 '+'여야 합니다.")

    @property
    def show(self):
        return pattern_generator(self.size, self.shape)
