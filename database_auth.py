"""
Database setup for User Authentication
"""

import sqlite3

def init_auth_database():
    """Initialize database with users and expenses tables"""
    connection = sqlite3.connect('expense_tracker.db')
    cursor = connection.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create expenses table with user_id
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON expenses(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON expenses(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON expenses(category)")
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("✅ Authentication database initialized!")

if __name__ == "__main__":
    init_auth_database()