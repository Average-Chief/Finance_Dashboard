from app.db import get_session
from app.services.user_service import get_user_by_id, update_role, update_status, get_all_users
from app.schemas.user import UserResponse, UserRoleUpdate, UserStatusUpdate
from app.core.rbac import allow_admin
from app.core.rate_limit import limit_admin_write, limit_standard
from app.models.user import User
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

router = APIRouter(prefix="/users", tags=["Users"])

#list all users, admin only
@router.get("/", response_model=list[UserResponse])
@limit_standard
def users_list(request:Request,session: Session=Depends(get_session), current_user: User=Depends(allow_admin)):
    return get_all_users(session)

#get specific user by id, admin only
@router.get("/{user_id}", response_model=UserResponse)
@limit_standard
def user_detail(request:Request,user_id:int, session: Session=Depends(get_session), current_user: User=Depends(allow_admin)):
    return get_user_by_id(session, user_id)

#update role, admin only
@router.patch("/{user_id}/role", response_model=UserResponse)
@limit_admin_write
def change_role(request:Request,user_id: int, role_update: UserRoleUpdate, session: Session=Depends(get_session), current_user: User=Depends(allow_admin)):
    return update_role(session, user_id, role_update.role)

#activate/deactivate user, admin only
@router.patch("/{user_id}/status", response_model=UserResponse)
@limit_admin_write
def change_status(request:Request,user_id: int, status_update: UserStatusUpdate, session: Session=Depends(get_session), current_user:User=Depends(allow_admin)):
    return update_status(session, user_id, status_update.is_active)
