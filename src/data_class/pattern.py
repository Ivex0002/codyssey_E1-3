from dataclasses import dataclass
from typing import Literal
from util import pattern_generator, validate_pattern


@dataclass
class Pattern:
    size: int
    shape: Literal["x", "+"]

    def __post_init__(self):
        if not validate_pattern.size(self.size):
            raise ValueError("size는 3 이상의 홀수여야 합니다.")

        if not validate_pattern.shape(self.shape):
            raise ValueError("shape는 'x' 또는 '+'여야 합니다.")

    @property
    def show(self):
        return pattern_generator(self.size, self.shape)
