import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    token = Column(String(200), unique=True)
    daily_quota = Column(Integer, default=3)
    last_use_date = Column(DateTime, default=None)
    is_visitor = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class HistoryRecord(Base):
    __tablename__ = "history_records"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(100), unique=True, index=True)
    user_token = Column(String(200), index=True)
    text_preview = Column(String(200), default="")
    report_preview = Column(String(500), default="")
    report_content = Column(Text, default="")
    clean_text = Column(Text, default="")
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
