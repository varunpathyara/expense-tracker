"""
Models module for Expense Tracker - SQLite Version
Contains Expense class and database operations
"""

from datetime import datetime
from database_sqlite import get_db_connection

class Expense:
    """Expense model class"""
    
    def __init__(self, amount, category, date, description="", expense_id=None):
        self.id = expense_id
        self.amount = float(amount)
        self.category = category
        self.date = date if isinstance(date, str) else date.strftime('%Y-%m-%d')
        self.description = description
    
    def save(self):
        """Save expense to database"""
        connection = get_db_connection()
        cursor = connection.cursor()
        
        if self.id:
            cursor.execute('UPDATE expenses SET amount=?, category=?, date=?, description=? WHERE id=?',
                         (self.amount, self.category, self.date, self.description, self.id))
        else:
            from flask_login import current_user
            user_id = current_user.id if hasattr(current_user, 'id') else 1
            cursor.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                         (user_id, self.amount, self.category, self.date, self.description))
            self.id = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        connection.close()
        return self.id
    
    @staticmethod
    def get_all(limit=None, offset=0, user_id=None):
        """Get all expenses from database"""
        connection = get_db_connection()
        cursor = connection.cursor()
        
        if user_id:
            query = 'SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, created_at DESC'
            if limit:
                query += f' LIMIT {limit} OFFSET {offset}'
            cursor.execute(query, (user_id,))
        else:
            query = 'SELECT * FROM expenses ORDER BY date DESC, created_at DESC'
            if limit:
                query += f' LIMIT {limit} OFFSET {offset}'
            cursor.execute(query)
        
        expenses = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        return expenses
    
    @staticmethod
    def get_by_id(expense_id):
        """Get expense by ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        row = cursor.fetchone()
        expense_dict = dict(row) if row else None
        cursor.close()
        connection.close()
        return expense_dict
    
    @staticmethod
    def delete(expense_id):
        """Delete expense by ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        connection.close()
        return affected_rows > 0
    
    @staticmethod
    def get_by_date_range(start_date, end_date):
        """Get expenses within a date range"""
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC"
        cursor.execute(query, (start_date, end_date))
        expenses = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        return expenses
    
    @staticmethod
    def get_categories():
        """Get all unique categories"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT category FROM expenses ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        return categories

    @staticmethod
    def get_total_count():
        """Get total number of expenses"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM expenses")
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count