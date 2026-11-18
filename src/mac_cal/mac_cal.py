from util import choice, TestLog
from data_class.simple_pattern import SimplePattern
import json
from .handle_user_input_pattern.custom_input import custom_input
from .handle_user_input_pattern.simple_input import simple_input

path = {
    "data_json_path": r"data/data.json",
    "test_logs_path": r"test_logs/test_logs.json",
}


class MacCal:
    def __init__(self):
        self.test_logs: list[TestLog] = []
        self.data_json: dict | None = None
        # 유저 입력 패턴이 장기저장 필요한가?
        self.patterns: list[SimplePattern]

        self.load()

    def load(self):
        self.data_json = self.load_path(path["data_json_path"])
        self.test_logs = self.load_path(path["test_logs_path"]) or []

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
        menu = ["3x3", "패턴 생성기(보너스)"]
        chosen_menu = menu[choice(menu) - 1]

        user_input = custom_input() if chosen_menu == 1 else simple_input()
        # todo filter, pattern 연산

    def run(self):
        menu = ["사용자 입력", "data.json 분석", "종료"]
        try:
            while True:
                print("===Mini NPU Simulator===")
                print("모드를 선택해주세요")

                user_input = choice(menu)

                match user_input:
                    case 1:
                        # todo : size, shape 입력받기
                        # size, shape 에 따른 필터/패턴 생성 로직
                        self.input_pattern()
                        return
                    case 2:
                        # 불러온 data.json 분석
                        # 단순 dict 타입이기 때문에 직접 다 까봐야 함
                        return
                    case 3:
                        self.exit()
                        break

        except (KeyboardInterrupt, EOFError):
            self.exit()
