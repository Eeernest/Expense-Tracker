from fastapi import Depends
from app.db.database import SessionDep
from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService
from typing import Annotated

def get_expense_service(session: SessionDep):
  repo = ExpenseRepository(session)
  return ExpenseService(repo)

ExpenseDep = Annotated[ExpenseService, Depends(get_expense_service)]