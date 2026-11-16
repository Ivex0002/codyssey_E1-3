from datetime import datetime
from .test_log import TestLog, SingleTest
from .test_spec import TestSpec, LazyTestTarget


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


def testing_function(spec: TestSpec) -> TestLog:
    """테스트 함수

    ! 반드시 `TestSpec` 으로 인자 전달 필요(지연함수 자동 네이밍) !"""
    start_time = _now()
    tests: list[SingleTest] = []

    for _ in range(spec.test_count):
        s = _now()
        spec.test_target()
        e = _now()
        tests.append(SingleTest(s, e))

    end_time = _now()
    return TestLog(start_time, end_time, spec.resolved_name, tests)


def quick_test(
    target: LazyTestTarget, test_count: int, name: str | None = None
) -> TestLog:
    """편의용 함수

    TestSpec 자동 래핑"""
    return testing_function(TestSpec(target, test_count, name))
