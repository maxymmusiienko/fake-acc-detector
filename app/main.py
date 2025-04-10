import os
from telegram.client import Telegram, AuthorizationState
from handler import make_handler
from models import Base
from db import engine

# Create tables if needed
Base.metadata.create_all(engine)

# Telegram init
tg = Telegram(
    api_id=int(os.environ["TG_API_ID"]),
    api_hash=os.environ["TG_API_HASH"],
    phone=os.environ["TG_PHONE"],
    database_encryption_key=os.environ["TG_DB_KEY"],
)

state = tg.login(blocking=False)

if state == AuthorizationState.WAIT_CODE:
    code = input("Enter code: ")
    tg.send_code(code)
    state = tg.login(blocking=False)

if state == AuthorizationState.WAIT_PASSWORD:
    tg.send_password(os.environ["TG_PASSWORD"])
    state = tg.login(blocking=False)

tg.add_message_handler(make_handler(tg))
tg.idle()

#todo add loging
#todo deal with chat name  and username
#todo think about DTO
