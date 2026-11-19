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
from data_class.type import PatternMatrix
from util import testable


@testable
def mac_calculate(
    filter_a: PatternMatrix, filter_b: PatternMatrix, pattern: PatternMatrix
):

    validate_matrix_len([filter_a, filter_b, pattern])

    score_a = 0.0
    score_b = 0.0

    operation_count = 0

    for y, row in enumerate(pattern):
        for x, value in enumerate(row):
            score_a += filter_a[y][x] * value
            score_b += filter_b[y][x] * value
            operation_count += 1

    return score_a, score_b, operation_count


def validate_matrix_len(matrices: list[PatternMatrix]):
    """하나라도 행 길이 다르면 오류"""
    sizes = set()
    for idx, mat in enumerate(matrices):
        width = len(mat[0])
        if any(len(row) != width for row in mat):
            raise ValueError(f"idx:{idx} 의 행렬구조가 올바르지 않습니다.")
        sizes.add((len(mat), width))

    if len(sizes) != 1:
        raise ValueError("세 행렬의 크기가 서로 다릅니다.")
    return
