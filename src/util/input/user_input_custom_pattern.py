from data_class.type import PatternMatrix


def user_input_custom_pattern() -> PatternMatrix:

    user_input: PatternMatrix = []

    for _ in range(3):
        row = list(map(float, input().split()))
        user_input.append(row)

    return user_input
