from flask import Blueprint, request, jsonify
from src.models.patient import Patient, db
from src.models.medical_record import MedicalRecord

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify({'patients': [patient.to_dict() for patient in patients]}), 200

@patient_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({'patient': patient.to_dict()}), 200

@patient_bp.route('/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['first_name', 'last_name', 'date_of_birth', 'gender']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new patient
    new_patient = Patient(
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=data['date_of_birth'],
        gender=data['gender'],
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        phone=data.get('phone'),
        email=data.get('email'),
        emergency_contact_name=data.get('emergency_contact_name'),
        emergency_contact_phone=data.get('emergency_contact_phone'),
        blood_type=data.get('blood_type'),
        allergies=data.get('allergies')
    )
    
    db.session.add(new_patient)
    db.session.commit()
    
    return jsonify({'message': 'Patient created successfully', 'patient': new_patient.to_dict()}), 201

@patient_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()
    
    # Update patient fields
    for key, value in data.items():
        if hasattr(patient, key):
            setattr(patient, key, value)
    
    db.session.commit()
    
    return jsonify({'message': 'Patient updated successfully', 'patient': patient.to_dict()}), 200

@patient_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Soft delete by setting is_active to False
    patient.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Patient deactivated successfully'}), 200

@patient_bp.route('/patients/<int:patient_id>/medical_records', methods=['GET'])
def get_patient_medical_records(patient_id):
    # Check if patient exists
    patient = Patient.query.get_or_404(patient_id)
    
    # Get all medical records for the patient
    medical_records = MedicalRecord.query.filter_by(patient_id=patient_id).all()
    
    return jsonify({'medical_records': [record.to_dict() for record in medical_records]}), 200
