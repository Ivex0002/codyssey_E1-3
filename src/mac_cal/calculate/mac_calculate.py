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
from typing import Literal

CalMod = Literal["_1d", "_2d"]


@testable
def mac_calculate(
    filter_a: PatternMatrix,
    filter_b: PatternMatrix,
    pattern: PatternMatrix,
    cal_mod: CalMod = "_2d",
):

    validate_matrix_len([filter_a, filter_b, pattern])

    score_a = 0.0
    score_b = 0.0

    operation_count = 0

    match cal_mod:
        case "_2d":
            for y, row in enumerate(pattern):
                for x, value in enumerate(row):
                    score_a += filter_a[y][x] * value
                    score_b += filter_b[y][x] * value
                    operation_count += 1

        # _2d 대비 _1d 전환시 유의미하게 성능이 좋으려면
        # 기존 PatternMatrix 타입은 그대로 쓰면서 이걸 전환 로직까지 포함 하고도 성능상에 우위에 있어야 함
        # 굳이 PatternMatrix 타입 까지 변경 하면서 레거시 코드를 수정해야만 고성능을 보인다면 채용 가치는 적음
        case "_1d":
            fm_fa, fm_fb, fm_p = _flatten_matrices([filter_a, filter_b, pattern])
            for idx, value in enumerate(fm_p):
                score_a += fm_fa[idx] * value
                score_b += fm_fb[idx] * value
                operation_count += 1
        case _:
            raise ValueError(f"지원하지 않는 계산 모드: {cal_mod}")

    return score_a, score_b, operation_count


def validate_matrix_len(matrices: list[PatternMatrix]):
    """세 행렬의 구조와 크기가 동일한지 검사"""

    sizes = set()

    for idx, mat in enumerate(matrices):
        if not mat:
            raise ValueError(f"idx:{idx} 행렬이 비어 있습니다.")

        width = len(mat[0])

        if any(len(row) != width for row in mat):
            raise ValueError(f"idx:{idx} 행렬의 행 길이가 서로 다릅니다.")

        sizes.add((len(mat), width))

    if len(sizes) != 1:
        raise ValueError(f"세 행렬의 크기가 서로 다릅니다. " f"현재 크기: {sizes}")


def _flatten_matrices(pm_list: list[PatternMatrix]) -> list[list[float]]:
    my_list: list[list[float]] = []
    for pm in pm_list:
        result = []
        for row in pm:
            for value in row:
                result.append(value)
        my_list.append(result)
    return my_list
