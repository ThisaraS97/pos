from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class ExpenseCategory(Base):
    __tablename__ = "expense_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<ExpenseCategory {self.name}>"

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("expense_categories.id"), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    reference = Column(String, nullable=True)
    recorded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Expense {self.description}>"
