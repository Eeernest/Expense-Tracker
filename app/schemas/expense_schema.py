from pydantic import BaseModel, ConfigDict
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

  model_config = ConfigDict(from_attributes=True)

class ExpenseDate(str, enum.Enum):
  today = "today"
  seven_days = "last 7 days"
  thirty_days = "last 30 days"
  ninety_days = "last 90 days"
  current_month = "Current month"

class ExpenseEdit(BaseModel):
  expense_id: int