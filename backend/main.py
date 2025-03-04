from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List
import models, schemas, database
import llm_api
from database import SessionLocal, engine
from database import init_db
from scheduler import scheduler
from google_calendar import create_calendar_event
from datetime import datetime as dt


# Start background task scheduler
if not scheduler.running:
    scheduler.start()



# Ensure database tables are created
init_db()


# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------- I Wills Endpoints -------- #

@app.post("/i_wills", response_model=schemas.IWill)
def create_i_will(i_will: schemas.IWillCreate, db: Session = Depends(get_db)):
    db_i_will = models.IWill(**i_will.dict())
    db.add(db_i_will)
    db.commit()
    db.refresh(db_i_will)
    if db_i_will.time:
        start_datetime = dt.combine(db_i_will.date, db_i_will.time)
        end_datetime = start_datetime + timedelta(hours=1)  # Default 1-hour event
        event_link = create_calendar_event(
            f"I Will: {db_i_will.action}",
            start_datetime.isoformat(),
            end_datetime.isoformat()
        )
        db_i_will.event_link = event_link
        db.commit()

    return db_i_will

@app.get("/i_wills", response_model=List[schemas.IWill])
def get_all_i_wills(db: Session = Depends(get_db)):
    return db.query(models.IWill).all()

@app.get("/i_wills/{task_date}", response_model=List[schemas.IWill])
def get_i_wills_by_date(task_date: date, db: Session = Depends(get_db)):
    return db.query(models.IWill).filter(models.IWill.date == task_date).all()

@app.put("/i_wills/{i_will_id}", response_model=schemas.IWill)
def update_i_will(i_will_id: int, i_will_update: schemas.IWillUpdate, db: Session = Depends(get_db)):
    i_will = db.query(models.IWill).filter(models.IWill.id == i_will_id).first()
    if not i_will:
        raise HTTPException(status_code=404, detail="I Will not found")

    for key, value in i_will_update.dict(exclude_unset=True).items():
        setattr(i_will, key, value)

    db.commit()
    db.refresh(i_will)
    return i_will

@app.delete("/i_wills/{i_will_id}")
def delete_i_will(i_will_id: int, db: Session = Depends(get_db)):
    i_will = db.query(models.IWill).filter(models.IWill.id == i_will_id).first()
    if not i_will:
        raise HTTPException(status_code=404, detail="I Will not found")

    db.delete(i_will)
    db.commit()
    return {"message": "I Will deleted successfully"}


from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import google_calendar  # Import the new module

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/calendar/week")
def get_weekly_events(
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format")
):
    try:
        events = google_calendar.get_weekly_events(start_date, end_date)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/projects", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects", response_model=List[schemas.Project])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@app.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project_update: schemas.ProjectCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

@app.post("/projects/{project_id}/tasks", response_model=schemas.Task)
def add_task(project_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_task = models.Task(**task.dict(), project_id=project_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    if db_task.due_date:
        start_datetime = dt.combine(db_task.due_date, dt.min.time())  # Start of the day
        end_datetime = start_datetime + timedelta(hours=1)  # Default 1-hour event
        event_link = create_calendar_event(
            f"Task: {db_task.title}",
            start_datetime.isoformat(),
            end_datetime.isoformat()
        )
        db_task.event_link = event_link
        db.commit()


    return db_task

@app.get("/projects/{project_id}/tasks", response_model=List[schemas.Task])
def get_tasks(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()

@app.put("/projects/{project_id}/tasks/{task_id}", response_model=schemas.Task)
def update_task(project_id: int, task_id: int, task_update: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.project_id == project_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

@app.delete("/projects/{project_id}/tasks/{task_id}")
def delete_task(project_id: int, task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.project_id == project_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@app.post("/work_sessions/start", response_model=schemas.WorkSessionResponse)
def start_work_session(session: schemas.WorkSessionStart, db: Session = Depends(get_db)):
    """Start a work session timer."""
    new_session = models.WorkSession(
        project_id=session.project_id,
        start_time=dt.utcnow(),
        method="timer"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@app.post("/work_sessions/stop", response_model=schemas.WorkSessionResponse)
def stop_work_session(session: schemas.WorkSessionStop, db: Session = Depends(get_db)):
    """Stop a work session timer and calculate duration."""
    work_session = db.query(models.WorkSession).filter(
        models.WorkSession.id == session.session_id,
        models.WorkSession.end_time == None
    ).first()

    if not work_session:
        raise HTTPException(status_code=404, detail="No active work session found")

    work_session.end_time = dt.utcnow()
    work_session.duration_hours = (work_session.end_time - work_session.start_time).total_seconds() / 3600
    db.commit()
    db.refresh(work_session)

    # Update project's total hours
    project = db.query(models.Project).filter(models.Project.id == work_session.project_id).first()
    if project:
        project.total_hours += work_session.duration_hours
        db.commit()

    return work_session

@app.post("/work_sessions/log", response_model=schemas.WorkSessionResponse)
def log_manual_work_session(session: schemas.WorkSessionLog, db: Session = Depends(get_db)):
    """Manually log a work session."""
    if session.end_time <= session.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    duration_hours = (session.end_time - session.start_time).total_seconds() / 3600
    new_session = models.WorkSession(
        project_id=session.project_id,
        start_time=session.start_time,
        end_time=session.end_time,
        duration_hours=duration_hours,
        method="manual"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # Update project's total hours
    project = db.query(models.Project).filter(models.Project.id == session.project_id).first()
    if project:
        project.total_hours += duration_hours
        db.commit()

    return new_session

@app.delete("/work_sessions/delete", response_model=dict)
def delete_work_session(session: schemas.WorkSessionDelete, db: Session = Depends(get_db)):
    """Delete a work session."""
    work_session = db.query(models.WorkSession).filter(models.WorkSession.id == session.session_id).first()

    if not work_session:
        raise HTTPException(status_code=404, detail="Work session not found")

    # Deduct time from the project's total hours
    project = db.query(models.Project).filter(models.Project.id == work_session.project_id).first()
    if project and work_session.duration_hours:
        project.total_hours -= work_session.duration_hours
        db.commit()

    db.delete(work_session)
    db.commit()

    return {"message": "Work session deleted successfully"}


@app.post("/llm/project_idea")
def get_project_idea(request: schemas.ProjectIdeaRequest):
    """Generates a project idea using an LLM (GPT-4)."""
    try:
        idea = llm_api.generate_project_idea(request.description)
        return {"project_idea": idea}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))