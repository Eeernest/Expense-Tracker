from pydantic import BaseModel
from app.models.expense_model import ExpenseCategory

class ExpenseBase(BaseModel):
  description: str
  amount: int

class ExpenseRead(ExpenseBase):
  id: int
  category: ExpenseCategory