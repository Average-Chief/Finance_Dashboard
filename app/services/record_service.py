from app.models.record import RecordType, FinancialRecord
from app.schemas.record import RecordCreate, RecordUpdate
from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import date, datetime
from typing import Optional

#create new record
def create_record(session:Session, record_data: RecordCreate, user_id:int)-> FinancialRecord:
    if record_data.amount<=0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    record = FinancialRecord(**record_data.model_dump(), created_by=user_id)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

#get non-deleted records with optional filters and pagination
def get_records(
    session: Session,
    record_type: Optional[RecordType]=None, 
    category: Optional[str]=None, 
    start_date: Optional[date]=None,
    end_date: Optional[date]=None,
    skip: int=0,
    limit: int=50,
)-> list[FinancialRecord]:
        
    query = select(FinancialRecord).where(FinancialRecord.is_deleted==False)

    if record_type:
        query = query.where(FinancialRecord.type==record_type)
    if category:
        query = query.where(FinancialRecord.category==category)
    if start_date:
        query = query.where(FinancialRecord.date>=start_date)
    if end_date:
        query = query.where(FinancialRecord.date<=end_date)
    
    query = query.order_by(FinancialRecord.date.desc()).offset(skip).limit(limit)
    return list(session.exec(query).all())

#get single record
def get_record_by_id(session: Session, record_id:int)-> FinancialRecord:
    record = session.get(FinancialRecord, record_id)
    if not record or record.is_deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

#update record
def update_record(session: Session, record_id:int, record_data: RecordUpdate)-> FinancialRecord:
    record = get_record_by_id(session, record_id)
    update_data = record_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    for key, value in update_data.items():
        setattr(record, key, value)
    
    record.updated_at = datetime.utcnow()
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

#delete record (soft delete)
def delete_record(session: Session, record_id:int)-> None:
    record = get_record_by_id(session, record_id)
    record.is_deleted = True
    record.updated_at=datetime.utcnow()
    session.delete(record)
    session.commit()