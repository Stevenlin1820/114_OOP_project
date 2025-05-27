"""
封裝與「使用者帳號 / 分數」相關的邏輯。
"""

from typing import Dict, List, Tuple
import storage


class UserManager:
    def __init__(self) -> None:
        self._users: Dict[str, Dict[str, int | str]] = storage.load_json(storage.USERS_FILE)

    # --------  CRUD  --------
    def authenticate(self, username: str, password: str) -> bool:
        return username in self._users and self._users[username]["password"] == password

    def register(self, username: str, password: str) -> bool:
        if username in self._users:
            return False
        self._users[username] = {"password": password, "score": 0}
        self._flush()
        return True

    def update_score(self, username: str, score: int) -> None:
        if username in self._users and score > self._users[username]["score"]:
            self._users[username]["score"] = score
            self._flush()

    def top_scores(self, n: int = 5) -> List[Tuple[str, Dict[str, int | str]]]:
        return sorted(
            self._users.items(), key=lambda kv: kv[1]["score"], reverse=True
        )[:n]

    # --------  internal  --------
    def _flush(self) -> None:
        storage.save_json(storage.USERS_FILE, self._users)

    # 給外部讀取 (唯讀)
    @property
    def data(self) -> Dict[str, Dict[str, int | str]]:
        return self._users
