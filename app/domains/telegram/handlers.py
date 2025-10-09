from pyrogram import filters, Client
from pyrogram.types import Message
from app.domains.telegram.utils import user_bot
from app.domains.telegram.service import TelegramService, get_telegram_service

@user_bot.on_message(filters.text)
async def handle_text_messages(client: Client, message: Message):
    print(message.text)
    telegram_service = await get_telegram_service()
    await telegram_service.process_new_message(message)
