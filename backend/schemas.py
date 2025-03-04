from pydantic import BaseModel
from typing import Optional
from datetime import date as dt_date, datetime, time as dt_time
from pydantic import BaseModel, PastDate, PastDatetime, FutureDate, FutureDatetime
from typing import List



class IWillBase(BaseModel):
    action: str
    date: dt_date
    time: Optional[dt_time] = None
    notification_time: Optional[datetime] = None
    event_link: Optional[str] = None

class IWillCreate(IWillBase):
    pass

class IWillUpdate(BaseModel):
    action: Optional[str] = None
    date: Optional[dt_date] = None
    time: Optional[dt_time] = None
    notification_time: Optional[datetime] = None
    completed: Optional[bool] = None

class IWill(IWillBase):
    id: int
    created_at: datetime
    completed: bool

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Pending"
    due_date: Optional[dt_date] = None
    event_link: Optional[str] = None


class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[dt_date] = None
    end_date: Optional[dt_date] = None
    
    completion_percent: Optional[float] = 0.0

class ProjectCreate(ProjectBase):
    pass



class WorkSessionBase(BaseModel):
    project_id: int

class WorkSessionStart(WorkSessionBase):
    """Used to start a timer"""
    pass

class WorkSessionStop(BaseModel):
    """Used to stop a timer"""
    session_id: int

class WorkSessionLog(WorkSessionBase):
    """Used to manually log a session"""
    start_time: datetime
    end_time: datetime

class WorkSessionDelete(BaseModel):
    """Used to delete a session"""
    session_id: int

class ProjectIdeaRequest(BaseModel):
    description: str  # User's input for idea generation

class WorkSessionResponse(BaseModel):
    id: int
    project_id: int
    start_time: datetime
    end_time: Optional[datetime]
    duration_hours: Optional[float]
    method: str  # "manual" or "timer"

    class Config:
        from_attributes = True

class Project(ProjectBase):
    id: int
    total_hours: float
    tasks: List[Task] = []

    work_sessions: List[WorkSessionResponse] = []
    class Config:
        orm_mode = True