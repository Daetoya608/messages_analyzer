from pyrogram import idle
from pyrogram.handlers import MessageHandler

from app.core.db.connection.session import init_models
from app.domains import *
from app.domains.telegram.handlers import handle_text_messages
from app.domains.telegram.utils import user_bot


async def main():
    await init_models()
    my_handler = MessageHandler(handle_text_messages)
    user_bot.add_handler(my_handler)
    await user_bot.start()
    await idle()


if __name__ == "__main__":
    user_bot.run(main())
