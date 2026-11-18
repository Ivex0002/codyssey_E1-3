from util import user_input_custom_pattern
from .pattern_enum import PatternEnum, PatternKey, PatternInputData


def custom_input() -> PatternInputData:
    """0, 1 등의 각 자리의 값을 입력받아 형태 배열을 리턴해주는 함수

    custom_input, simple_input 각각의 리턴 타입을 custom_input 기준으로 설정함"""
    user_input: PatternInputData = {}
    for idx, item in enumerate(PatternEnum):
        print(f"[{idx+1}]{item.display_name}를 입력하세요")
        result = user_input_custom_pattern()
        user_input[item.key] = result
    return user_input
