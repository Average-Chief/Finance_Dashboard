from app.db import get_session
from app.schemas.dashboard import SummaryResponse, RecentRecordResponse
from app.services.dashboard_service import get_category_breakdown, get_dashboard_summary, recent_activity, get_monthly_trends
from app.core.rbac import allow_all, allow_analyst
from app.core.rate_limit import limit_dashboard
from app.models.user import User
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel import Session

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

#overall summary, anyone can access
@router.get("/summary", response_model=SummaryResponse)
@limit_dashboard
def dashboard_summary(request:Request,session: Session=Depends(get_session), current_user:User=Depends(allow_all)):
    return get_dashboard_summary(session)

#category breakdown, analyst and admin only
@router.get("/category-breakdown")
@limit_dashboard
def category_breakdown(request:Request,session: Session=Depends(get_session), current_user:User=Depends(allow_analyst)):
    return get_category_breakdown(session)

#monthly trends, analyst and admin only
@router.get("/monthly-trends")
@limit_dashboard
def trends(request:Request,session: Session=Depends(get_session), current_user:User=Depends(allow_analyst)):
    return get_monthly_trends(session)

#most recent activity, anyone can access
@router.get("/recent-activity", response_model=list[RecentRecordResponse])
@limit_dashboard
def recent(request:Request,limit:int=Query(10, ge=1, le=50, description="No. of recent records"), session:Session=Depends(get_session), current_user:User=Depends(allow_all)):
    return recent_activity(session, limit)
