# 대형입력 대응 전략

[연산 로직 파일](../src/mac_cal/calculate/mac_calculate.py)

- 해당 파일에 기입된 `_flatten_matrices` 를 활용하여 1차원 배열로 전환 및 저장

```
def _flatten_matrices(pattern_data: PatternInputData) -> _FlatPatternData:
    flat_patterns: _FlatPatternData = {}
    for name, matrix in pattern_data.items():
        result: _FlatData = []
        for row in matrix:
            result.extend(row)
        flat_patterns[name] = result
    return flat_patterns
```
