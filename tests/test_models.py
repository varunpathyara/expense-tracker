"""
Unit tests for Expense Tracker
Run with: pytest tests/ -v
"""

import pytest
from models import Expense
from datetime import datetime

class TestExpense:
    """Test cases for Expense model"""
    
    def test_expense_creation(self):
        """Test creating an expense object"""
        expense = Expense(
            amount=100.50,
            category="Food & Dining",
            date="2025-02-13",
            description="Lunch at restaurant"
        )
        
        assert expense.amount == 100.50
        assert expense.category == "Food & Dining"
        assert expense.date == "2025-02-13"
        assert expense.description == "Lunch at restaurant"
    
    def test_expense_with_id(self):
        """Test creating expense with ID"""
        expense = Expense(
            amount=50.00,
            category="Transportation",
            date="2025-02-13",
            description="Taxi fare",
            expense_id=1
        )
        
        assert expense.id == 1
    
    def test_expense_amount_conversion(self):
        """Test amount is converted to float"""
        expense = Expense(
            amount="75.25",
            category="Shopping",
            date="2025-02-13"
        )
        
        assert isinstance(expense.amount, float)
        assert expense.amount == 75.25

# Add more tests as needed
# Example: Test database operations, API endpoints, etc.

def test_placeholder():
    """Placeholder test to ensure pytest runs"""
    assert True
