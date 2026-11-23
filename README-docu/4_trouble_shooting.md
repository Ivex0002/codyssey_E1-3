## 1. 임포팅 정리 문제
[해당 커밋](https://github.com/Ivex0002/codyssey_E1-3/compare/195c1ba9798f09c42a4b676831bba96cd4527ae9...a53f0abaca1b046592cdfdff3da51379af955080)
- 조금 더 편리하게 임포팅 하는 방식이 없을까 고민하던 중, `__init__.py` 파일의 사용법을 알게 되었습니다
- 해당 폴더의 하위 파일들을 일목 요연하게 정리하여 export 해주는 것이었죠
- 그래서 [util/__init__.py](../src/util/__init__.py) 과 같이 유틸 함수들을 묶어 한 문서에 정리해두었습니다.
- 그러나 `src\util` 내부의 하위 파일에서는 `from util import choice, validate_pattern` 와 같은 재귀 호출이 불가능하고, 데이터 클래스 등 외부 참조가 필요할때(src/data_class/simple_pattern.py) 서로가 서로를 참조하는 순환 참조가 불가능하기 때문에 사용법에 주의가 필요했습니다.

- 이런 참조 형식 문제는 본래 vscode 와 같은 에디터가 사전에 잡아줘야만 하는 컴파일 오류입니다.
- type script 에서는 이런 임포팅 오류를 즉시 잡아주기 때문에 생긴 해프닝이었습니다.
- 이에 대한 문제를 해결하기 위해 오류가 발생한 지점을 모두 찾아 아래와 같이 절대 경로로 변경했습니다.
```
- from util import pattern_generator, validate_pattern

+ from util.pattern.pattern_generator import pattern_generator
+ from util.validate.validate_pattern import validate_pattern
```
