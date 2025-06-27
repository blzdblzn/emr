from flask import Blueprint, request, jsonify, render_template
from src.models.hmo_provider import HMOProvider, db
from src.models.hmo_contract import HMOContract

hmo_bp = Blueprint('hmo', __name__)

@hmo_bp.route('/hmo-providers', methods=['GET'])
def get_hmo_providers():
    hmo_providers = HMOProvider.query.all()
    return jsonify({'hmo_providers': [provider.to_dict() for provider in hmo_providers]}), 200

@hmo_bp.route('/hmo-providers/<int:provider_id>', methods=['GET'])
def get_hmo_provider(provider_id):
    provider = HMOProvider.query.get_or_404(provider_id)
    return jsonify({'hmo_provider': provider.to_dict()}), 200

@hmo_bp.route('/hmo-providers', methods=['POST'])
def create_hmo_provider():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new HMO provider
    new_provider = HMOProvider(
        name=data['name'],
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        phone=data.get('phone'),
        email=data.get('email'),
        website=data.get('website'),
        contact_person=data.get('contact_person'),
        contact_phone=data.get('contact_phone'),
        contact_email=data.get('contact_email')
    )
    
    db.session.add(new_provider)
    db.session.commit()
    
    return jsonify({'message': 'HMO provider created successfully', 'hmo_provider': new_provider.to_dict()}), 201

@hmo_bp.route('/hmo-providers/<int:provider_id>', methods=['PUT'])
def update_hmo_provider(provider_id):
    provider = HMOProvider.query.get_or_404(provider_id)
    data = request.get_json()
    
    # Update provider fields
    for key, value in data.items():
        if hasattr(provider, key):
            setattr(provider, key, value)
    
    db.session.commit()
    
    return jsonify({'message': 'HMO provider updated successfully', 'hmo_provider': provider.to_dict()}), 200

@hmo_bp.route('/hmo-providers/<int:provider_id>', methods=['DELETE'])
def delete_hmo_provider(provider_id):
    provider = HMOProvider.query.get_or_404(provider_id)
    
    # Soft delete by setting is_active to False
    provider.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'HMO provider deactivated successfully'}), 200

@hmo_bp.route('/hmo-contracts', methods=['GET'])
def get_hmo_contracts():
    contracts = HMOContract.query.all()
    return jsonify({'hmo_contracts': [contract.to_dict() for contract in contracts]}), 200

@hmo_bp.route('/hmo-contracts/<int:contract_id>', methods=['GET'])
def get_hmo_contract(contract_id):
    contract = HMOContract.query.get_or_404(contract_id)
    return jsonify({'hmo_contract': contract.to_dict()}), 200

@hmo_bp.route('/hmo-contracts', methods=['POST'])
def create_hmo_contract():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['hmo_id', 'contract_number', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if HMO provider exists
    hmo_provider = HMOProvider.query.get(data['hmo_id'])
    if not hmo_provider:
        return jsonify({'error': 'HMO provider not found'}), 404
    
    # Create new HMO contract
    new_contract = HMOContract(
        hmo_id=data['hmo_id'],
        contract_number=data['contract_number'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        contract_terms=data.get('contract_terms'),
        payment_terms=data.get('payment_terms'),
        service_coverage=data.get('service_coverage'),
        reimbursement_rates=data.get('reimbursement_rates'),
        claim_submission_guidelines=data.get('claim_submission_guidelines')
    )
    
    db.session.add(new_contract)
    db.session.commit()
    
    return jsonify({'message': 'HMO contract created successfully', 'hmo_contract': new_contract.to_dict()}), 201

@hmo_bp.route('/hmo-contracts/<int:contract_id>', methods=['PUT'])
def update_hmo_contract(contract_id):
    contract = HMOContract.query.get_or_404(contract_id)
    data = request.get_json()
    
    # Update contract fields
    for key, value in data.items():
        if hasattr(contract, key):
            setattr(contract, key, value)
    
    db.session.commit()
    
    return jsonify({'message': 'HMO contract updated successfully', 'hmo_contract': contract.to_dict()}), 200

@hmo_bp.route('/hmo-contracts/<int:contract_id>', methods=['DELETE'])
def delete_hmo_contract(contract_id):
    contract = HMOContract.query.get_or_404(contract_id)
    
    # Soft delete by setting is_active to False
    contract.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'HMO contract deactivated successfully'}), 200

@hmo_bp.route('/hmo-providers/<int:provider_id>/contracts', methods=['GET'])
def get_provider_contracts(provider_id):
    # Check if HMO provider exists
    provider = HMOProvider.query.get_or_404(provider_id)
    
    # Get all contracts for the provider
    contracts = HMOContract.query.filter_by(hmo_id=provider_id).all()
    
    return jsonify({'hmo_contracts': [contract.to_dict() for contract in contracts]}), 200
