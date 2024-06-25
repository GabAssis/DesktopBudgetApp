# app/utils/db_utils.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.database import SessionLocal

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, username: str, password: str):
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def update_user(db: Session, user_id: int, username: str, password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.username = username
        user.password = password
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
