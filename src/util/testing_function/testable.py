from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar
from .test_spec import LazyTestTarget

P = ParamSpec("P")
R = TypeVar("R")


def testable(func: Callable[P, R]) -> Callable[P, LazyTestTarget[R]]:
    """하나의 함수를 지연실행으로 변환

    사용법::

        @testable
        def slow_add(a, b):
            return a + b

        spec = TestSpec(
            test_target=slow_add(1, 2),
            test_count=100,
        )

        log = testing_function(spec)
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> LazyTestTarget[R]:
        return LazyTestTarget(func, args, kwargs)

    return wrapper
