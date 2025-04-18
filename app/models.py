from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, DateTime
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    telegram_message_id = Column(BigInteger, nullable=False)
    chat_id = Column(BigInteger, nullable=False)
    chat_name = Column(String)
    user_id = Column(BigInteger)
    user_name = Column(String)
    text = Column(Text)
    content_type = Column(String)
    is_comment = Column(Boolean, default=False)
    original_channel_id = Column(BigInteger)
    original_post_id = Column(BigInteger)
    timestamp = Column(DateTime, default=datetime.now())
