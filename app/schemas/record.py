from pydantic import BaseModel, Field
from datetime import date as DateType, datetime
from typing import Optional
from app.models.record import RecordType

#requests
class RecordCreate(BaseModel):
    amount: float = Field(gt=0, description="must be positive")
    type: RecordType
    category: str = Field(min_length=1, max_length=50)
    currency: str = Field(default="INR", max_length=3, description="ISO 4217 currency code")
    date: DateType
    description: Optional[str] = Field(default=None, max_length=500)

class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    currency: Optional[str] = Field(default=None, max_length=3)
    date: Optional[DateType] = None
    description: Optional[str] = Field(default=None, max_length=500)

#responses
class RecordResponse(BaseModel):
    id: int
    amount: float
    type: RecordType
    category: str
    currency: str
    date: DateType
    description: Optional[str]
    created_by: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}