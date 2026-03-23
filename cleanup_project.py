# cleanup_project.py
import os
import shutil

print("=" * 70)
print("PROJECT CLEANUP - Remove Unnecessary Files")
print("=" * 70)

# Files to keep (core project files)
keep_files = {
    'app.py',
    'database.py',
    'models.py',
    'requirements.txt',
    'encryption.key',
    'patient_data.db',
    'templates',
    'static'
}

# Files to remove (temporary/test files)
remove_patterns = [
    'working_populate.py',
    'add_more_patients.py',
    'populate_data.py',
    'clean_database.py',
    'test_',
    'debug_',
    'manual_test.py',
    'emergency_fix.py',
    'reset_database.py',
    'drop_tables.py',
    'fresh_start.py',
    'clean_and_populate',
    'populate_fresh.py',
    'debug_key.py',
    'test_imports.py',
    'complete_reset.py',
    'working_populate.py',
    '.db-journal',
    'test.db'
]

# Also remove any backup files
backup_patterns = ['*.bak', '*.backup', '*.old']

print("\n📁 Current files:")
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    print(f"   • {f}")

print("\n🗑️  Files to remove:")
removed_count = 0

for file in os.listdir('.'):
    file_path = os.path.join('.', file)
    
    # Skip directories
    if os.path.isdir(file_path):
        continue
    
    # Check if file should be removed
    remove = False
    
    # Check patterns
    for pattern in remove_patterns:
        if pattern in file:
            remove = True
            break
    
    # Check if it's a backup file
    for pattern in backup_patterns:
        if file.endswith(pattern.replace('*', '')):
            remove = True
            break
    
    # Don't remove core files
    if file in keep_files:
        remove = False
    
    if remove:
        try:
            os.remove(file_path)
            print(f"   ✓ Removed: {file}")
            removed_count += 1
        except Exception as e:
            print(f"   ✗ Error removing {file}: {e}")

# Also remove any .pyc files and __pycache__
import glob
for pyc in glob.glob('**/*.pyc', recursive=True):
    os.remove(pyc)
    print(f"   ✓ Removed: {pyc}")

for cache in glob.glob('**/__pycache__', recursive=True):
    shutil.rmtree(cache)
    print(f"   ✓ Removed: {cache}")

print(f"\n✅ Removed {removed_count} unnecessary files")

print("\n" + "=" * 70)
print("CLEANUP COMPLETE!")
print("=" * 70)

print("\n📁 Remaining core files:")
remaining = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in sorted(remaining):
    size = os.path.getsize(f)
    if size > 1024:
        size_str = f"{size/1024:.1f} KB"
    else:
        size_str = f"{size} B"
    print(f"   • {f} ({size_str})")

print("\n📁 Folders:")
folders = [f for f in os.listdir('.') if os.path.isdir(f)]
for folder in sorted(folders):
    print(f"   • {folder}/")