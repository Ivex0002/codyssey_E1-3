from .check_int_user_input import check_int_user_input
from util import choice, validate_pattern
from data_class.simple_pattern import SimplePattern, PatternShape

_wrong_input_msg = "잘못된 응답입니다. 다시 입력해주세요\n"


def _get_valid_input(prompt, input_func, validator):
    while True:
        print(prompt)
        value = input_func()

        if validator(value):
            return value

        print(_wrong_input_msg)


def user_input_simple_pattern():
    """size, shape를 입력받아 리턴해주는 함수"""

    size = _get_valid_input(
        "크기 : 3 이상의 홀수를 입력하세요",
        lambda: check_int_user_input(99),
        validate_pattern.size,
    )

    menu: list[PatternShape] = ["x", "+"]
    shape = _get_valid_input(
        "형태 : 둘 중 하나의 형태를 골라주세요",
        lambda: menu[choice(menu) - 1],
        validate_pattern.shape,
    )

    return SimplePattern(size, shape)
