# Triple A (Active Asset Allocation)

**Triple A** is a real-time quantitative asset allocation and automated trading framework.

This project implements a **Human-in-the-Loop** (HITL) trading pipeline that:

- Collects high-frequency tick data from Korea Investment & Securities (KIS) via WebSocket.
- Uses **CatBoost** for real-time portfolio target allocation estimation.
- Enforces a **5% deviation trigger** between actual and target weights.
- Sends approval requests via **Telegram Bot** before executing trades.
- Uses **PySide6** for a live GUI dashboard.

## Architecture Overview

Key components:

- **Data Fetcher**: WebSocket client to receive KIS tick data (encrypted with AES-256-CBC).
- **State Synchronizer**: Periodic REST polling of account balances to compute `W_actual`.
- **Inference Engine**: Real-time feature engineering + CatBoost model inference for `W_target`.
- **Deviation Detector**: 5% deviation logic + cooldown + debounce.
- **Telegram Approval**: Sends inline keyboard approval requests and handles callbacks.
- **GUI**: PySide6-based dashboard (thread-safe communication via Signals/Slots).

## Getting Started

1. Create virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -e .
```

2. Copy `example.env` to `.env` and fill in your keys.

3. Run:

```powershell
python -m triple_a.main
```
