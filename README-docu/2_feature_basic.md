## 1. 데이터 구조

[패턴 제너레이터를 활용한 패턴 클래스](../src/data_class/simple_pattern.py)

패턴 장기 저장시에 모든 값들을 저장하게 되면 메모리 비효율이 매우 커지므로, 단순화 가능한 항목들을 최대한 줄여 크기, 모양만을 입력받아 저장하도록 했습니다

이를 실제 값으로 치환하기 위해 [패턴 제너레이터 함수](../src/util/pattern/pattern_generator.py) 를 필요할때만 호출하도록 구성했습니다.

## 2. 모드 1 입력 처리(NxN)

[NxN 유저 입력 받기](../src/mac_cal/handle_user_input_pattern/user_inpt_pattern.py)

<details>
<summary>모드 1 유저 실행 흐름 예시</summary>
  
```
===Mini NPU Simulator===
모드를 선택해주세요

1. 사용자 입력
2. data.json 분석
3. 배열 평탄화 모드
4. 종료
   선택: 1
   패턴, 필터의 크기를 3 이상의 홀수인 자연수로 입력해주세요(NxN)
   선택: 3
   [1]필터 A를 입력하세요

5. 직접입력
6. 패턴생성기 활용
   선택: 1
   1 0 1
   0 1 0
   1 0 1
   [2]필터 B를 입력하세요

7. 직접입력
8. 패턴생성기 활용
   선택: 2
   아래에 기입된 형태 중 하나를 번호로 선택해주세요

9. x
10. - 선택: 2
      [3]패턴를 입력하세요

11. 직접입력
12. 패턴생성기 활용
    선택: 1
    1 0 1
    0 0 0
    1 0 1
    ===filter_a===
    1.0 0.0 1.0
    0.0 1.0 0.0
    1.0 0.0 1.0
    ===filter_b===
    0.0 1.0 0.0
    1.0 1.0 1.0
    0.0 1.0 0.0
    ===pattern===
    1.0 0.0 1.0
    0.0 0.0 0.0
    1.0 0.0 1.0
    입력된 값은 위와 같습니다
    MAC 연산을 실행합니다

#---------------------------------------
MAC 결과
#---------------------------------------
A 점수: 4.0
B 점수: 0.0
연산 시간(평균/10회): 0.006 ms
판정: A

```

</details>

