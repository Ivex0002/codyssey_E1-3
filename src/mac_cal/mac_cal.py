from util import (
    choice,
    TestLog,
    print_pattern,
    quick_test,
    print_result,
)
import json
from .calculate.mac_calculate import mac_calculate, CalMod
from .calculate.data_json_cal import data_json_cal
from handle_user_input_pattern.handle_user_input_pattern import user_inpt_pattern

path = {
    "data_json_path": r"data/data.json",
    "test_logs_path": r"test_logs/test_logs.json",
}


class MacCal:
    def __init__(self):
        self.test_logs: list[TestLog] = []
        self.data_json: dict | None = None
        # 유저 입력 패턴이 장기저장 필요한가?
        # self.patterns: list[SimplePattern]
        self.what_d: CalMod = "_2d"

        self.load()

    def load(self):
        self.data_json = self.load_path(path["data_json_path"])
        # 테스트 로그 장기저장(미정)
        # self.test_logs = self.load_path(path["test_logs_path"]) or []

    def load_path(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("⚠️ 데이터 파일이 손상되었습니다.")
            print(f"파일 경로 : {path}")

    def save_test_log(self, log: TestLog):
        if log:
            self.test_logs.append(log)
        with open(path["test_logs_path"], "w", encoding="utf-8") as f:
            json.dump(
                [log.to_dict() for log in self.test_logs],
                f,
                ensure_ascii=False,
                indent=4,
            )

    def exit(self):
        print("프로그램을 종료합니다.")

    def input_pattern(self):
        # menu = ["3x3", "패턴 생성기(보너스)"]
        # chosen_menu = menu[choice(menu) - 1]

        # # print("debug:" + chosen_menu)

        # user_input = custom_input() if chosen_menu == menu[0] else simple_input()
        user_input = user_inpt_pattern()

        for key, val in user_input.items():
            print_pattern(key, val)
        print("입력된 값은 위와 같습니다\nMAC 연산을 실행합니다")

        cal_result = mac_calculate(
            user_input["filter_a"],
            user_input["filter_b"],
            user_input["pattern"],
            self.what_d,
        )

        try:
            # 1회 실행 결과를 저장
            score_a, score_b, _count = cal_result()
            # 10회 연산 평균을 로그로 저장
            # 기능 요구사항에는 없었으나, 테스트 1회의 연산 시간 및 전체 테스트 연산 시간 따로 추적 가능
            result_log = quick_test(cal_result, test_count=10)

            print_result(score_a, score_b, result_log)

        # 잘못된 인풋이 들어올 때 e) 세 배열의 크기가 다른 등의 경우
        except ValueError as e:
            print(f"MAC 연산 오류: {e}")

    def handle_data_json(self):
        data_json_cal(self.data_json, self.what_d)
        return

    def set_flatten_mod(self):
        print(f"현재 데이터 평탄화 모드는 {self.what_d} 입니다\n 모드를 선택해주세요")
        menu: list[CalMod] = ["_1d", "_2d"]
        user_input = choice(menu)
        self.what_d = menu[user_input - 1]
        print(f"데이터 파싱 구조가 변경 되었습니다 : {self.what_d}\n")

    def run(self):
        menu = ["사용자 입력", "data.json 분석", "배열 평탄화 모드", "종료"]
        try:
            while True:
                print("===Mini NPU Simulator===")
                print("모드를 선택해주세요")

                user_input = choice(menu)

                match user_input:
                    case 1:
                        self.input_pattern()
                        continue
                    case 2:
                        # 불러온 data.json 분석
                        # 단순 dict 타입이기 때문에 직접 다 까봐야 함
                        self.handle_data_json()
                        continue
                    case 3:
                        self.set_flatten_mod()
                        continue
                    case 4:
                        self.exit()
                        break

        except (KeyboardInterrupt, EOFError):
            self.exit()
