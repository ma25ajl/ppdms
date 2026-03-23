# Pseudonymised Patient Data Management System (PPDMS)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A secure patient data management system implementing **pseudonymisation** for GDPR-compliant medical research and clinical audit. This system demonstrates how healthcare organisations can balance data utility for research with strict privacy protection requirements.

## 🏥 Overview

The PPDMS addresses the critical challenge of protecting patient identities while enabling valuable medical research. It implements:

- **AES-256 encryption** for all identifiable patient information
- **Pseudonymisation** with reversible mapping for authorised access
- **Role-based access control** (Admin, Clinician, Researcher)
- **Separation of concerns** between identifiable and clinical data
- **GDPR-compliant** data protection by design

## ✨ Features

### 🔒 Security
- AES-256 encryption at rest
- Secure key management
- Role-based access control
- SQL injection prevention
- Audit logging for re-identification

### 👥 User Roles
| Role | Permissions |
|------|-------------|
| **Administrator** | Add patients, re-identify, full system access |
| **Clinician** | Add clinical data, view patient records |
| **Researcher** | View anonymised clinical data only |

### 📊 Data Management
- Patient registration with pseudonym generation
- Clinical data entry with diagnoses, treatments, lab results
- Secure re-identification for authorized users
- Clinical data filtering by pseudonym ID

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ma25ajl/ppdms.git
cd ppdms
