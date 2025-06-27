from flask import Blueprint, request, jsonify
from src.models.medical_record import MedicalRecord, db
from src.models.patient import Patient

medical_record_bp = Blueprint('medical_record', __name__)

@medical_record_bp.route('/medical_records', methods=['GET'])
def get_medical_records():
    medical_records = MedicalRecord.query.all()
    return jsonify({'medical_records': [record.to_dict() for record in medical_records]}), 200

@medical_record_bp.route('/medical_records/<int:record_id>', methods=['GET'])
def get_medical_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    return jsonify({'medical_record': record.to_dict()}), 200

@medical_record_bp.route('/medical_records', methods=['POST'])
def create_medical_record():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['patient_id', 'doctor_id', 'visit_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if patient exists
    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Create new medical record
    new_record = MedicalRecord(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        visit_date=data['visit_date'],
        chief_complaint=data.get('chief_complaint'),
        diagnosis=data.get('diagnosis'),
        treatment_plan=data.get('treatment_plan'),
        prescription=data.get('prescription'),
        notes=data.get('notes'),
        follow_up_date=data.get('follow_up_date')
    )
    
    db.session.add(new_record)
    db.session.commit()
    
    return jsonify({'message': 'Medical record created successfully', 'medical_record': new_record.to_dict()}), 201

@medical_record_bp.route('/medical_records/<int:record_id>', methods=['PUT'])
def update_medical_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    data = request.get_json()
    
    # Update medical record fields
    for key, value in data.items():
        if hasattr(record, key):
            setattr(record, key, value)
    
    db.session.commit()
    
    return jsonify({'message': 'Medical record updated successfully', 'medical_record': record.to_dict()}), 200

@medical_record_bp.route('/medical_records/<int:record_id>', methods=['DELETE'])
def delete_medical_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'message': 'Medical record deleted successfully'}), 200
