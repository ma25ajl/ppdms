# database.py
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name='patient_data.db'):
        self.db_name = os.path.join(os.path.dirname(__file__), db_name)
        print(f"📁 DatabaseManager using: {self.db_name}")
        self.init_db()
        
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Secure Lookup Table for identifiable information (encrypted)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS secure_lookup (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pseudonym_id TEXT UNIQUE NOT NULL,
                encrypted_data BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Clinical Data Table (pseudonymised)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clinical_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pseudonym_id TEXT NOT NULL,
                diagnosis TEXT,
                treatment TEXT,
                lab_results TEXT,
                visit_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database tables initialized")
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn