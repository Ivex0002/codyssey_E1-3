from .pattern_enum import PatternEnum, PatternInputData
from util import (
    check_int_user_input,
    choice,
    user_input_custom_pattern,
    user_input_simple_pattern,
)


def user_inpt_pattern() -> PatternInputData:
    print("패턴, 필터의 크기를 3 이상의 자연수로 입력해주세요(NxN)")
    size = check_int_user_input(99, 3)
    user_input: PatternInputData = []

    for idx, item in enumerate(PatternEnum):
        print(f"[{idx+1}]{item.display_name}를 입력하세요")
        menu = ["직접입력", "패턴생성기 활용"]
        chosen_menu = choice(menu)

        match chosen_menu:
            case 1:
                result = user_input_custom_pattern(size)
            case 2:
                result = user_input_simple_pattern(size)

        user_input[item.key] = result
    return user_input
