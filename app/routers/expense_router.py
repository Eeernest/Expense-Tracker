from fastapi import APIRouter
from app.models.expense_model import ExpenseCategory
from app.schemas.expense_schema import ExpenseBase, ExpenseRead
from app.dependencies.expense_dependency import ExpenseDep

from app.dependencies.permit_dependency import CurrentUserDep

router = APIRouter()

@router.post("/expense/", response_model=ExpenseRead)
def add_expense(
  category: ExpenseCategory,
  expense: ExpenseBase,
  user: CurrentUserDep,
  service: ExpenseDep
):
  return service.add_expense(category, expense, user)