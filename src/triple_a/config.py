"""Configuration utilities."""

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    kis_app_key: str
    kis_secret_key: str
    kis_account_id: str
    telegram_bot_token: str
    telegram_admin_chat_id: str
    catboost_model_path: Path
    deviation_threshold: float
    signal_ttl_seconds: int


def load_settings(env_path: Path | None = None) -> Settings:
    if env_path is None:
        env_path = Path(".env")

    load_dotenv(dotenv_path=env_path)

    return Settings(
        kis_app_key=__import__("os").getenv("KIS_APP_KEY", ""),
        kis_secret_key=__import__("os").getenv("KIS_SECRET_KEY", ""),
        kis_account_id=__import__("os").getenv("KIS_ACCOUNT_ID", ""),
        telegram_bot_token=__import__("os").getenv("TELEGRAM_BOT_TOKEN", ""),
        telegram_admin_chat_id=__import__("os").getenv("TELEGRAM_ADMIN_CHAT_ID", ""),
        catboost_model_path=Path(__import__("os").getenv("CATBOOST_MODEL_PATH", "./models/catboost.cbm")),
        deviation_threshold=float(__import__("os").getenv("DEVIATION_THRESHOLD", "0.05")),
        signal_ttl_seconds=int(__import__("os").getenv("SIGNAL_TTL_SECONDS", "600")),
    )
