from pydantic import BaseModel
from typing import Optional
from datetime import date

class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    total_records: int
    top_category: Optional[str]
    top_category_total: Optional[float]

class CategoryTotal(BaseModel):
    category: str
    type: str
    total: float

class MonthlyTrend(BaseModel):
    month: str
    income: float
    expenses: float
    net: float

class RecentRecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    currency: str
    date: date
    description: Optional[str]
    model_config= {"from_attributes": True}
    