from data_class.type import PatternMatrix


def user_input_custom_pattern(size: int) -> PatternMatrix:

    user_input: PatternMatrix = []

    for _ in range(size):
        row = list(map(float, input().split()))
        user_input.append(row)

    return user_input
