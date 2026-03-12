import enum
from datetime import datetime, timezone
from sqlalchemy import Integer, String, Column, Enum, DateTime, ForeignKey
from app.db.database import Base

class ExpenseCategory(str, enum.Enum):
  housing = "Housing"
  food = "Food"
  transportation = "Transportation"
  healthcare = "Healthcare"
  entertainment = "Entertainment"
  savings = "Savings"

class Expense(Base):
  __tablename__ = "expense"

  id = Column(Integer, primary_key=True)
  description = Column(String, nullable=False, index=True, unique=True)
  amount = Column(Integer, nullable=False, index=True)
  date = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
  category = Column(Enum(ExpenseCategory), index=True, nullable=False)
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  user_id = Column(Integer, ForeignKey("users.id"))