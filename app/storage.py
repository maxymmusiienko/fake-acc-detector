from models import Message
from db import Session
from datetime import datetime
from pytz import timezone
from logger import get_logger

logger = get_logger(__name__)
message_buffer = []
FLUSH_SIZE = 5 #todo just test

def queue_message(data: dict):
    message = Message(
        telegram_message_id=data["telegram_message_id"],
        chat_id=data["chat_id"],
        chat_name=data["chat_name"],
        user_id=data["user_id"],
        user_name=data["user_name"],
        text=data["text"],
        content_type=data["content_type"],
        is_comment=data["is_comment"],
        original_channel_id=data.get("original_channel_id"),
        original_post_id=data.get("original_post_id"),
        timestamp = datetime.now(timezone("Europe/Kiev")) #todo mb take date from message
    )
    message_buffer.append(message)

    if len(message_buffer) >= FLUSH_SIZE:
        flush_messages()

def flush_messages():
    if not message_buffer:
        return
    session = Session()
    session.bulk_save_objects(message_buffer)
    session.commit()
    logger.info(f"✅ Flushed {len(message_buffer)} messages to DB")
    message_buffer.clear()
