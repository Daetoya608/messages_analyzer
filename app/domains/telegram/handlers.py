from pyrogram import filters, Client
from pyrogram.types import Message
from app.domains.telegram.utils import user_bot

@user_bot.on_message(filters.text)
async def hello(client: Client, message: Message):
    pass
