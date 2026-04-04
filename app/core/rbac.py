from app.models.user import User, Role
from app.core.auth import get_current_user
from fastapi import Depends, HTTPException, status

#dependency to check user role for access cntrol
class CheckRole:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles=allowed_roles
    
    def __call__(self, current_user: User=Depends(get_current_user))->User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {[r.value for r in self.allowed_roles]}"
            )
        return current_user

allow_admin = CheckRole([Role.admin])
allow_analyst = CheckRole([Role.analyst, Role.admin])
allow_all = CheckRole([Role.admin, Role.analyst, Role.viewer])