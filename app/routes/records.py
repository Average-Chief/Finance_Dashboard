from app.db import get_session
from app.models.user import User
from app.models.record import RecordType
from app.schemas.record import RecordCreate, RecordResponse, RecordUpdate
from app.services.record_service import create_record, get_records, get_record_by_id, update_record, delete_record
from app.core.rbac import allow_admin, allow_all
from app.core.rate_limit import limit_admin_write, limit_standard
from fastapi import APIRouter, Depends, Query, Request
from sqlmodel import Session
from datetime import date
from typing import Optional

router = APIRouter(prefix="/records", tags=["Records"])

#new record, admin only
@router.post("/", response_model=RecordResponse, status_code=201)
@limit_admin_write
def new_record(request:Request, record: RecordCreate, session: Session=Depends(get_session), current_user: User=Depends(allow_admin)):
    return create_record(session, record, current_user.id)

#record list with optional filters, anyone can access
@router.get("/", response_model=list[RecordResponse])
@limit_standard
def list_records(
    request:Request,
    session:Session=Depends(get_session),
    current_user:User=Depends(allow_all),
    type:Optional[RecordType]=Query(None, description="Filter by record type"),
    category: Optional[str]=Query(None, description="Filter by category"),
    start_date: Optional[date]=Query(None, description="Start Date [YYYY-MM-DD]"),
    end_date: Optional[date]=Query(None, description="End Date [YYYY-MM-DD]"),
    skip: int = Query(0, ge=0, description="No. of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Max no. of records to return")
):
    return get_records(session, type, category, start_date, end_date, skip, limit)

#get single record by id, anyone can access
@router.get("/{record_id}", response_model=RecordResponse)
@limit_standard
def get_record(request:Request, record_id: int, session: Session=Depends(get_session), current_user: User=Depends(allow_all)):
    return get_record_by_id(session, record_id)

#update record, admin only
@router.put("/{record_id}", response_model=RecordResponse)
@limit_admin_write
def modify_record(request:Request, record_id: int, record_data: RecordUpdate, session: Session=Depends(get_session),current_user:User=Depends(allow_admin)):
    return update_record(session, record_id, record_data)

#delete record, admin only
@router.delete("/{record_id}", status_code=204)
@limit_admin_write
def remove_record(request:Request, record_id: int, session: Session=Depends(get_session), current_user:User=Depends(allow_admin)):
    delete_record(session, record_id)
