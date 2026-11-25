from data_class.pattern_enum import PatternEnum, PatternInputData
from util import (
    check_int_user_input,
    choice,
    user_input_custom_pattern,
    user_input_simple_pattern,
    validate_pattern,
)


def user_inpt_pattern() -> PatternInputData:
    print("패턴, 필터의 크기를 3 이상의 홀수인 자연수로 입력해주세요(NxN)")
    while True:
        size = check_int_user_input(99, 3)
        is_right_size = validate_pattern.size(size)

        if is_right_size:
            break
        else:
            print("잘못된 입력입니다. 다시 입력해주세요\n")
            continue

    user_input: PatternInputData = {}

    for idx, item in enumerate(PatternEnum):
        print(f"[{idx+1}]{item.display_name}를 입력하세요")
        menu = ["직접입력", "패턴생성기 활용"]
        chosen_menu = choice(menu)

        if chosen_menu == 1:
            result = user_input_custom_pattern(size)
        else:
            result = user_input_simple_pattern(size)

        # match chosen_menu:
        #     case 1:
        #         result = user_input_custom_pattern(size)
        #     case 2:
        #         result = user_input_simple_pattern(size)
        #     case _:
        #         raise ValueError("잘못된 메뉴 선택")

        user_input[item.key] = result
    return user_input
