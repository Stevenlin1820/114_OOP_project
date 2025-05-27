"""
統一管理路徑與 JSON 讀寫工具。
"""

import json
import os
from typing import Any, Dict

# 專案根目錄 (即本檔案所在處)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR                      # 全部資料檔就放這裡

USERS_FILE = os.path.join(DATA_DIR, "math_game_users.json")
STATE_FILE = os.path.join(DATA_DIR, "math_game_state.json")


def load_json(path: str) -> Dict[str, Any]:
    """安全地載入 JSON；失敗就回傳空 dict。"""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_json(path: str, data: Dict[str, Any]) -> None:
    """把 dict 寫回磁碟 (UTF-8 & pretty print)。"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
