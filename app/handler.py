from parser import extract_message_data
from storage import queue_message
from logger import get_logger

def validate_message(data):
    if data.get("user_id") is None:
        return False, "missing sender_id"
    if not isinstance(data.get("text"), str):
        return False, "text is not a string"
    if not data["text"].strip():
        return False, "text is empty"
    return True, ""

def make_handler(tg):
    logger = get_logger(__name__)

    def new_message_handler(update):
        if update.get("@type") != "updateNewMessage":
            return
        try:
            data = extract_message_data(tg, update)
            is_valid, reason = validate_message(data)
            if is_valid:
                queue_message(data)
                logger.info(f"queued message: {data['text']}")
            else:
                logger.info(f"skipping message: {reason}. Data: {data}")
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
    return new_message_handler
