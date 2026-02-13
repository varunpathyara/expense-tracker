import sqlite3

def get_db_connection():
    connection = sqlite3.connect('expense_tracker.db')
    connection.row_factory = sqlite3.Row
    return connection

def init_database():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON expenses(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON expenses(category)")
    connection.commit()
    cursor.close()
    connection.close()
    print("Database initialized!")

def test_connection():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        connection.close()
        print("Connection successful!")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    init_database()
    test_connection()
    