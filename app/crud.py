from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models import User, Task


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()



def get_user_by_username(db:Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username:str, email: str, password: str):
    hashed = hash_password(password)
    user = User(username= username, email=email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_some_task(db: Session, user_id: int, title: str, start_dt, description=None, end_dt=None):
    task = Task(user_id=user_id, title=title, description=description, start_dt=start_dt, end_dt=end_dt)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks_for_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).order_by(Task.start_dt).all()


def get_task_by_id(db: Session, user_id: int, task_id: int):
    return db.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()


def update_some_task(db: Session, task, **fields):
    for k, v in fields.items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task


def delete_some_task(db: Session, task):
    db.delete(task)
    db.commit()
