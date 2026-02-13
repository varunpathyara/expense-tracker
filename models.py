"""
Models module for Expense Tracker
Contains Expense class and database operations
"""

from datetime import datetime
from database_sqlite import get_db_connection

class Expense:
    """
    Expense model class
    Represents a single expense entry
    """
    
    def __init__(self, amount, category, date, description="", expense_id=None):
        self.id = expense_id
        self.amount = float(amount)
        self.category = category
        self.date = date if isinstance(date, str) else date.strftime('%Y-%m-%d')
        self.description = description
    
    def save(self):
        """
        Save expense to database
        
        Returns:
            int: ID of the saved expense
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        if self.id:
            # Update existing expense
            query = """
            UPDATE expenses 
            SET amount = ?, category = ?, date = ?, description = ?
            WHERE id = ?
            """
            cursor.execute(query, (self.amount, self.category, self.date, 
                                 self.description, self.id))
        else:
            # Insert new expense
            query = """
            INSERT INTO expenses (amount, category, date, description)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (self.amount, self.category, self.date, 
                                 self.description))
            self.id = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return self.id
    
    @staticmethod
    def get_all(limit=None, offset=0):
        """
        Get all expenses from database
        
        Args:
            limit (int): Maximum number of records to fetch
            offset (int): Number of records to skip
            
        Returns:
            list: List of expense dictionaries
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = "SELECT * FROM expenses ORDER BY date DESC, created_at DESC"
        
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        expenses = []
        
        for row in cursor.fetchall():
            expense_dict = dict(zip(columns, row))
            # Convert date to string for JSON serialization
            if expense_dict.get('date') and not isinstance(expense_dict['date'], str):
                expense_dict['date'] = expense_dict['date'].strftime('%Y-%m-%d')
            expenses.append(expense_dict)
        
        cursor.close()
        connection.close()
        
        return expenses
    
    @staticmethod
    def get_by_id(expense_id):
        """
        Get expense by ID
        
        Args:
            expense_id (int): Expense ID
            
        Returns:
            dict: Expense data or None if not found
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = "SELECT * FROM expenses WHERE id = ?"
        cursor.execute(query, (expense_id,))
        
        row = cursor.fetchone()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            expense_dict = dict(zip(columns, row))
            if expense_dict.get('date') and not isinstance(expense_dict['date'], str):
                expense_dict['date'] = expense_dict['date'].strftime('%Y-%m-%d')
        else:
            expense_dict = None
        
        cursor.close()
        connection.close()
        
        return expense_dict
    
    @staticmethod
    def delete(expense_id):
        """
        Delete expense by ID
        
        Args:
            expense_id (int): Expense ID
            
        Returns:
            bool: True if deleted successfully
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = "DELETE FROM expenses WHERE id = ?"
        cursor.execute(query, (expense_id,))
        
        connection.commit()
        affected_rows = cursor.rowcount
        
        cursor.close()
        connection.close()
        
        return affected_rows > 0
    
    @staticmethod
    def get_by_date_range(start_date, end_date):
        """
        Get expenses within a date range
        
        Args:
            start_date (str): Start date (YYYY-MM-DD)
            end_date (str): End date (YYYY-MM-DD)
            
        Returns:
            list: List of expense dictionaries
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = """
        SELECT * FROM expenses 
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
        """
        cursor.execute(query, (start_date, end_date))
        
        columns = [desc[0] for desc in cursor.description]
        expenses = []
        
        for row in cursor.fetchall():
            expense_dict = dict(zip(columns, row))

            if expense_dict.get('date') and not isinstance(expense_dict['date'], str):
                expense_dict['date'] = expense_dict['date'].strftime('%Y-%m-%d')

            expenses.append(expense_dict)
        
        cursor.close()
        connection.close()
        
        return expenses


