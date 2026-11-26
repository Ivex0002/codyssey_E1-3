## 1. 시뮬레이터 최적화
[데이터 평탄화 분기 처리 + MAC 계산 함수](../src/mac_cal/calculate/mac_calculate.py)
- 2차원 배열을 1차원 배열로 전환하여 연산하는 로직입니다
- 정확한 함수간의 연산 능력 비교를 위해 각각의 테스트 범위는 전처리 과정을 거친 데이터를 연산하는 함수 1개로 한정했습니다

<details>
<summary>연산 함수 분기 로직</summary>

```
CalMod: TypeAlias = Literal["_1d", "_2d"]

def mac_calculate(
    pattern_data: PatternInputData,
    cal_mod: CalMod = "_2d",
):

    _validate_matrix_len(pattern_data)

    match cal_mod:
        case "_2d":
            return _2d_cal(pattern_data)

        case "_1d":
            flat_patterns = _flatten_matrices(pattern_data)
            return _1d_cal(flat_patterns)

        case _:
            raise ValueError(f"지원하지 않는 계산 모드: {cal_mod}")


@testable
def _1d_cal(flat_patterns: _FlatPatternData):
    score_a = 0.0
    score_b = 0.0

    operation_count = 0

    pattern, filter_a, filter_b = _get_flat(flat_patterns)
    for idx, value in enumerate(pattern):
        score_a += filter_a[idx] * value
        score_b += filter_b[idx] * value
        operation_count += 1

    return score_a, score_b, operation_count


@testable
def _2d_cal(pattern_data: PatternInputData):
    score_a = 0.0
    score_b = 0.0

    operation_count = 0

    pattern, filter_a, filter_b = _get_filter_pattern(pattern_data)

    for y, row in enumerate(pattern):
        for x, value in enumerate(row):
            score_a += filter_a[y][x] * value
            score_b += filter_b[y][x] * value
            operation_count += 1

    return score_a, score_b, operation_count
```

- 인자로 전달된 `CalMod` 에 따라 각각 다른 함수를 전달해주는 로직입니다
- 각각의 함수 비교를 위해 2차원 배열을 1차원으로 평탄화 하는 작업은 테스트에서 제외했습니다

### 연산량 분석

- 패턴의 가로와 세로 크기가 각각 \(N\)인 정사각형 행렬을 기준으로 연산량을 분석했습니다.

- 각 연산 함수는 패턴의 모든 원소를 한 번씩 순회하며, 순회할 때마다 두 개의 필터에 대한 MAC 연산을 수행합니다.

- 따라서 전체 반복 횟수는 다음과 같습니다.

\[
T(N) = \sum_{y=0}^{N-1}\sum_{x=0}^{N-1}1 = N^2
\]

- **2차원 배열 (`_2d_cal`)**: 중첩 반복문을 통해 총 \(N^2\)개의 원소를 순회합니다.
- **1차원 배열 (`_1d_cal`)**: 평탄화된 배열의 길이인 \(N^2\)만큼 순회합니다.

두 함수 모두 동일한 \(N^2\)개의 원소를 처리하므로 이론적인 시간 복잡도는 동일하게 \(O(N^2)\)입니다.

※ `operation_count`는 개별 산술 연산의 횟수가 아닌, MAC 연산을 수행한 원소의 처리 횟수를 의미합니다.

</details>


<details>
<summary>@testable 유틸 함수</summary>

```
def testable(func: Callable[P, R]) -> Callable[P, LazyTestTarget[R]]:
    """하나의 함수를 지연실행으로 변환"""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> LazyTestTarget[R]:
        return LazyTestTarget(func, args, kwargs)

    return wrapper
```
```
# 테스트 로그용 전환 클래스
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
```
```
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
    target: LazyTestTarget[R], test_count: int, name: str | None = None
) -> TestLog:
    """편의용 함수

    TestSpec 자동 래핑"""
    return testing_function(TestSpec(target, test_count, name))
```

