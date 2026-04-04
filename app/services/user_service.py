from app.models.user import User, Role
from app.core.auth import hash_password
from app.schemas.user import UserRegister
from sqlmodel import Session, select
from fastapi import HTTPException

#register new user
def register_user(session: Session, user_data: UserRegister, role:Role = Role.viewer)-> User:
    #check if email already exists
    existing_user = session.exec(select(User).where(User.email==user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hash_password(user_data.password),
        role=role
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def get_user_by_email(session: Session, email:str)-> User:
    return session.exec(select(User).where(User.email==email)).first()

def get_all_users(session: Session)-> list[User]:
    return session.exec(select(User)).all()

def get_user_by_id(session: Session, user_id:int)-> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_role(session: Session, user_id: int, new_role:Role)->User:
    user = get_user_by_id(session, user_id)
    user.role = new_role
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_status(session: Session, user_id:int, is_active:bool)->User:
    user = get_user_by_id(session, user_id)
    user.is_active = is_active
    session.add(user)
    session.commit()
    session.refresh(user)
    return user