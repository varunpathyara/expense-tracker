"""
User authentication models
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

def get_db_connection():
    connection = sqlite3.connect('expense_tracker.db')
    connection.row_factory = sqlite3.Row
    return connection

class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
    
    @staticmethod
    def create_user(username, email, password):
        """Create a new user"""
        password_hash = generate_password_hash(password)
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return User(user_id, username, email, password_hash)
        except sqlite3.IntegrityError:
            cursor.close()
            connection.close()
            return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if row:
            return User(row['id'], row['username'], row['email'], row['password_hash'])
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if row:
            return User(row['id'], row['username'], row['email'], row['password_hash'])
        return None
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)