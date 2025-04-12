from sqlalchemy import func
from models import Message
from db import Session

def collect_stats():
    session = Session()
    try:
        results = session.query(
            Message.user_id,
            func.count(Message.id).label("message_count"),
            func.count(func.distinct(Message.chat_id)).label("chat_count")
        ).group_by(Message.user_id).all()

        stats = {
            user_id: {"message_count": message_count, "chat_count": chat_count} #todo maybe model for this
            for user_id, message_count, chat_count in results
        }

        print("📊 Stats collected:", stats) #todo if many ids remove print, its just for test
        return stats
    finally:
        session.close()
