from typing import Literal


def pattern_generator(size: int, shape: Literal["x", "+"]):
    """2차원 배열 x or + 생성 함수"""

    if size < 3 or size % 2 == 0 or shape not in ["x", "+"]:
        print("size는 1 이상의 홀수여야 하며, shape는 'x' 또는 '+'여야 합니다.")
        return

    mid = size // 2
    cond = {
        "+": lambda x, y: x == mid or y == mid,
        "x": lambda x, y: x == y or x + y == size - 1,
    }[shape]

    return [[1.0 if cond(x, y) else 0.0 for x in range(size)] for y in range(size)]
