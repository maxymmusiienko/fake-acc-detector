class MessageDTO:
    def __init__(self, text, date, chat_name):
        self.text = text
        self.date = date.isoformat()
        self.chat_name = chat_name

    def to_dict(self):
        return {
            "text": self.text,
            "date": self.date,
            "chat_name": self.chat_name,
        }


class UserStatsBrief:
    def __init__(self, user_id, message_count, chat_count, chat_names):
        self.user_id = user_id
        self.message_count = message_count
        self.chat_count = chat_count
        self.chat_names = chat_names

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "message_count": self.message_count,
            "chat_count": self.chat_count,
            "chat_names": self.chat_names,
        }


class UserStatsDetailed(UserStatsBrief):
    def __init__(self, user_id, message_count, chat_count, chat_names, messages):
        super().__init__(user_id, message_count, chat_count, chat_names)
        self.messages = messages

    def to_dict(self):
        data = super().to_dict()
        data["recent_messages"] = [m.to_dict() for m in self.messages]
        return data
