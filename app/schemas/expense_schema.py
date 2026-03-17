from pydantic import BaseModel
import enum
from datetime import datetime

from app.models.expense_model import ExpenseCategory

class ExpenseBase(BaseModel):
  description: str
  amount: float

class ExpenseRead(ExpenseBase):
  id: int
  category: ExpenseCategory
  date: datetime

class ExpenseDate(str, enum.Enum):
  today = "today"
  seven_days = "last 7 days"
  thirty_days = "last 30 days"
  ninety_days = "last 90 days"

class ExpenseEdit(BaseModel):
  expense_id: int