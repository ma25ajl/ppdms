from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from database import DatabaseManager
from models import SecurityManager, PatientManager

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize managers
db_manager = DatabaseManager()
security_manager = SecurityManager()
patient_manager = PatientManager(db_manager, security_manager)

# Mock user system for demonstration
USERS = {
    'admin': {'password_hash': security_manager.hash_password('admin123'), 'role': 'admin'},
    'researcher': {'password_hash': security_manager.hash_password('research123'), 'role': 'researcher'},
    'clinician': {'password_hash': security_manager.hash_password('clinic123'), 'role': 'clinician'}
}

def login_required(role=None):
    """Decorator to require login and optionally specific role"""
    def decorator(f):
        from functools import wraps
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

# ... after your add_patient route ...

@app.route('/add-clinical-data', methods=['GET', 'POST'])
@login_required(role='clinician')
def add_clinical_data():
    if request.method == 'POST':
        # Get form data
        pseudonym_id = request.form['pseudonym_id'].strip().upper()
        diagnosis = request.form['diagnosis']
        treatment = request.form.get('treatment', '')
        lab_results = request.form.get('lab_results', '')
        visit_date = request.form['visit_date']
        visit_type = request.form.get('visit_type', 'Routine Checkup')
        clinical_notes = request.form.get('clinical_notes', '')
        medication = request.form.get('medication', '')
        
        # Validate pseudonym ID exists
        if not patient_manager.verify_pseudonym_id(pseudonym_id):
            flash(f'Invalid Pseudonym ID: {pseudonym_id}. Please check and try again.', 'error')
            return redirect(url_for('add_clinical_data'))
        
        # Combine additional clinical data
        additional_data = {
            'visit_type': visit_type,
            'clinical_notes': clinical_notes,
            'medication': medication
        }
        
        # Add to database
        try:
            patient_manager.add_clinical_data(
                pseudonym_id=pseudonym_id,
                diagnosis=diagnosis,
                treatment=treatment,
                lab_results=f"{lab_results}\nAdditional Data: {additional_data}",
                visit_date=visit_date
            )
            flash(f'Clinical data added successfully for {pseudonym_id}!', 'success')
            return redirect(url_for('add_clinical_data'))
            
        except Exception as e:
            flash(f'Error adding clinical data: {str(e)}', 'error')
            return redirect(url_for('add_clinical_data'))
    
    # GET request - show the form
    return render_template('add_clinical_data.html')

# ... continue with other routes ...

@app.route('/add-clinical-data', methods=['GET', 'POST'])
@login_required(role='clinician')
def add_clinical_data():
    if request.method == 'POST':
        pseudonym_id = request.form['pseudonym_id']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        lab_results = request.form['lab_results']
        visit_date = request.form['visit_date']
        
        if not patient_manager.verify_pseudonym_id(pseudonym_id):
            flash('Invalid Pseudonym ID.', 'error')
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

from datetime import datetime

@app.route('/reidentify', methods=['GET', 'POST'])
@login_required(role='admin')
def reidentify():
    patient_info = None
    if request.method == 'POST':
        pseudonym_id = request.form['pseudonym_id'].strip().upper()
        reason = request.form.get('reason', '')
        notes = request.form.get('notes', '')
        
        # Log the access attempt
        print(f"Re-identification attempted by {session.username} for {pseudonym_id}. Reason: {reason}")
        
        patient_info = patient_manager.reidentify_patient(pseudonym_id)
        
        if patient_info:
            flash('Patient re-identified successfully. Access logged.', 'success')
        else:
            flash('Patient not found or invalid pseudonym ID.', 'error')
    
    return render_template('reidentify.html', 
                         patient_info=patient_info,
                         now=datetime.now())

if __name__ == '__main__':
    app.run(debug=True)