"""
處理「單一玩家的暫存進度」；結構與 UserManager 類似。
"""

from typing import Dict, Any
import storage


class StateManager:
    def __init__(self) -> None:
        self._states: Dict[str, Dict[str, Any]] = storage.load_json(storage.STATE_FILE)

    def get(self, username: str) -> Dict[str, Any] | None:
        return self._states.get(username)

    def save(self, username: str, state: Dict[str, Any]) -> None:
        self._states[username] = state
        self._flush()

    def clear(self, username: str) -> None:
        if username in self._states:
            del self._states[username]
            self._flush()

    # -------- internal --------
    def _flush(self) -> None:
        storage.save_json(storage.STATE_FILE, self._states)
