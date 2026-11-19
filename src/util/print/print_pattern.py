from src.data_class.type import PatternMatrix


def print_pattern(name: str, pattern: PatternMatrix):
    """패턴 1개의 이름, 실제 값들을 터미널에 출력해주는 함수"""
    print(f"==={name}===")
    for row in pattern:
        print(" ".join(map(str, row)))
    return
