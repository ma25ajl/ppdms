# Pseudonymised Patient Data Management System (PPDMS)

A secure patient data management system implementing pseudonymisation for GDPR-compliant medical research and clinical audit.

## Features

- **Pseudonymisation**: Patient identifiers encrypted with AES-256, separated from clinical data
- **Role-Based Access**: Admin, Clinician, and Researcher roles with different permissions
- **Secure Re-identification**: Authorized admin access with audit logging
- **Clinical Data Management**: Store and retrieve anonymised patient records
- **GDPR Compliant**: Implements data protection by design

## Technology Stack

- **Backend**: Python 3.8+ with Flask
- **Database**: SQLite with encryption at rest
- **Security**: Cryptography library (AES-256, Fernet)
- **Frontend**: HTML5, CSS3, JavaScript

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ma25ajl/ppdms.git
cd ppdms