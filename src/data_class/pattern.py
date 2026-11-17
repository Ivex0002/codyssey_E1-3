from dataclasses import dataclass
from typing import Literal
from util import pattern_generator


@dataclass
class Pattern:
    size: str
    shape: Literal["x", "+"]

    @property
    def show():
        return pattern_generator()
