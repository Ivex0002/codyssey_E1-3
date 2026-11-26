from typing import TypeAlias, Literal, TypedDict
from data_class.type import PatternMatrix, PatternShape
from data_class.pattern_enum import PatternInputData
from .mac_calculate import mac_calculate, CalMod
from util import validate_score, quick_test

# data.json 파싱용 편의 함수
# 외부에선 쓰일 일이 없으므로 내부 타입으로 지정
# 제공된 data.json에서 필터와 패턴이 각각 구조가 다르므로 따로 제작

# 필터
_FilterShape: TypeAlias = Literal["cross", "x"]
_FilterData: TypeAlias = dict[_FilterShape, PatternMatrix]
_FilterCollection: TypeAlias = dict[str, _FilterData]


# 패턴
class _PatternData(TypedDict):
    input: PatternMatrix
    expected: PatternShape


_PatternCollection: TypeAlias = dict[str, _PatternData]


# 패턴과 필터를 담은 데이터
_MetaKey: TypeAlias = Literal["version", "type"]
_MetaData: TypeAlias = dict[_MetaKey, str]


class DataJson(TypedDict):
    filters: _FilterCollection
    patterns: _PatternCollection
    meta: _MetaData


# 데이터 정규화
# filter:pattern
PATTERN_MAP: dict[_FilterShape, PatternShape] = {
    "cross": "+",
    "x": "x",
}


# 테스트 로그 세이브 변수
class _TestLogSave(TypedDict):
    avg: float
    cnt: int
    is_pass: bool
    fail_rsn: str | None


def data_json_cal(data: DataJson | None, what_d: CalMod):
    if not data:
        raise ValueError("data.json은 유효한 파일이 아닙니다")

    filters: _FilterCollection = data["filters"]
    patterns: _PatternCollection = data["patterns"]

    _big_label("[1] 필터 로드")
    for size, shapes in filters.items():
        shape_names = ", ".join(shape.capitalize() for shape in shapes)
        print(f"✓ {size} 필터 로드 완료 ({shape_names})")

    _big_label("[2] 패턴 분석")

    # [3] 성능 분석용 변수
    test_log_saves: dict[str, _TestLogSave] = {}

    for size, pattern in patterns.items():
        _small_label(size)
        found_filter = filters[_size_for_filter(size)]
        pattern_data: PatternInputData = {
            "filter_a": found_filter["cross"],
            "filter_b": found_filter["x"],
            "pattern": pattern["input"],
        }

        result = mac_calculate(pattern_data, what_d)
        try:
            score_cross, score_x, operation_count = result()
            _print_score(score_cross, score_x)
            result_log = quick_test(result, test_count=10)
            can_cal, cal_time = validate_score(score_cross, score_x, result_log)

            if can_cal:
                jud = PATTERN_MAP["cross" if score_cross > score_x else "x"]
                is_pass = jud == pattern["expected"]
                fail_rsn = None if is_pass else "기대 결과와 판정 결과 불일치"
                _print_jud(jud, pattern["expected"])
            else:
                is_pass = False
                fail_rsn = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
                _print_jud(None, pattern["expected"])

            # 저장
            test_log_saves[size] = {
                "avg": cal_time,
                "cnt": operation_count,
                "is_pass": is_pass,
                "fail_rsn": fail_rsn,
            }
        # data.json에 서로 길이가 다른 패턴/필터가 입력될경우
        except ValueError as e:
            print(f"MAC 연산 오류: {e}")
            test_log_saves[size] = {
                "avg": 0.0,
                "cnt": 0,
                "is_pass": False,
                "fail_rsn": str(e),
            }

    _big_label(f"[3] 성능 분석 (평균/10회)\n데이터 평탄화 모드 : {what_d}")
    print(f"{'크기':<10}{'평균 시간(ms)':>12}{'연산 횟수':>12}")
    print("-" * 34)
    for size, log in test_log_saves.items():
        print(f"{size:<10}{log['avg']:>12.3f}{log['cnt']:>12}")

    _big_label("[4] 결과 요약")

    total = len(test_log_saves)
    passed = sum(log["is_pass"] for log in test_log_saves.values())
    failed = total - passed
    print(f"총 테스트: {len(test_log_saves)}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")
    print(f"실패 케이스:")
    for size, log in test_log_saves.items():
        if not log["is_pass"]:
            print(f"- {size} : {log['fail_rsn']}")
    return


line = "#---------------------------------------"


def _big_label(str: str):
    print(line)
    print(str)
    print(line)


def _small_label(str: str):
    print(f"\n---{str}---")


def _size_for_filter(pattern_size: str):
    return pattern_size.rsplit("_", 1)[0]


def _print_score(score_cross: float, score_x: float):
    print(f"Cross 점수 : {score_cross}")
    print(f"X 점수 : {score_x}")


def _print_jud(jud: str | None, exp: str):
    if jud is None:
        print(f"판정: UNDECIDED | expected: {exp} | FAIL")
        return

    status = "PASS" if jud.lower() == exp.lower() else "FAIL"
    print(f"판정: {jud} | expected: {exp} | {status}")