- 위의 함수로 특정 함수 1개를 wrap 함으로써 `@testable` 데코레이션 호출 1회만으로 성능 데이터를 간편하게 받아 볼 수 있습니다
- 필요 이상의 기능을 넣은 이유는 추후에 테스트 로그들을 장기 저장할 필요가 있을 경우에 대비하기 위해서 입니다
- 각각의 테스트를 실행한 타겟 함수명과 인자를 같이 저장하여 테스트 로그 이름으로 저장합니다

```
cal_result = mac_calculate(
  user_input,
  self.what_d,
)

try:
  # 1회 실행 결과를 저장
  score_a, score_b, _count = cal_result()
  # 10회 연산 평균을 로그로 저장
  result_log = quick_test(cal_result, test_count=10)
  print_result(score_a, score_b, result_log)

(중략)
```
- 당장은 위와 같이 단순하게 `quick_test` 함수에 target을 `TestSpec`으로 지연함수로 전처리 과정을 주어 결과값으로 [테스트 로그](../src/util/testing_function/test_log.py)를 넘겨줍니다
- 테스트 로그에서는 전체 시간, 각각의 테스트 1회의 시간을 따로 살펴 볼 수 있습니다
- 현재 코드는 10회의 테스트 평균을 내기 위해 각각의 단일 테스트들의 합계와 테스트 횟수를 기반으로 작성했습니다
  
</details>

<details>
<summary>결과 로그</summary>

```
#---------------------------------------
[3] 성능 분석 (평균/10회)
데이터 평탄화 모드 : _2d
#---------------------------------------
크기           평균 시간(ms)       연산 횟수
----------------------------------
size_5_1         0.008          25
size_5_2         0.007          25
size_5_3         0.007          25
size_13_1        0.026         169
size_13_2        0.023         169
size_25_1        0.105         625
size_25_2        0.097         625

(중략)

#---------------------------------------
[3] 성능 분석 (평균/10회)
데이터 평탄화 모드 : _1d
#---------------------------------------
크기           평균 시간(ms)       연산 횟수
----------------------------------
size_5_1         0.007          25
size_5_2         0.006          25
size_5_3         0.004          25
size_13_1        0.027         169
size_13_2        0.023         169
size_25_1        0.058         625
size_25_2        0.057         625
```

- 위의 연산 결과를 토대로 1d로 평탄화를 거친 연산이 비교적 빠름을 확인 할 수 있습니다

</details>

## 2. 패턴 생성기
[패턴 생성 함수](../src/util/pattern/pattern_generator.py)
- 크기, 모양을 입력받아 실제 패턴을 리턴해주는 함수입니다.
- 요구 사항대로 Cross, X 패턴을 자동적으로 생성해줍니다
- 해당 함수로 생성된 패턴은 모드 1에서 활용됩니다.

<details>
<summary>유저 실행 흐름</summary>

```
$ python -m main
===Mini NPU Simulator===
모드를 선택해주세요


1. 사용자 입력
2. data.json 분석
3. 배열 평탄화 모드
4. 종료
선택: 1


1. 3x3
2. 패턴 생성기(보너스)
선택: 2
[1]필터 A를 입력하세요
크기 : 3 이상의 홀수를 입력하세요
선택: 13
형태 : 둘 중 하나의 형태를 골라주세요


1. x
2. +
선택: 1
[2]필터 B를 입력하세요
크기 : 3 이상의 홀수를 입력하세요
선택: 13
형태 : 둘 중 하나의 형태를 골라주세요


1. x
2. +
선택: 2
[3]패턴를 입력하세요
크기 : 3 이상의 홀수를 입력하세요
선택: 13
형태 : 둘 중 하나의 형태를 골라주세요


1. x
2. +
선택: 1
===filter_a===
1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0
0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0
0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0
0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0
0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0
0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0
1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0
===filter_b===
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
===pattern===
1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0
0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0
0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0
0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0
0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0
0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0
0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0
1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0
입력된 값은 위와 같습니다
MAC 연산을 실행합니다

#---------------------------------------
MAC 결과
#---------------------------------------
A 점수: 25.0
B 점수: 1.0
연산 시간(평균/10회): 0.029 ms
판정: A
```

</details>
