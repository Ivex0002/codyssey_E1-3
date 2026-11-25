from data_class.type import PatternMatrix
from ..validate.validate_pattern import validate_pattern


def user_input_custom_pattern(size: int) -> PatternMatrix:
    while True:
        user_input: PatternMatrix = []

        for _ in range(size):
            row = list(map(float, input().split()))
            user_input.append(row)

        is_right_size = validate_pattern.is_right_size_pattern(size, user_input)

        if is_right_size:
            break
        else:
            print(
                f"입력된 행렬의 길이가 지정된 사이즈({size})와 다릅니다\n다시 입력해주세요"
            )
            continue

    return user_input
