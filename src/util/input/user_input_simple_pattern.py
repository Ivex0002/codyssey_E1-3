from data_class.type import PatternMatrix, PatternShape
from data_class.simple_pattern import SimplePattern
from ..input.choice import choice


def user_input_simple_pattern(size: int) -> PatternMatrix:
    menu: list[PatternShape] = ["x", "+"]
    print("아래에 기입된 형태 중 하나를 번호로 선택해주세요")

    chosen_menu = menu[choice(menu) - 1]

    return SimplePattern(size, chosen_menu).show
