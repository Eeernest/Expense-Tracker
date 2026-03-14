from pydantic import BaseModel
import enum

from app.models.expense_model import ExpenseCategory

class ExpenseBase(BaseModel):
  description: str
  amount: int

class ExpenseRead(ExpenseBase):
  id: int
  category: ExpenseCategory
  date: str

class ExpenseDate(str, enum.Enum):
  one_week = "one week"
  one_month = "one month"
  three_months = "three months"