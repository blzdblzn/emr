from flask import Blueprint, request, jsonify
from src.models.insurance import InsuranceDetail, db
from src.models.patient import Patient
from src.models.hmo_provider import HMOProvider

insurance_bp = Blueprint('insurance', __name__)

@insurance_bp.route('/insurance', methods=['GET'])
def get_insurance_details():
    insurance_details = InsuranceDetail.query.all()
    return jsonify({'insurance_details': [detail.to_dict() for detail in insurance_details]}), 200

@insurance_bp.route('/insurance/<int:detail_id>', methods=['GET'])
def get_insurance_detail(detail_id):
    detail = InsuranceDetail.query.get_or_404(detail_id)
    return jsonify({'insurance_detail': detail.to_dict()}), 200

@insurance_bp.route('/insurance', methods=['POST'])
def create_insurance_detail():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['patient_id', 'hmo_id', 'policy_number', 'coverage_start_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if patient exists
    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Check if HMO provider exists
    hmo_provider = HMOProvider.query.get(data['hmo_id'])
    if not hmo_provider:
        return jsonify({'error': 'HMO provider not found'}), 404
    
    # Create new insurance detail
    new_detail = InsuranceDetail(
        patient_id=data['patient_id'],
        hmo_id=data['hmo_id'],
        policy_number=data['policy_number'],
        group_number=data.get('group_number'),
        coverage_start_date=data['coverage_start_date'],
        coverage_end_date=data.get('coverage_end_date'),
        primary_holder_name=data.get('primary_holder_name'),
        relationship_to_primary=data.get('relationship_to_primary'),
        coverage_type=data.get('coverage_type'),
        coverage_details=data.get('coverage_details')
    )
    
    db.session.add(new_detail)
    db.session.commit()
    
    return jsonify({'message': 'Insurance detail created successfully', 'insurance_detail': new_detail.to_dict()}), 201

@insurance_bp.route('/insurance/<int:detail_id>', methods=['PUT'])
def update_insurance_detail(detail_id):
    detail = InsuranceDetail.query.get_or_404(detail_id)
    data = request.get_json()
    
    # Update insurance detail fields
    for key, value in data.items():
        if hasattr(detail, key):
            setattr(detail, key, value)
    
    db.session.commit()
    
    return jsonify({'message': 'Insurance detail updated successfully', 'insurance_detail': detail.to_dict()}), 200

@insurance_bp.route('/insurance/<int:detail_id>', methods=['DELETE'])
def delete_insurance_detail(detail_id):
    detail = InsuranceDetail.query.get_or_404(detail_id)
    
    # Soft delete by setting is_active to False
    detail.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Insurance detail deactivated successfully'}), 200

@insurance_bp.route('/insurance/by-patient/<int:patient_id>', methods=['GET'])
def get_patient_insurance_details(patient_id):
    # Check if patient exists
    patient = Patient.query.get_or_404(patient_id)
    
    # Get all insurance details for the patient
    details = InsuranceDetail.query.filter_by(patient_id=patient_id).all()
    
    return jsonify({'insurance_details': [detail.to_dict() for detail in details]}), 200

@insurance_bp.route('/insurance/by-hmo/<int:hmo_id>', methods=['GET'])
def get_hmo_insurance_details(hmo_id):
    # Check if HMO provider exists
    hmo_provider = HMOProvider.query.get_or_404(hmo_id)
    
    # Get all insurance details for the HMO provider
    details = InsuranceDetail.query.filter_by(hmo_id=hmo_id).all()
    
    return jsonify({'insurance_details': [detail.to_dict() for detail in details]}), 200
