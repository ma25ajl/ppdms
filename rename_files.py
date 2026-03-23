# rename_files.py
import os

print("=" * 70)
print("RENAME FILES - Professional Structure")
print("=" * 70)

# Define renaming mappings
rename_map = {
    # Keep these as is (already well-named)
    # 'app.py' stays
    # 'database.py' stays
    # 'models.py' stays
    # 'requirements.txt' stays
    # 'encryption.key' stays
    # 'patient_data.db' stays
}

# Optional: Create a more organized structure with subdirectories
print("\n📁 Creating organized structure...")

# Create subdirectories if they don't exist
dirs_to_create = [
    'data',           # For database files
    'config',         # For configuration
    'scripts',        # For utility scripts
    'docs'            # For documentation
]

for dir_name in dirs_to_create:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"   ✓ Created: {dir_name}/")

# Move database and key to data folder (optional - uncomment if desired)
# import shutil
# if os.path.exists('patient_data.db'):
#     shutil.move('patient_data.db', 'data/patient_data.db')
#     print("   ✓ Moved patient_data.db to data/")
# 
# if os.path.exists('encryption.key'):
#     shutil.move('encryption.key', 'data/encryption.key')
#     print("   ✓ Moved encryption.key to data/")

print("\n" + "=" * 70)
print("✅ Rename complete!")
print("=" * 70)

print("\n💡 Recommended final structure:")
print("""
PPDMS/
├── app.py                 # Main Flask application
├── database.py            # Database manager
├── models.py              # Security & patient managers
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── add_patient.html
│   ├── add_clinical_data.html
│   ├── view_clinical_data.html
│   ├── reidentify.html
│   └── debug.html
├── static/                # CSS & static files
│   └── style.css
├── data/                  # Data files (optional)
│   ├── patient_data.db    # SQLite database
│   └── encryption.key     # Encryption key
├── scripts/               # Utility scripts (optional)
│   └── populate_data.py   # Data population script
└── docs/                  # Documentation (optional)
    └── README.md
""")