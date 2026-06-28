from sqlalchemy import Column,String,Boolean,Text , DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.databases.connection import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    username = Column(String, unique=True, nullable=False)
    
    email = Column(String, unique=True, nullable=False)
    
    password = Column(String, nullable=False)
    
    github_token = Column(String,nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
class AnalysisRun(Base):
    __tablename__ = "analysis_runs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    github_push = Column(Boolean,
    nullable=False)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    project_name = Column(String, nullable=True)
    
    language = Column(String, nullable=False)
    
    original_code = Column(Text, nullable=False)
    
    review_report = Column(Text, nullable=True)
    
    bugs_found = Column(Boolean, default=False)
    
    fixed_code = Column(Text, nullable=True)
    
    optimized_code = Column(Text, nullable=True)
    
    explanation = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    readme_content = Column(Text, nullable=True)
