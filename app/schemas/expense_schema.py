from pydantic import BaseModel
from app.models.expense_model import ExpenseCategory

class ExpenseBase(BaseModel):
  description: str
  amount: int

class ExpenseCreate(ExpenseBase):
  category: ExpenseCategory
  user_id: int