import datetime
import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from database import Base

class ConsultationSession(Base):
    __tablename__ = "consultation_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    industry = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    company_size = Column(String, nullable=True)
    status = Column(String, default="discovering")  # discovering, analyzing, completed
    current_step = Column(Integer, default=0)
    messages = Column(Text, default="[]")  # Serialized JSON list of messages
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class BusinessAnalysis(Base):
    __tablename__ = "business_analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("consultation_sessions.id"), nullable=True)
    industry = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    company_size = Column(String, nullable=True)
    
    # Large structured components stored as serialized JSON strings
    business_summary = Column(Text, nullable=False)
    pain_point_analysis = Column(Text, nullable=False)
    automation_readiness = Column(Text, nullable=False)
    recommendations = Column(Text, nullable=False)
    tech_stack = Column(Text, nullable=False)
    roi_prediction = Column(Text, nullable=False)
    roadmap_plan = Column(Text, nullable=False)
    workflow_diagram = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
