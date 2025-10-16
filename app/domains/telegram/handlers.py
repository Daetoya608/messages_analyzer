from pyrogram import Client
from pyrogram.types import Message as TgMessage

from app.core.db.connection import get_session
from app.domains.telegram.service import get_telegram_service


async def handle_text_messages(client: Client, message: TgMessage):
    print(message.text)
    async for session in get_session():
        telegram_service = get_telegram_service(session)
        await telegram_service.process_new_message(message)
