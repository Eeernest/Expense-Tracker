from fastapi import APIRouter, Query
from app.models.expense_model import ExpenseCategory
from app.schemas.expense_schema import ExpenseBase, ExpenseRead, ExpenseDate
from app.dependencies.expense_dependency import ExpenseDep

from app.dependencies.permit_dependency import CurrentUserDep

from typing import Annotated

router = APIRouter()

@router.post("/expenses/", response_model=ExpenseRead)
def add_expense(
  category: ExpenseCategory,
  expense: ExpenseBase,
  user: CurrentUserDep,
  service: ExpenseDep
):
  return service.add_expense(category, expense, user)

@router.get("/expenses/", response_model=list[ExpenseRead])
def view_expense(
  service: ExpenseDep,
  user: CurrentUserDep,
  date: ExpenseDate,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100,
  category: ExpenseCategory | None = None
):
  if date:
    return service.view_date(user, date, offset, limit, category)
  
  return service.view_all(user, offset, limit, category)