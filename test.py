import os
from telegram.client import Telegram, AuthorizationState

tg = Telegram(
    api_id=int(os.environ["TG_API_ID"]),
    api_hash=os.environ["TG_API_HASH"],
    phone=os.environ["TG_PHONE"],
    database_encryption_key=os.environ["TG_DB_KEY"],
)

state = tg.login(blocking=False)

if state == AuthorizationState.WAIT_CODE:
    code = input("Waiting for code: ")
    tg.send_code(code)
    state = tg.login(blocking=False)

if state == AuthorizationState.WAIT_PASSWORD:
    password = os.environ["TG_PASSWORD"]
    tg.send_password(password)
    state = tg.login(blocking=False)

def new_message_handler(update):
    if update.get("@type") != "updateNewMessage":
        return

    message = update["message"]
    chat_id = message["chat_id"]
    sender_id = message["sender_id"]

    # Extract message content
    content = message.get("content", {})
    print("Content type:", content.get("@type"))
    text = ""

    content_type = content.get("@type")
    if content_type == "messageText":
        text = content["text"]["text"]
    elif content_type.startswith("message") and "caption" in content:
        # Media message with caption
        text = content["caption"].get("text", "")

    # Get chat title
    chat_result = tg.get_chat(chat_id)
    chat_result.wait()
    chat = chat_result.update
    chat_title = chat.get("title", "Private Chat")

    # Get sender user info
    user_display = "Unknown"
    if sender_id["@type"] == "messageSenderUser":
        user_id = sender_id["user_id"]
        user_result = tg.get_user(user_id)
        user_result.wait()
        user = user_result.update

        first = user.get("first_name", "")
        last = user.get("last_name", "")
        username = user.get("username", "")
        if first or last:
            user_display = f"{first} {last}".strip()
        elif username:
            user_display = f"@{username}"

    print(f"[{chat_title}] {user_display}: {text}")

tg.add_message_handler(new_message_handler)
tg.idle()
