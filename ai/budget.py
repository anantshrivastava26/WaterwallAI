"""AI budgeting (section 11). Gates LLM calls under a daily token budget."""
from __future__ import annotations

from datetime import date
from threading import Lock

from backend.app.config import settings


class TokenBudget:
    def __init__(self, daily_limit: int) -> None:
        self.daily_limit = daily_limit
        self._lock = Lock()
        self._day: date = date.today()
        self._used = 0

    def _roll_if_new_day(self) -> None:
        today = date.today()
        if today != self._day:
            self._day = today
            self._used = 0

    def can_spend(self, estimate: int) -> bool:
        with self._lock:
            self._roll_if_new_day()
            return self._used + estimate <= self.daily_limit

    def spend(self, tokens: int) -> None:
        with self._lock:
            self._roll_if_new_day()
            self._used += tokens

    @property
    def remaining(self) -> int:
        with self._lock:
            self._roll_if_new_day()
            return max(0, self.daily_limit - self._used)


budget = TokenBudget(settings.daily_llm_token_budget)
