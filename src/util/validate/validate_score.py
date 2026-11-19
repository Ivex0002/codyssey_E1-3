from util import TestLog


def validate_score(score_a: float, score_b: float, result_log: TestLog):
    """점수 판정용 유틸함수

    2가지 점수와 판정 로그들을 입력받고

    판정 결과, 평균 계산 시간을 출력"""
    can_cal = abs(score_a - score_b) >= 1e-9
    sum_test_time = sum((test.end_time - test.start_time) for test in result_log.tests)
    cal_time = sum_test_time / len(result_log.tests) / 1_000_000

    return can_cal, cal_time
