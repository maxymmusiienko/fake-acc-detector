from parser import extract_message_data
from storage import queue_message
from logger import get_logger

def make_handler(tg):
    def new_message_handler(update):
        logger = get_logger(__name__)
        if update.get("@type") != "updateNewMessage":
            return
        try:
            data = extract_message_data(tg, update)
            if data["text"].strip():
                queue_message(data)
                logger.debug(f"queued message: {data['text']}")
            else:
                logger.debug(f"skipping empty message from {data['sender_id']}")
        except Exception as e:
            logger.error("❌ Error processing message:", e)
    return new_message_handler
