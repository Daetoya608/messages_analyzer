from decouple import config
from pyrogram import Client

api_id = config("API_ID")
api_hash = config("API_HASH")
phone = config("PHONE")
login = config("LOGIN")


user_bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)
