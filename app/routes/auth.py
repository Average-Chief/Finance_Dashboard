from app.db import get_session
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.services.user_service import register_user, get_user_by_email
from app.core.auth import verify_pass, create_access_token, get_current_user
from app.core.rate_limit import limit_auth
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])

#register route
#default role viewer
@router.post("/register", response_model=UserResponse, status_code=201)
@limit_auth
def register(request:Request, user_data: UserRegister, session: Session=Depends(get_session)):
    user = register_user(session, user_data)
    return user

#login route
#authenticate and recieve a jwt token
@router.post("/login", response_model=TokenResponse)
@limit_auth
def login(request:Request, user_data: UserLogin, session: Session=Depends(get_session)):
    user = get_user_by_email(session, user_data.email)
    if not user or not verify_pass(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")
    token = create_access_token(user.id, user.role.value)
    return TokenResponse(access_token=token, role=user.role.value)

#user profile route
#only accessible by authenticated users
@router.get("/me", response_model=UserResponse)
@limit_auth
def my_profile(request:Request, current_user: User=Depends(get_current_user)):
    return current_user
    