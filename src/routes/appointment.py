from flask import Blueprint, request, jsonify, render_template
from src.models.appointment import Appointment, db
from src.models.patient import Patient
from src.models.user import User
from datetime import datetime

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify({'appointments': [appointment.to_dict() for appointment in appointments]}), 200

@appointment_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify({'appointment': appointment.to_dict()}), 200

@appointment_bp.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['patient_id', 'doctor_id', 'appointment_date', 'reason']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if patient exists
    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Check if doctor exists
    doctor = User.query.get(data['doctor_id'])
    if not doctor or doctor.role != 'doctor':
        return jsonify({'error': 'Doctor not found'}), 404
    
    # Create new appointment
    new_appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        appointment_date=data['appointment_date'],
        reason=data['reason'],
        status=data.get('status', 'scheduled'),
        notes=data.get('notes')
    )
    
    db.session.add(new_appointment)
    db.session.commit()
    
    return jsonify({'message': 'Appointment created successfully', 'appointment': new_appointment.to_dict()}), 201

@appointment_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json()
    
    # Update appointment fields
    for key, value in data.items():
        if hasattr(appointment, key):
            setattr(appointment, key, value)
    
    db.session.commit()
    
    return jsonify({'message': 'Appointment updated successfully', 'appointment': appointment.to_dict()}), 200

@appointment_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    db.session.delete(appointment)
    db.session.commit()
    
    return jsonify({'message': 'Appointment deleted successfully'}), 200

@appointment_bp.route('/appointments/by-patient/<int:patient_id>', methods=['GET'])
def get_patient_appointments(patient_id):
    # Check if patient exists
    patient = Patient.query.get_or_404(patient_id)
    
    # Get all appointments for the patient
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    
    return jsonify({'appointments': [appointment.to_dict() for appointment in appointments]}), 200

@appointment_bp.route('/appointments/by-doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_appointments(doctor_id):
    # Check if doctor exists
    doctor = User.query.get_or_404(doctor_id)
    
    # Get all appointments for the doctor
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    
    return jsonify({'appointments': [appointment.to_dict() for appointment in appointments]}), 200

@appointment_bp.route('/appointments/by-date/<date>', methods=['GET'])
def get_appointments_by_date(date):
    try:
        # Parse date string to date object
        appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
        
        # Get all appointments for the date
        appointments = Appointment.query.filter(
            db.func.date(Appointment.appointment_date) == appointment_date
        ).all()
        
        return jsonify({'appointments': [appointment.to_dict() for appointment in appointments]}), 200
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
