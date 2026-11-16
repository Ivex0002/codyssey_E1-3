# testing_function
# 하나의 함수를 지연실행으로 변환
from .testing_function.testable import testable

# 하나의 함수를 다회 테스트
# 다중 spec 운용 -> testing_function
# 빠른 테스트 -> quick_test
from .testing_function.testing_function import testing_function, quick_test

# 인자를 묶어주는 클래스
from .testing_function.test_spec import TestSpec
