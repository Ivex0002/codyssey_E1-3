from .check_int_user_input import check_int_user_input


# todo
def user_input_pattern():
    """size, shape를 입력받아 리턴해주는 함수"""
    while True:
        print("크기 : 3 이상의 홀수를 입력하세요")
        size = check_int_user_input(99)

        if size < 3 or size % 2 == 0:
            continue

    while True:
        shape = input("x 혹은 y를 입력해주세요\n선택 : ").strip()
        if shape not in ["x", "+"]:
            continue

    return {}
