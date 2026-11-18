def user_input_custom_pattern():

    user_input: list[list[float]] = []

    for _ in range(3):
        row = list(map(float, input().split()))
        user_input.append(row)

    return user_input
