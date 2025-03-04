from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from database import Base



class IWill(Base):
    __tablename__ = "i_wills"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    date = Column(Date, nullable=False)  # Day-based task
    time = Column(Time, nullable=True)   # Optional time
    notification_time = Column(DateTime, nullable=True)  # Optional notification
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    event_link = Column(String, nullable=True)



from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class WorkSession(Base):
    __tablename__ = "work_sessions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration_hours = Column(Float, nullable=True)  # Automatically calculated
    method = Column(String, nullable=False)  # "manual" or "timer"

    project = relationship("Project", back_populates="work_sessions")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, default=datetime.utcnow)
    end_date = Column(Date, nullable=True)
    total_hours = Column(Float, default=0.0)  # Total time spent on the project
    completion_percent = Column(Float, default=0.0)  
    tasks = relationship("Task", back_populates="project", cascade="all, delete")
    work_sessions = relationship("WorkSession", back_populates="project", cascade="all, delete")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="Pending")  # Options: Pending, In Progress, Completed
    due_date = Column(Date, nullable=True)

    # Relationship with Project
    project = relationship("Project", back_populates="tasks")
    event_link = Column(String, nullable=True)

