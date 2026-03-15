"""Orchestration layer combining data ingestion, model inference, and approval workflow."""

from __future__ import annotations

import threading
from collections import deque
from typing import Deque

from triple_a.config import Settings
from triple_a.data_fetcher import KISWebsocketClient, AccountStateSync, TickData
from triple_a.model import CatBoostInference, FeatureEngineer
from triple_a.telegram_bot import TelegramApprovalBot


class TripleAPipeline:
    """High-level pipeline coordinator."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._tick_queue: Deque[TickData] = deque(maxlen=10_000)

        self._feature_engineer = FeatureEngineer()
        self._model = CatBoostInference(settings.catboost_model_path)

        self._telegram_bot = TelegramApprovalBot(
            token=settings.telegram_bot_token,
            admin_chat_id=settings.telegram_admin_chat_id,
            ttl_seconds=settings.signal_ttl_seconds,
        )

        self._ws_client = KISWebsocketClient(
            settings=settings,
            out_queue=self._tick_queue,
            on_error=self._on_error,
        )

        self._state_sync = AccountStateSync(
            settings=settings,
            on_state_update=self._on_state_update,
        )

        self._running = threading.Event()

    def _on_error(self, exc: Exception) -> None:
        # TODO: log and surface errors to GUI.
        ...

    def _on_state_update(self, state: dict) -> None:
        # TODO: update internal weights and deviation math.
        ...

    def start(self) -> None:
        self._running.set()
        self._ws_client.start()
        self._state_sync.start()

        # TODO: start periodic inference worker in separate thread.

    def stop(self) -> None:
        self._running.clear()
        self._ws_client.stop()
        self._state_sync.stop()
