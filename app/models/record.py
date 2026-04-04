from enum import Enum
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class RecordType(str, Enum):
    income = "income"
    expense = "expense"

#financial record table
class FinancialRecord(SQLModel, table=True):
    id: Optional[int]= Field(default=None, primary_key=True)
    amount: float = Field(gt=0, description="amount must be greater than zero")
    type: RecordType
    date: date
    category:str = Field(max_length=50, index=True)
    currency: str= Field(default="INR", max_length=3)
    description: Optional[str]= Field(default=None, max_length=255)
    #ownedship
    created_by: int = Field(foreign_key="user.id", index=True)
    #timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    #soft delete
    is_deleted: bool = Field(default=False, index=True)