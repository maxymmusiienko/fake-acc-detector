from parser import extract_message_data
from storage import queue_message

def make_handler(tg):
    def new_message_handler(update):
        if update.get("@type") != "updateNewMessage":
            return
        try:
            data = extract_message_data(tg, update)
            queue_message(data)
        except Exception as e:
            print("❌ Error processing message:", e)
    return new_message_handler
