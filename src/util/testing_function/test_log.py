from dataclasses import dataclass, asdict


@dataclass
class SingleTest:
    start_time: int
    end_time: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TestLog:
    """저장/로드용 테스팅 로그 클래스"""

    start_time: int
    end_time: int
    name: str
    tests: list[SingleTest]

    @property
    def test_count(self):
        return len(self.tests)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["test_count"] = self.test_count
        return data