## 3. 모드 2 JSON 로드 및 스키마 검증(data.json)
[data.json 파싱 및 계산 로직](../src/mac_cal/calculate/data_json_cal.py)
- `patterns의 각 항목에 대해, 키에서 N을 추출하여 해당 size_N 필터를 선택해야 한다` 라고 요구조건에 나와 있었으나, 이는 굳이 N으로 따로 저장할 필요가 없다고 판단했습니다.
- 패턴의 `size_{N}_{idx}` 형식의 키값에서 마지막 "_" 앞의 문자열만 파싱하여 즉시 필터 목록에서 이를 찾도록 로직을 짰습니다.
- data.json 뿐만 아니라 유저 입력시에도 모든 배열의 길이가 같은지 검증이 필요하다고 판단하여 [검증 유틸 함수](https://github.com/Ivex0002/codyssey_E1-3/blob/a07e715e60ce6ef845b9d0c9706e0539aac3c99d/src/mac_cal/calculate/mac_calculate.py#L81) 로 mac 연산마다 검증을 사전에 실행하도록 했습니다

<details>
<summary>모드 2 유저 실행 흐름 예시</summary>

```
===Mini NPU Simulator===
모드를 선택해주세요


1. 사용자 입력
2. data.json 분석
3. 배열 평탄화 모드
4. 종료
선택: 2
#---------------------------------------
[1] 필터 로드
#---------------------------------------
✓ size_5 필터 로드 완료 (Cross, X)
✓ size_13 필터 로드 완료 (Cross, X)
✓ size_25 필터 로드 완료 (Cross, X)
#---------------------------------------
[2] 패턴 분석
#---------------------------------------

---size_5_1---
Cross 점수 : 0.9
X 점수 : 0.8999999999999999
판정: UNDECIDED | expected: x | FAIL

---size_5_2---
Cross 점수 : 8.9
X 점수 : 0.1
판정: + | expected: + | PASS

---size_13_1---
Cross 점수 : 0.3
X 점수 : 14.700000000000008
판정: x | expected: x | PASS

---size_13_2---
Cross 점수 : 7.499999999999997
X 점수 : 7.5
판정: UNDECIDED | expected: + | FAIL

---size_25_1---
Cross 점수 : 4.9
X 점수 : 4.899999999999999
판정: UNDECIDED | expected: x | FAIL

---size_25_2---
Cross 점수 : 52.9
X 점수 : 0.1
판정: + | expected: + | PASS
#---------------------------------------
[3] 성능 분석 (평균/10회)
데이터 평탄화 모드 : _2d
#---------------------------------------
크기           평균 시간(ms)       연산 횟수
----------------------------------
size_5_1         0.007          25
size_5_2         0.005          25
size_13_1        0.016         169
size_13_2        0.017         169
size_25_1        0.057         625
size_25_2        0.050         625
#---------------------------------------
[4] 결과 요약
#---------------------------------------
총 테스트: 6개
통과: 3개
실패: 3개
실패 케이스:
- size_5_1 : 동점(UNDECIDED) 처리 규칙에 따라 FAIL
- size_13_2 : 동점(UNDECIDED) 처리 규칙에 따라 FAIL
- size_25_1 : 동점(UNDECIDED) 처리 규칙에 따라 FAIL
```

- `size_5_1`, `size_13_2`, `size_25_1` 에선 두 패턴 모두 기준치 `1e-9` 미만의 오차이므로 동점 처리 규칙에 따라 **판정 불가** 결과가 됩니다
- `size_5_2`, `size_13_1`, `size_25_2` 에선 한 쪽의 결과가 기준치 이상의 오차이며, 또한 판정과 expected 값이 같으므로 **PASS** 결과가 나옵니다

</details>

<details>
<summary>`expected` 오답 패턴 스트레스 실험</summary>

- 위의 결과에서 `expected`와 판정 결과가 다른 경우가 없었으므로 임의로 데이터를 추가하여 실험해보겠습니다

```json
    "size_5_3": {
      "input": [
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [1.0, 1.0, 1.0, 1.0, 1.0],
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0]
      ],
      "expected": "x"
    },
```

- 추가한 데이터입니다. `size_5_2` 에서 `expected` 값만 반대로 바꾸어 보았습니다.

```
(중략)

---size_5_3---
Cross 점수 : 8.9
X 점수 : 0.1
판정: + | expected: x | FAIL

(중략)

#---------------------------------------
[4] 결과 요약
#---------------------------------------
총 테스트: 7개
통과: 3개
실패: 4개
실패 케이스:
- size_5_1 : 동점(UNDECIDED) 처리 규칙에 따라 FAIL
- size_5_3 : 기대 결과와 판정 결과 불일치
- size_13_2 : 동점(UNDECIDED) 처리 규칙에 따라 FAIL
- size_25_1 : 동점(UNDECIDED) 처리 규칙에 따라 FAIL
```

- 위와 같이 판정과 `expected`가 각각 +, x 로 서로 다름을 확인 할 수 있으며, `size_5_3 : 기대 결과와 판정 결과 불일치` 으로 실패 원인을 확인 할 수 있습니다

</details>

## 4. 라벨 정규화(표준화) 필수 구현

## 4-1. 라벨 정규화를 위한 PATTERN_MAP 상수
- Cross, X의 경우 패턴상에서의 expected 값과 필터의 키값들이 서로 다르기 때문에 데이터 비교를 위해 이를 일치시킬 필요가 있습니다
- 이를 구현하기 위해선 여러 방법이 있겠으나, 필요 최저한의 코드로 해당 기능을 구현하기 위해 map 상수를 작성하여 만들었습니다

```
# filter:pattern
PATTERN_MAP: dict[_FilterShape, PatternShape] = {
    "cross": "+",
    "x": "x",
}
```

- 각 항목 앞쪽의 키는 필터상의 모양을 뜻하는 키 목록들을, 이에 대응되는 값은 패턴상의 모양을 뜻하는 키 목록들을 배치했습니다.
- 이로써 아래와 같이 상수를 호출하여 비교 판정할 때 타입이 명확하게 잡힙니다

<img width="538" height="125" alt="스크린샷 2026-11-26 153205" src="https://github.com/user-attachments/assets/607de724-b4cb-412c-82ec-e53f85d80a25" />
<img width="516" height="125" alt="image" src="https://github.com/user-attachments/assets/e8d35e0c-1f79-4eac-ab91-a0fb9e4c0055" />

- `jud` 와 `pattern["expected"]` 이 같은 타입으로 잡힘을 확인 할 수 있습니다

## 4-2. data.json 파일을 기반으로 한 타입 생성
- 단순히 data.json 파일의 구조만을 보고 매번 키값을 문자열로 뽑아오면 만약에 한글자라도 오타가 날 경우 바로 실행 오류가 나거나 비교불가 판정이 됩니다
- 이를 해결하기 위해서 data.json 파일을 기반으로 collection 타입을 각각 따로 지정하여 작성했습니다. [해당 파일](../src/mac_cal/calculate/data_json_cal.py)
- 이로 인해 각각 필터와 패턴의 타입이 vscode 상에서 명확하게 잡히므로 인자를 전달할 때 아래와 같이 특정 키를 검색하기 매우 쉬워지며, 이것들의 리턴값 또한 명확하게 잡히므로 비교 연산시에 버그를 사전에 방지할수 있는 이점이 있습니다
```

# 필터

\_FilterShape: TypeAlias = Literal["cross", "x"]
\_FilterData: TypeAlias = dict[_FilterShape, PatternMatrix]

# 패턴

PatternShape: TypeAlias = Literal["x", "+"]
class \_PatternData(TypedDict):
input: PatternMatrix
expected: PatternShape

```

<img width="492" height="480" alt="스크린샷 2026-11-26 152116" src="https://github.com/user-attachments/assets/055c26e5-0901-4573-baec-615cf452d5a7" />

- `patterns` 에서 뽑아낸 값인 `pattern` 에서 타입이 `(variable) pattern: _PatternData` 으로 잡힘을 확인 할 수 있습니다

- 미션 요구지에는 Cross, X 만이 제시되어 있었으나, ux 관점에서 각각의 키값과 터미널 출력물이 일관되고 안정적인 데이터 제공을 위해 [필터 명, 패턴 명을 Enum을 활용](../src/mac_cal/handle_user_input_pattern/pattern_enum.py)하여 작성했습니다

## 5. MAC 연산
[MAC 연산 함수](../src/mac_cal/calculate/mac_calculate.py)
```

for y, row in enumerate(pattern):
for x, value in enumerate(row):
score*a += filter_a[y][x] * value
score*b += filter_b[y][x] * value
operation_count += 1

```
위와 같이 이중 for 문으로 작성하여 각각의 y, x 위치를 인덱싱하여 찾은 후 패턴의 값과 필터의 값을 곱하는 방식을 사용했습니다

## 6. 점수 비교 정책
[점수 판정 함수](../src/util/validate/validate_score.py)
- 제시된 권장 기준을 토대로 각각의 점수 차이가 1e-9 미만이면 False를 리턴합니다
- 또한 테스트 결과 클래스인 [TestLog](../src/util/testing_function/test_log.py) 를 활용하여 계산에 걸린 평균 시간도 같이 리턴해주도록 구성했습니다.

