import hashlib
import secrets
import json
import os
from cryptography.fernet import Fernet
import sqlite3

class SecurityManager:
    def __init__(self, key_file='encryption.key'):
        # Use absolute path to ensure consistent file location
        self.key_file = os.path.join(os.path.dirname(__file__), key_file)
        print(f"🔑 SecurityManager using key file: {self.key_file}")
        self.key = self._load_or_create_key()
        self.cipher_suite = Fernet(self.key)
    
    def _load_or_create_key(self):
        """Load existing key or create a new one"""
        if os.path.exists(self.key_file):
            # Load existing key
            with open(self.key_file, 'rb') as f:
                key = f.read()
            print(f"🔑 Loaded existing encryption key from {self.key_file}")
            return key
        else:
            # Create new key
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            print(f"🔑 Created NEW encryption key in {self.key_file}")
            return key
    
    def generate_pseudonym_id(self):
        """Generate a unique pseudonym ID (6 chars for compatibility)"""
        return f"P-{secrets.token_hex(3).upper()}"
    
    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        if isinstance(data, dict):
            data = json.dumps(data)
        return self.cipher_suite.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        try:
            decrypted = self.cipher_suite.decrypt(encrypted_data)
            return json.loads(decrypted.decode())
        except Exception as e:
            print(f"❌ Decryption error: {e}")
            return None
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()


class PatientManager:
    def __init__(self, db_manager, security_manager):
        self.db = db_manager
        self.security = security_manager
        print(f"✅ PatientManager initialized")
    
    def add_patient(self, name, nhs_number, date_of_birth, email="", phone=""):
        """Add a new patient and generate pseudonym ID"""
        pseudonym_id = self.security.generate_pseudonym_id()
        
        # Prepare identifiable data
        identifiable_data = {
            'name': name,
            'nhs_number': nhs_number,
            'date_of_birth': date_of_birth,
            'email': email,
            'phone': phone
        }
        
        # Encrypt the identifiable data
        encrypted_data = self.security.encrypt_data(identifiable_data)
        
        # Store in secure lookup table
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO secure_lookup (pseudonym_id, encrypted_data) VALUES (?, ?)',
            (pseudonym_id, encrypted_data)
        )
        conn.commit()
        conn.close()
        
        print(f"✅ Added patient: {name} -> {pseudonym_id}")
        return pseudonym_id
    
    def add_clinical_data(self, pseudonym_id, diagnosis, treatment, lab_results, visit_date):
        """Add clinical data linked to pseudonym ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clinical_data'")
            if not cursor.fetchone():
                print("Creating clinical_data table...")
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
            
            # Insert data
            cursor.execute(
                '''INSERT INTO clinical_data 
                   (pseudonym_id, diagnosis, treatment, lab_results, visit_date) 
                   VALUES (?, ?, ?, ?, ?)''',
                (pseudonym_id, diagnosis, treatment, lab_results, visit_date)
            )
            conn.commit()
            
            print(f"✅ Added clinical data for {pseudonym_id}")
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error in add_clinical_data: {str(e)}")
            if 'conn' in locals():
                conn.close()
            return False
    
    def get_clinical_data(self, pseudonym_id=None):
        """Get clinical data (pseudonymised)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        if pseudonym_id:
            cursor.execute(
                'SELECT * FROM clinical_data WHERE pseudonym_id = ? ORDER BY visit_date DESC',
                (pseudonym_id,)
            )
        else:
            cursor.execute('SELECT * FROM clinical_data ORDER BY visit_date DESC')
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        columns = ['id', 'pseudonym_id', 'diagnosis', 'treatment', 'lab_results', 'visit_date', 'created_at']
        return [dict(zip(columns, row)) for row in results]
    
    def reidentify_patient(self, pseudonym_id):
        """Re-identify patient (authorized users only)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT encrypted_data FROM secure_lookup WHERE pseudonym_id = ?',
            (pseudonym_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            encrypted_data = result[0]
            return self.security.decrypt_data(encrypted_data)
        return None
    
    def verify_pseudonym_id(self, pseudonym_id):
        """Verify if a pseudonym ID exists"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT 1 FROM secure_lookup WHERE pseudonym_id = ?',
            (pseudonym_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None