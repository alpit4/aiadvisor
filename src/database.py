"""
Database models and initialization
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from .config import settings

# Database setup
engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Request status constants
REQUEST_STATUS_PENDING = "PENDING"
REQUEST_STATUS_RESOLVED = "RESOLVED"
REQUEST_STATUS_UNRESOLVED = "UNRESOLVED"


class HelpRequest(Base):
    """Help request model"""
    __tablename__ = "help_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_phone = Column(String, nullable=False)
    customer_name = Column(String, nullable=True)
    question = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    status = Column(String(20), default="PENDING")
    supervisor_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    timeout_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<HelpRequest(id={self.id}, status={self.status}, question='{self.question[:50]}...')>"


class KnowledgeEntry(Base):
    """Knowledge base entry model"""
    __tablename__ = "knowledge_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    source_request_id = Column(Integer, nullable=True)  # Links to HelpRequest
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<KnowledgeEntry(id={self.id}, question='{self.question[:50]}...')>"


async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """Get database session context manager"""
    return SessionLocal()
