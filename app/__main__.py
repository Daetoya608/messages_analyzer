# from app.domains.telegram.utils import user_bot
from pyrogram import Client, idle
from decouple import config
import logging


logging.basicConfig(level=logging.INFO)
api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE')
login = config('LOGIN')


from pyrogram import filters, Client
from pyrogram.types import Message as TgMessage
from app.domains import *
from app.domains.telegram.service import get_telegram_service
from app.core.db.connection.session import init_models

user_bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


@user_bot.on_message()
async def handle_text_messages(client: Client, message: TgMessage):
    print(message.text)
    telegram_service = await get_telegram_service()
    await telegram_service.process_new_message(message)



# async def main():
#     async with user_bot:
#         print("Бот запущен!")
#         await idle()  # удерживает клиента активным, пока не остановишь

async def main():
    await init_models()
    await user_bot.start()
    await idle()


if __name__ == "__main__":
    user_bot.run(main())
