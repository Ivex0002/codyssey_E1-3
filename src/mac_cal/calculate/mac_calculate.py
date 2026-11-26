# 예시
# #---------------------------------------
# # [3] MAC 결과
# #---------------------------------------
# A 점수: 1.0
# B 점수: 5.0
# 연산 시간(평균/10회): 0.012 ms
# 판정: B

# #---------------------------------------
# # [3] MAC 결과 (판정 불가)
# #---------------------------------------
# A 점수: 0.9000000000000000
# B 점수: 0.8999999999999999
# 판정: 판정 불가 (|A-B| < 1e-9)
from data_class.pattern_enum import PatternInputData, PatternKey
from util import testable, validate_pattern
from typing import Literal, TypeAlias

CalMod: TypeAlias = Literal["_1d", "_2d"]


_FlatData = list[float]
_FlatPatternData: TypeAlias = dict[PatternKey, _FlatData]


# @testable
def mac_calculate(
    pattern_data: PatternInputData,
    cal_mod: CalMod = "_2d",
):

    _validate_matrix_len(pattern_data)

    match cal_mod:
        case "_2d":
            return _2d_cal(pattern_data)

        case "_1d":
            flat_patterns = _flatten_matrices(pattern_data)
            return _1d_cal(flat_patterns)

        case _:
            raise ValueError(f"지원하지 않는 계산 모드: {cal_mod}")


@testable
def _1d_cal(flat_patterns: _FlatPatternData):
    score_a = 0.0
    score_b = 0.0

    operation_count = 0

    pattern, filter_a, filter_b = _get_flat(flat_patterns)
    for idx, value in enumerate(pattern):
        score_a += filter_a[idx] * value
        score_b += filter_b[idx] * value
        operation_count += 1

    return score_a, score_b, operation_count


@testable
def _2d_cal(pattern_data: PatternInputData):
    score_a = 0.0
    score_b = 0.0

    operation_count = 0

    pattern, filter_a, filter_b = _get_filter_pattern(pattern_data)

    for y, row in enumerate(pattern):
        for x, value in enumerate(row):
            score_a += filter_a[y][x] * value
            score_b += filter_b[y][x] * value
            operation_count += 1

    return score_a, score_b, operation_count


def _validate_matrix_len(pattern_data: PatternInputData):
    """세 행렬의 구조와 크기가 동일한지 검사"""

    for name, value in pattern_data.items():
        if not value:
            raise ValueError(f"{name}이 비어 있습니다.")

    pattern, filter_a, filter_b = _get_filter_pattern(pattern_data)
    _list = [pattern, filter_a, filter_b]

    # 1번 필터의 첫번째 row를 기준
    size = len(filter_a[0])

    for value in _list:
        if not validate_pattern.is_right_size_pattern(size, value):
            raise ValueError(f"길이가 다른 행렬이 존재합니다")


def _get_filter_pattern(pattern_data: PatternInputData):
    pattern = pattern_data["pattern"]
    filter_a = pattern_data["filter_a"]
    filter_b = pattern_data["filter_b"]
    return pattern, filter_a, filter_b


def _get_flat(flat_data: _FlatPatternData):
    pattern = flat_data["pattern"]
    filter_a = flat_data["filter_a"]
    filter_b = flat_data["filter_b"]
    return pattern, filter_a, filter_b


def _flatten_matrices(pattern_data: PatternInputData) -> _FlatPatternData:
    flat_patterns: _FlatPatternData = {}
    for name, matrix in pattern_data.items():
        result: _FlatData = []
        for row in matrix:
            result.extend(row)
        flat_patterns[name] = result
    return flat_patterns
