from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
from models import IWill, Task
from notifications import send_email_notification

scheduler = BackgroundScheduler()

def check_upcoming_notifications():
    """Checks for upcoming 'I Wills' and tasks and sends notifications"""
    db: Session = SessionLocal()
    now = datetime.utcnow()

    # Get all I Wills with upcoming notifications
    i_wills = db.query(IWill).filter(IWill.notification_time <= now, IWill.completed == False).all()
    
    for i_will in i_wills:
        email_subject = f"Reminder: {i_will.action}"
        email_message = f"Hey! Don't forget to complete: {i_will.action} today."
        send_email_notification("smith.witt@gmail.com", email_subject, email_message)

    # Get all tasks with upcoming due dates
    tasks = db.query(Task).filter(Task.due_date <= now).all()

    for task in tasks:
        email_subject = f"Task Due Soon: {task.title}"
        email_message = f"Your task '{task.title}' is due soon. Stay on track!"
        #send_email_notification("recipient@example.com", email_subject, email_message)

    db.close()

# Schedule the job to run every minute
if not scheduler.running:
    scheduler.add_job(check_upcoming_notifications, "interval", minutes=1)
    scheduler.start()
