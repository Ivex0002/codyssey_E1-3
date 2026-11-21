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

from ..testing_function.test_log import TestLog
from ..validate.validate_score import validate_score


def print_result(score_a: float, score_b: float, result_log: TestLog):
    can_cal, cal_time = validate_score(score_a, score_b, result_log)

    print(line)
    print(result_msg + "" if can_cal else cant_cal_msg)
    print(line)
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")

    if can_cal:
        result = "A" if score_a > score_b else "B"
        print(f"연산 시간(평균/{result_log.test_count}회): {cal_time:.3f} ms")
        print(f"판정: {result}")
    else:
        print(cant_cal_result_msg)


line = "#---------------------------------------"
result_msg = "MAC 결과"
cant_cal_msg = " (판정 불가)"
cant_cal_result_msg = "판정 불가 (|A-B| < 1e-9)"
