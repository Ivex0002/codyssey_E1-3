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
# 1. 로직들 atoz 테스트 돌려보기
# 2. 장기저장 필요한지 -> SimplePattern 기반?
