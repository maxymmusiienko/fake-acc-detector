from sqlalchemy import func
from models import Message
from db import Session
from logger import get_logger
from dtos import UserStatsBrief, MessageDTO, UserStatsDetailed

logger = get_logger(__name__)
_stats_snapshot = {}

def get_current_stats():
    return {
        user_id: stats.to_dict()
        for user_id, stats in _stats_snapshot.items()
    }

def collect_stats():
    session = Session()
    try:
        # Get message count and distinct chat count per user
        count_results = session.query(
            Message.user_id,
            func.count(Message.id).label("message_count"),
            func.count(func.distinct(Message.chat_id)).label("chat_count"),
        ).group_by(Message.user_id).all()

        # Get all (user_id, chat_name) pairs
        chats_results = session.query(
            Message.user_id,
            Message.chat_name,
        ).distinct().all()

        # Group chat names per user
        chat_names_by_user = {}
        for user_id, chat_name in chats_results:
            chat_names_by_user.setdefault(user_id, set()).add(chat_name)

        # Compose stats
        global _stats_snapshot
        _stats_snapshot = {
            user_id: UserStatsBrief(
                user_id, message_count, chat_count, sorted(chat_names_by_user.get(user_id, []))
            )
            for user_id, message_count, chat_count in count_results
        }

        logger.info(f"📊 Stats collected: for {len(_stats_snapshot)} users")

        return get_current_stats()
    finally:
        session.close()

def get_stats_by_id(user_id: int):
    session = Session()
    try:
        msg_count = session.query(Message).filter_by(user_id=user_id).count()
        chats = session.query(Message.chat_name).filter_by(user_id=user_id).distinct()
        chat_names = sorted({row[0] for row in chats})

        messages = (
            session.query(Message)
            .filter_by(user_id=user_id)
            .order_by(Message.timestamp.desc())
            .limit(20)
            .all()
        )

        message_dtos = [
            MessageDTO(m.text, m.timestamp, m.chat_name)
            for m in messages
        ]

        stats = UserStatsDetailed(
            user_id=user_id,
            message_count=msg_count,
            chat_count=len(chat_names),
            chat_names=chat_names,
            messages=message_dtos,
        )

        return stats.to_dict()
    finally:
        session.close()
