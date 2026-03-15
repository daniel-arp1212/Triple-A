"""Market data ingestion and synchronization.

This module contains stubs for the KIS websocket and REST synchronization pipelines described in the
architecture document.

- `KISWebsocketClient`: connects to KIS WebSocket and emits decoded tick frames.
- `AccountStateSync`: polls REST endpoints to keep `W_actual` in sync.
"""

from __future__ import annotations

import json
import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, Dict, Optional

import httpx
import websockets

from triple_a.config import Settings


@dataclass
class TickData:
    """Normalized tick data payload."""

    timestamp: float
    ticker: str
    price: float
    volume: float
    bid: float
    ask: float
    extra: Dict[str, object]


class KISWebsocketClient(threading.Thread):
    """WebSocket listener that feeds decoded tick data into a queue."""

    def __init__(
        self,
        settings: Settings,
        out_queue: Deque[TickData],
        on_error: Optional[Callable[[Exception], None]] = None,
    ) -> None:
        super().__init__(daemon=True)
        self.settings = settings
        self.out_queue = out_queue
        self.on_error = on_error
        self._running = threading.Event()

    def run(self) -> None:
        self._running.set()
        while self._running.is_set():
            try:
                self._run_once()
            except Exception as exc:
                if self.on_error:
                    self.on_error(exc)
                time.sleep(1)

    def stop(self) -> None:
        self._running.clear()

    def _run_once(self) -> None:
        # TODO: implement KIS WebSocket handshake, approval key generation,
        # AES-256-CBC decryption, and tick parsing into TickData.
        raise NotImplementedError("KIS websocket client is not implemented yet.")


class AccountStateSync(threading.Thread):
    """Periodically syncs account state via REST API."""

    def __init__(
        self,
        settings: Settings,
        sync_interval_seconds: float = 60.0,
        on_state_update: Optional[Callable[[Dict[str, object]], None]] = None,
    ) -> None:
        super().__init__(daemon=True)
        self.settings = settings
        self.sync_interval_seconds = sync_interval_seconds
        self.on_state_update = on_state_update
        self._running = threading.Event()

    def run(self) -> None:
        self._running.set()
        while self._running.is_set():
            try:
                state = self._fetch_state()
                if self.on_state_update:
                    self.on_state_update(state)
            except Exception:
                pass
            time.sleep(self.sync_interval_seconds)

    def stop(self) -> None:
        self._running.clear()

    def _fetch_state(self) -> Dict[str, object]:
        # TODO: implement KIS REST API calls to fetch output1/output2.
        #       The returned dict should include:
        #         - actual_weights: Dict[str, float]
        #         - total_asset: float
        #         - cash: float
        return {}
