from data_class.type import PATTERN_SHAPES, PatternMatrix


class ValidatePattern:
    @staticmethod
    def size(size: int) -> bool:
        # print(f"debug: {size}")
        return size >= 3 and size % 2 == 1

    @staticmethod
    def shape(shape: str) -> bool:
        # print(f"debug: {shape}")
        return shape in PATTERN_SHAPES

    @staticmethod
    def is_right_size_pattern(size: int, pattern: PatternMatrix) -> bool:
        return len(pattern) == size and all(len(row) == size for row in pattern)


validate_pattern = ValidatePattern()
"""해당 패턴의 크기가 3 이상 및 홀수 여부, 모양이 +, x인지 여부"""
