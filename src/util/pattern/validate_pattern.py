class ValidatePattern:
    @staticmethod
    def size(size: int) -> bool:
        return size < 3 or size % 2 == 0

    @staticmethod
    def shape(shape: str) -> bool:
        return shape not in ("x", "+")


validate_pattern = ValidatePattern()
