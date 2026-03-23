from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from database import DatabaseManager
from models import SecurityManager, PatientManager
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)

# IMPORTANT: Use the EXISTING key file
# The key file 'encryption.key' was created by working_populate.py
key_file = os.path.join(os.path.dirname(__file__), 'encryption.key')

print("=" * 50)
print("Starting Flask Application")
print(f"Current directory: {os.path.dirname(__file__)}")
print(f"Key file path: {key_file}")
print(f"Key file exists: {os.path.exists(key_file)}")
print("=" * 50)

# Initialize managers with the existing key
db_manager = DatabaseManager('patient_data.db')
security_manager = SecurityManager(key_file)  # Pass the key file path
patient_manager = PatientManager(db_manager, security_manager)

# Mock user system
USERS = {
    'admin': {'password_hash': security_manager.hash_password('admin123'), 'role': 'admin'},
    'researcher': {'password_hash': security_manager.hash_password('research123'), 'role': 'researcher'},
    'clinician': {'password_hash': security_manager.hash_password('clinic123'), 'role': 'clinician'}
}

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Please log in first.', 'error')
                return redirect(url_for('login'))
            if role and USERS.get(session['username'], {}).get('role') != role:
                flash('Insufficient permissions.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = USERS.get(username)
        if user and security_manager.hash_password(password) == user['password_hash']:
            session['username'] = username
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/add-patient', methods=['GET', 'POST'])
@login_required(role='admin')
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        nhs_number = request.form['nhs_number']
        date_of_birth = request.form['date_of_birth']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        
        pseudonym_id = patient_manager.add_patient(name, nhs_number, date_of_birth, email, phone)
        flash(f'Patient added successfully! Pseudonym ID: {pseudonym_id}', 'success')
        return redirect(url_for('add_patient'))
    
    return render_template('add_patient.html')

@app.route('/add-clinical-data', methods=['GET', 'POST'])
@login_required(role='clinician')
def add_clinical_data():
    if request.method == 'POST':
        pseudonym_id = request.form['pseudonym_id'].strip().upper()
        diagnosis = request.form['diagnosis']
        treatment = request.form.get('treatment', '')
        lab_results = request.form.get('lab_results', '')
        visit_date = request.form['visit_date']
        
        # Debug output
        print(f"\n🔍 Adding clinical data for {pseudonym_id}")
        
        if not patient_manager.verify_pseudonym_id(pseudonym_id):
            flash(f'Invalid Pseudonym ID: {pseudonym_id}', 'error')
            return redirect(url_for('add_clinical_data'))
        
        patient_manager.add_clinical_data(pseudonym_id, diagnosis, treatment, lab_results, visit_date)
        flash('Clinical data added successfully!', 'success')
        return redirect(url_for('add_clinical_data'))
    
    return render_template('add_clinical_data.html')

@app.route('/view-clinical-data')
@login_required()
def view_clinical_data():
    pseudonym_id = request.args.get('pseudonym_id')
    clinical_data = patient_manager.get_clinical_data(pseudonym_id)
    return render_template('view_clinical_data.html', clinical_data=clinical_data, pseudonym_id=pseudonym_id)

@app.route('/reidentify', methods=['GET', 'POST'])
@login_required(role='admin')
def reidentify():
    patient_info = None
    if request.method == 'POST':
        pseudonym_id = request.form['pseudonym_id'].strip().upper()
        
        print(f"\n🔍 Re-identification attempt for: {pseudonym_id}")
        
        try:
            patient_info = patient_manager.reidentify_patient(pseudonym_id)
            
            if patient_info:
                print(f"✅ Success: Found {patient_info.get('name')}")
                flash('Patient re-identified successfully. Access logged.', 'success')
            else:
                print(f"❌ Failed: No patient found with ID {pseudonym_id}")
                flash('Patient not found.', 'error')
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('reidentify.html', patient_info=patient_info, now=datetime.now())

@app.route('/debug')
def debug():
    """Debug route to check system status"""
    info = {
        'key_file_exists': os.path.exists('encryption.key'),
        'db_file_exists': os.path.exists('patient_data.db'),
        'tables': []
    }
    
    if info['db_file_exists']:
        import sqlite3
        conn = sqlite3.connect('patient_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        info['tables'] = [t[0] for t in tables]
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            info[f'{table[0]}_count'] = count
        
        conn.close()
    
    return render_template('debug.html', info=info)

if __name__ == '__main__':
    app.run(debug=True, port=5000)