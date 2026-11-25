# # from util import user_input_simple_pattern
# from .pattern_enum import PatternEnum, PatternInputData


# # 리턴 타입 체킹
# def simple_input() -> PatternInputData:
#     """size, shape 를 입력받아 형태 배열을 리턴해주는 함수

#     형태 생성 파트를 분리하여 제작했으나 리턴 타입의 통일을 위해 아래와 같이 제작함"""
#     user_input: PatternInputData = {}
#     for idx, item in enumerate(PatternEnum):
#         print(f"[{idx+1}]{item.display_name}를 입력하세요")
#         result = user_input_simple_pattern()
#         user_input[item.key] = result.show
#     return user_input
