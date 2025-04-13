def get_chat_name(tg, chat_id):
    try:
        chat_result = tg.get_chat(chat_id)
        chat_result.wait()
        chat = chat_result.update
        return chat.get("title", "Private Chat") or chat.get("username") or f"Chat {chat_id}"
    except Exception as e:
        print(f"⚠️ Failed to get chat name for {chat_id}: {e}")
        return f"Chat {chat_id}"

def get_user_name(tg, user_id):
    try:
        user_result = tg.get_user(user_id)
        user_result.wait()
        user = user_result.update
        first = user.get("first_name", "")
        last = user.get("last_name", "")
        username = user.get("username", "")
        if username:
            return username
        return f"{first} {last}".strip() or f"User {user_id}"
    except Exception as e:
        print(f"⚠️ Failed to get user name for {user_id}: {e}")
        return f"User {user_id}"

def extract_message_data(tg, update):
    message = update["message"]
    sender_id = message["sender_id"]
    content = message.get("content", {})
    reply_to = message.get("reply_to", {})

    text = ""
    content_type = content.get("@type", "")
    if content_type == "messageText":
        text = content["text"]["text"]
    elif "caption" in content:
        text = content["caption"].get("text", "")

    is_comment = (
            reply_to.get("@type") == "messageReplyToMessage"
            and reply_to.get("chat_id") != message["chat_id"]
    )

    chat_id = message["chat_id"]
    user_id = sender_id.get("user_id")

    chat_name = get_chat_name(tg, chat_id)
    user_name = get_user_name(tg, user_id)

    return {
        "telegram_message_id": message["id"],
        "chat_id": chat_id,
        "chat_name": chat_name,
        "user_id": user_id,
        "user_name": user_name,
        "text": text,
        "content_type": content_type,
        "is_comment": is_comment,
        "original_channel_id": reply_to.get("chat_id"),
        "original_post_id": reply_to.get("message_id"),
    }
