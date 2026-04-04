from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import secret_key, algorithm, access_token_expires_in
from app.models.user import User
from app.db import get_session

#password hashing
pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str)-> str:
    return pswd_context.hash(password)

def verify_pass(plain_password:str, hashed_password:str)->bool:
    return pswd_context.verify(plain_password, hashed_password)

#token handling (JWT)
#create jwt token with userid and role
def create_access_token(user_id:int, role:str)->str:
    expire= datetime.utcnow()+timedelta(minutes=access_token_expires_in)
    payload = {"sub":str(user_id), "role":role, "expire":int(expire.timestamp())}
    return jwt.encode(payload, secret_key, algorithm=algorithm)

#auth dependency for secure endpoints
security = HTTPBearer()

#fastapi dependency to get current user from token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session=Depends(get_session))-> User:
    token = credentials.credentials
    #decoding token
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    #fetch user
    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User's inactive")
    return user
