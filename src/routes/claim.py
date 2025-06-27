from flask import Blueprint, request, jsonify
from src.models.claim import Claim, db
from src.models.claim_reconciliation import ClaimReconciliation
from src.models.billing import BillingRecord
from src.models.hmo_provider import HMOProvider
from src.models.insurance import InsuranceDetail
from src.models.user import User
from datetime import datetime

claim_bp = Blueprint('claim', __name__)

@claim_bp.route('/claims', methods=['GET'])
def get_claims():
    claims = Claim.query.all()
    return jsonify({'claims': [claim.to_dict() for claim in claims]}), 200

@claim_bp.route('/claims/<int:claim_id>', methods=['GET'])
def get_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    return jsonify({'claim': claim.to_dict()}), 200

@claim_bp.route('/claims', methods=['POST'])
def create_claim():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['billing_record_id', 'hmo_id', 'insurance_detail_id', 'claim_number', 
                      'submission_date', 'service_date', 'total_amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if billing record exists
    billing_record = BillingRecord.query.get(data['billing_record_id'])
    if not billing_record:
        return jsonify({'error': 'Billing record not found'}), 404
    
    # Check if HMO provider exists
    hmo_provider = HMOProvider.query.get(data['hmo_id'])
    if not hmo_provider:
        return jsonify({'error': 'HMO provider not found'}), 404
    
    # Check if insurance detail exists
    insurance_detail = InsuranceDetail.query.get(data['insurance_detail_id'])
    if not insurance_detail:
        return jsonify({'error': 'Insurance detail not found'}), 404
    
    # Create new claim
    new_claim = Claim(
        billing_record_id=data['billing_record_id'],
        hmo_id=data['hmo_id'],
        insurance_detail_id=data['insurance_detail_id'],
        claim_number=data['claim_number'],
        submission_date=data['submission_date'],
        service_date=data['service_date'],
        total_amount=data['total_amount'],
        approved_amount=data.get('approved_amount'),
        status=data.get('status', 'pending'),
        denial_reason=data.get('denial_reason'),
        payment_date=data.get('payment_date'),
        payment_amount=data.get('payment_amount'),
        notes=data.get('notes')
    )
    
    db.session.add(new_claim)
    db.session.commit()
    
    return jsonify({'message': 'Claim created successfully', 'claim': new_claim.to_dict()}), 201

@claim_bp.route('/claims/<int:claim_id>', methods=['PUT'])
def update_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    data = request.get_json()
    
    # Update claim fields
    for key, value in data.items():
        if hasattr(claim, key):
            setattr(claim, key, value)
    
    db.session.commit()
    
    return jsonify({'message': 'Claim updated successfully', 'claim': claim.to_dict()}), 200

@claim_bp.route('/claims/<int:claim_id>', methods=['DELETE'])
def delete_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    
    # Delete associated reconciliations first
    ClaimReconciliation.query.filter_by(claim_id=claim_id).delete()
    
    # Delete the claim
    db.session.delete(claim)
    db.session.commit()
    
    return jsonify({'message': 'Claim deleted successfully'}), 200

@claim_bp.route('/claims/by-status/<status>', methods=['GET'])
def get_claims_by_status(status):
    claims = Claim.query.filter_by(status=status).all()
    return jsonify({'claims': [claim.to_dict() for claim in claims]}), 200

@claim_bp.route('/claims/by-hmo/<int:hmo_id>', methods=['GET'])
def get_claims_by_hmo(hmo_id):
    claims = Claim.query.filter_by(hmo_id=hmo_id).all()
    return jsonify({'claims': [claim.to_dict() for claim in claims]}), 200
