from sqlalchemy import func
from models import Message, UserStats
from db import Session

_stats_snapshot = {}

def get_current_stats():
    return {
        user_id: stats.to_dict()
        for user_id, stats in _stats_snapshot.items()
    }

def collect_stats():
    session = Session()
    try:
        results = session.query(
            Message.user_id,
            func.count(Message.id).label("message_count"),
            func.count(func.distinct(Message.chat_id)).label("chat_count")
        ).group_by(Message.user_id).all()

        global _stats_snapshot
        _stats_snapshot = {
            user_id: UserStats(user_id, message_count, chat_count)
            for user_id, message_count, chat_count in results
        }

        print("📊 Stats collected:", get_current_stats())
        return get_current_stats()
    finally:
        session.close()
