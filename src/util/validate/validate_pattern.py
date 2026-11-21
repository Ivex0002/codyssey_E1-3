class ValidatePattern:
    @staticmethod
    def size(size: int) -> bool:
        return size < 3 or size % 2 == 0

    @staticmethod
    def shape(shape: str) -> bool:
        return shape not in ("x", "+")


validate_pattern = ValidatePattern()
"""해당 패턴의 크기가 3 이상 및 홀수 여부, 모양이 +, x인지 여부"""
