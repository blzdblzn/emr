# EMR System with Accounting and HMO Reconciliation

## Overview
This document provides instructions for running and using the Electronic Medical Record (EMR) system with integrated accounting and HMO reconciliation features. The system is built using Flask and provides a comprehensive solution for healthcare providers to manage patient records, billing, and insurance claims.

## Features
- **Patient Management**: Registration, medical history, appointments
- **Clinical Features**: Visit documentation, prescriptions, lab orders
- **Accounting System**: Billing, invoicing, payment tracking
- **HMO Reconciliation**: Claim submission, tracking, and reconciliation
- **Reporting**: Financial reports, claim status, reconciliation audits

## System Requirements
- Python 3.11 or higher
- MySQL database
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd emr_system
```

### 2. Set Up Virtual Environment
```bash
cd emr_app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
The system is pre-configured to use MySQL with the following default settings:
- Host: localhost
- Port: 3306
- Username: root
- Password: password
- Database: mydb

To modify these settings, update the database configuration in `src/main.py`.

### 5. Initialize Database
```bash
cd src
python main.py
```
This will create all necessary database tables.

## Running the Application

### Start the Server
```bash
cd emr_app
./start.sh
```
Or manually:
```bash
cd emr_app
source venv/bin/activate
cd src
python main.py
```

The application will be available at http://localhost:5000

## API Endpoints

The system provides RESTful API endpoints for all modules:

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login
- `GET /api/auth/users` - List all users
- `GET /api/auth/users/<id>` - Get user details
- `PUT /api/auth/users/<id>` - Update user
- `DELETE /api/auth/users/<id>` - Deactivate user

### Patient Management
- `GET /api/patients` - List all patients
- `GET /api/patients/<id>` - Get patient details
- `POST /api/patients` - Create new patient
- `PUT /api/patients/<id>` - Update patient
- `DELETE /api/patients/<id>` - Deactivate patient
- `GET /api/patients/<id>/medical_records` - Get patient medical records

### Medical Records
- `GET /api/medical-records` - List all medical records
- `GET /api/medical-records/<id>` - Get medical record details
- `POST /api/medical-records` - Create new medical record
- `PUT /api/medical-records/<id>` - Update medical record
- `DELETE /api/medical-records/<id>` - Delete medical record

### Appointments
- `GET /api/appointments` - List all appointments
- `GET /api/appointments/<id>` - Get appointment details
- `POST /api/appointments` - Create new appointment
- `PUT /api/appointments/<id>` - Update appointment
- `DELETE /api/appointments/<id>` - Delete appointment
- `GET /api/appointments/by-patient/<id>` - Get patient appointments
- `GET /api/appointments/by-doctor/<id>` - Get doctor appointments
- `GET /api/appointments/by-date/<date>` - Get appointments by date

### Billing
- `GET /api/billing` - List all billing records
- `GET /api/billing/<id>` - Get billing record details
- `POST /api/billing` - Create new billing record
- `PUT /api/billing/<id>` - Update billing record
- `DELETE /api/billing/<id>` - Delete billing record
- `GET /api/billing/<id>/items` - Get billing items

### Insurance
- `GET /api/insurance` - List all insurance details
- `GET /api/insurance/<id>` - Get insurance detail
- `POST /api/insurance` - Create new insurance detail
- `PUT /api/insurance/<id>` - Update insurance detail
- `DELETE /api/insurance/<id>` - Deactivate insurance detail
- `GET /api/insurance/by-patient/<id>` - Get patient insurance details
- `GET /api/insurance/by-hmo/<id>` - Get HMO insurance details

### HMO Management
- `GET /api/hmo/hmo-providers` - List all HMO providers
- `GET /api/hmo/hmo-providers/<id>` - Get HMO provider details
- `POST /api/hmo/hmo-providers` - Create new HMO provider
- `PUT /api/hmo/hmo-providers/<id>` - Update HMO provider
- `DELETE /api/hmo/hmo-providers/<id>` - Deactivate HMO provider
- `GET /api/hmo/hmo-contracts` - List all HMO contracts
- `GET /api/hmo/hmo-contracts/<id>` - Get HMO contract details
- `POST /api/hmo/hmo-contracts` - Create new HMO contract
- `PUT /api/hmo/hmo-contracts/<id>` - Update HMO contract
- `DELETE /api/hmo/hmo-contracts/<id>` - Deactivate HMO contract
- `GET /api/hmo/hmo-providers/<id>/contracts` - Get provider contracts

### Claims
- `GET /api/claims` - List all claims
- `GET /api/claims/<id>` - Get claim details
- `POST /api/claims` - Create new claim
- `PUT /api/claims/<id>` - Update claim
- `DELETE /api/claims/<id>` - Delete claim
- `GET /api/claims/by-status/<status>` - Get claims by status
- `GET /api/claims/by-hmo/<id>` - Get claims by HMO

### Reconciliation
- `GET /api/reconciliation/reconciliations` - List all reconciliations
- `GET /api/reconciliation/reconciliations/<id>` - Get reconciliation details
- `POST /api/reconciliation/reconciliations` - Create new reconciliation
- `PUT /api/reconciliation/reconciliations/<id>` - Update reconciliation
- `GET /api/reconciliation/reconciliations/by-claim/<id>` - Get reconciliations by claim
- `GET /api/reconciliation/reconciliations/by-status/<status>` - Get reconciliations by status
- `POST /api/reconciliation/reconciliations/auto-reconcile` - Auto-reconcile claims
- `GET /api/reconciliation/reconciliations/report` - Get reconciliation report

### Reporting
- `GET /api/reports/financial-summary` - Financial summary report
- `GET /api/reports/hmo-performance` - HMO performance report
- `GET /api/reports/claim-aging` - Claim aging report
- `GET /api/reports/denial-analysis` - Denial analysis report
- `GET /api/reports/reconciliation-audit` - Reconciliation audit report

## HMO Reconciliation Process

The HMO reconciliation feature allows healthcare providers to:

1. **Match Billing Records with Claims**: Automatically compare hospital billing records with HMO-approved claims
2. **Identify Discrepancies**: Detect differences between services rendered and payments received
3. **Track Claim Status**: Monitor pending, partially paid, or denied claims
4. **Generate Reports**: Create financial reports and audit trails for reconciliation activities

### Reconciliation Workflow:

1. Create billing records for services rendered
2. Submit claims to HMO providers
3. Update claim status as responses are received
4. Use the auto-reconcile feature to match claims with payments
5. Review discrepancies and take appropriate actions
6. Generate reconciliation reports for financial analysis

## Security Considerations
- The system implements role-based access control
- Passwords are securely hashed
- API endpoints require authentication
- Database connections are secured

## Troubleshooting
- If the application fails to start, check database connectivity
- Ensure all dependencies are installed correctly
- Verify that the MySQL service is running
- Check log files for detailed error messages

## Support
For additional support or questions, please contact the development team.
