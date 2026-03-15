"""Telegram Bot integration for HITL approval workflow."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, ContextTypes, MessageHandler, filters


@dataclass
class ApprovalContext:
    """Stores an approval request context for later callback handling.""" 

    created_at: datetime
    payload: Dict[str, Any]


class TelegramApprovalBot:
    """A simple approval workflow via Telegram inline keyboard."""

    def __init__(self, token: str, admin_chat_id: str, ttl_seconds: int = 600) -> None:
        self._token = token
        self._admin_chat_id = admin_chat_id
        self._ttl_seconds = ttl_seconds
        self._context_store: Dict[str, ApprovalContext] = {}

        self._app = Application.builder().token(self._token).build()
        self._app.add_handler(CallbackQueryHandler(self._on_callback, pattern=r"^approve:|^reject:"))

    async def start(self) -> None:
        await self._app.initialize()
        await self._app.start()
        await self._app.updater.start_polling()

    async def stop(self) -> None:
        await self._app.updater.stop()
        await self._app.stop()
        await self._app.shutdown()

    async def send_approval_request(self, payload_id: str, payload: Dict[str, Any], message: str) -> None:
        self._context_store[payload_id] = ApprovalContext(created_at=datetime.utcnow(), payload=payload)
        keyboard = [[InlineKeyboardButton("Approve", callback_data=f"approve:{payload_id}"),
                     InlineKeyboardButton("Reject", callback_data=f"reject:{payload_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self._app.bot.send_message(chat_id=self._admin_chat_id, text=message, reply_markup=reply_markup)

    async def _on_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if query is None:
            return
        await query.answer()

        payload_id = query.data.split(":", 1)[1]
        ctx = self._context_store.get(payload_id)
        if ctx is None:
            await query.edit_message_text("[Expired] This signal is no longer available.")
            return

        if datetime.utcnow() - ctx.created_at > timedelta(seconds=self._ttl_seconds):
            await query.edit_message_text("[Expired] This signal has timed out.")
            self._context_store.pop(payload_id, None)
            return

        if query.data.startswith("approve:"):
            await query.edit_message_text("✅ Approved. Executing trade...")
            # TODO: notify trade executor
        else:
            await query.edit_message_text("❌ Rejected. No action taken.")

        self._context_store.pop(payload_id, None)
