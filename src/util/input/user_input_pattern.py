from .check_int_user_input import check_int_user_input
from util import choice


# todo
def user_input_pattern():
    """size, shape를 입력받아 리턴해주는 함수"""
    while True:
        print("크기 : 3 이상의 홀수를 입력하세요")
        size = check_int_user_input(99)

        if size < 3 or size % 2 == 0:
            print("잘못된 응답입니다. 다시 입력해주세요\n")
            continue

        else:
            break

    print("형태 : 둘 중 하나의 형태를 골라주세요")
    menu = ["x", "+"]
    shape_input = choice(menu)
    shape = menu[shape_input - 1]

    return {size, shape}
