import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from mac_cal.mac_cal import MacCal

if __name__ == "__main__":
    mac_cal = MacCal()
    mac_cal.run()
# todo
# 1. 사용자 입력 패턴/필터 입력 받을때 사이즈 먼저 1회 입력 > 매 패턴 필터마다 커스텀 입력 여부 받기
# 3x3 강제 하는게 문제
# v

# 2. 행렬 길이 불일치시 사용자 입력 다시 받기
# v

# 3. 필터 키 정규화 하라는데 필수적인가? 정규화 말고 타입 Literal 로 따지는게 편하지 않나
# src/mac_cal/calculate/data_json_cal.py > 'is_pass = jud.lower() == pattern["expected"].lower()'
# 부족한 점
# filter 키(예:'Cross'/'X') 정규화 함수 또는 분리된 normalize_label 부재
# 보완
# 라벨 매칭 규칙을 별도 함수로 정리해 일관성 검증을 추가하세요
# >>> 맵 만들어서 각각의 키 비교
# v

# 3-1. 라벨 정규화 함수를 분리 하라는데, 타입 Literal 이 이 역할 대신 가능함
# >>> 리드미 문서에 따로 기입하기
# >>> Literal 과 맵 상수를 작성하여 해결함
# v

# 4. 결과 리포트 리드미 문서에 원인 분석 첨부
# >>> 각각의 실패, 성공 원인 및 오답 데이터 예시 첨부
# v

# 5. 테스팅 함수 범위 지정을 하나의 계산 함수에만 따로 지정한 이유 리드미에 첨부
# v

# 6. MAC 점수 해석(점수↑ → 유사도↑)의 근거를 README에 한두 문장으로 기술
# v

# 6-1. src/mac_cal/calculate/mac_calculate.py > 'operation_count += 1'
# README에 패턴 크기 N 대비 연산량이 N^2임을 수식으로 명확히 서술
# v

# 6-2. src/util/print/print_result.py > 'cant_cal_result_msg = " (판정 불가)"'
# mode1 vs mode2의 동점 처리 차이를 README에 비교 표로 정리
# v

# 7. 새 라벨 확장 절차를 단계별 체크리스트로 README에 추가
# v

# 8. 대형 입력(N=1000) 관련 예상 문제와 우선 적용 최적화(예: flatten/메모리 뷰 등)를 README에 기술
# v

# 9. src/mac_cal/calculate/mac_calculate.py > 'case "_1d":'
# CPU와 NPU 병목(직렬 vs 병렬)에 대한 분석/설명이 없음
# CPU 대 NPU 병목과 병렬화 이점을 간단히 정리해 README에 추가하세요
# v
