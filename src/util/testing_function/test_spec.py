from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class LazyTestTarget(Generic[R]):
    def __init__(self, func: Callable[..., R], args: tuple, kwargs: dict):
        self.func = func
        self.args = args
        self.kwargs = kwargs

        # 함수명 자동 생성
        args_str = [repr(a) for a in args]
        kwargs_str = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        self.call_signature = f"{func.__name__}({', '.join(args_str + kwargs_str)})"

    def __call__(self) -> R:
        return self.func(*self.args, **self.kwargs)


@dataclass
class TestSpec(Generic[R]):
    """테스팅 함수용 인자를 묶어주는 클래스"""

    test_target: LazyTestTarget[R]
    test_count: int
    name: str | None = None

    # 인자 인스턴스 생성 시점에 검증
    def __post_init__(self):
        if not isinstance(self.test_target, LazyTestTarget):
            raise TypeError("test_target은 LazyTestTarget이어야 합니다.")
        if (
            isinstance(self.test_count, bool)
            or not isinstance(self.test_count, int)
            or self.test_count <= 0
        ):
            raise ValueError("test_count는 1 이상의 정수여야 합니다.")
        if self.name is not None and (
            not isinstance(self.name, str) or not self.name.strip()
        ):
            raise ValueError("name은 비어 있지 않은 문자열 혹은 None 이어야 합니다.")

    @property
    def resolved_name(self) -> str:
        return self.name if self.name is not None else self.test_target.call_signature

    def __iter__(self):
        yield self.test_target
        yield self.test_count
        yield self.name
