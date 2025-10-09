from pyrogram import Client, filters, idle
from decouple import config

import logging
logging.basicConfig(level=logging.INFO)
api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE')
login = config('LOGIN')


app = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


@app.on_message(filters.private)
async def hello(client, message):
    print(message.text)
    await message.reply("Hello from Pyrogram!")


async def main():
    await app.start()
    await app.send_message("me", "Hi!")
    await idle()


app.run(main())