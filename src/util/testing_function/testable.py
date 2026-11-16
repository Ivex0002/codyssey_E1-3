from collections.abc import Callable
from functools import wraps
from .test_spec import LazyTestTarget


# 사용법
# @testable
# def slow_add(a, b):
#     return a + b
# spec = TestSpec(
#     test_target=slow_add(1, 2),
#     test_count=100,
# )
# log = testing_function(spec)
def testable(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> LazyTestTarget:
        return LazyTestTarget(func, args, kwargs)

    return wrapper
