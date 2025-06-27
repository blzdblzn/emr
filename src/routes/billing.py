from flask import Blueprint, request, jsonify
from src.models.billing import BillingRecord, db
from src.models.billing_item import BillingItem
from src.models.patient import Patient

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/billing', methods=['GET'])
def get_billing_records():
    billing_records = BillingRecord.query.all()
    return jsonify({'billing_records': [record.to_dict() for record in billing_records]}), 200

@billing_bp.route('/billing/<int:record_id>', methods=['GET'])
def get_billing_record(record_id):
    record = BillingRecord.query.get_or_404(record_id)
    return jsonify({'billing_record': record.to_dict()}), 200

@billing_bp.route('/billing', methods=['POST'])
def create_billing_record():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['patient_id', 'invoice_number', 'invoice_date', 'due_date', 'total_amount', 'balance']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if patient exists
    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Create new billing record
    new_record = BillingRecord(
        patient_id=data['patient_id'],
        medical_record_id=data.get('medical_record_id'),
        invoice_number=data['invoice_number'],
        invoice_date=data['invoice_date'],
        due_date=data['due_date'],
        total_amount=data['total_amount'],
        paid_amount=data.get('paid_amount', 0),
        balance=data['balance'],
        status=data.get('status', 'pending'),
        payment_method=data.get('payment_method'),
        payment_date=data.get('payment_date'),
        notes=data.get('notes')
    )
    
    db.session.add(new_record)
    db.session.commit()
    
    # Add billing items if provided
    if 'billing_items' in data and isinstance(data['billing_items'], list):
        for item_data in data['billing_items']:
            item = BillingItem(
                billing_record_id=new_record.id,
                service_code=item_data['service_code'],
                service_description=item_data['service_description'],
                quantity=item_data.get('quantity', 1),
                unit_price=item_data['unit_price'],
                total_price=item_data['total_price']
            )
            db.session.add(item)
        
        db.session.commit()
    
    return jsonify({'message': 'Billing record created successfully', 'billing_record': new_record.to_dict()}), 201

@billing_bp.route('/billing/<int:record_id>', methods=['PUT'])
def update_billing_record(record_id):
    record = BillingRecord.query.get_or_404(record_id)
    data = request.get_json()
    
    # Update billing record fields
    for key, value in data.items():
        if hasattr(record, key) and key != 'billing_items':
            setattr(record, key, value)
    
    # Update billing items if provided
    if 'billing_items' in data and isinstance(data['billing_items'], list):
        # Remove existing items
        BillingItem.query.filter_by(billing_record_id=record_id).delete()
        
        # Add new items
        for item_data in data['billing_items']:
            item = BillingItem(
                billing_record_id=record.id,
                service_code=item_data['service_code'],
                service_description=item_data['service_description'],
                quantity=item_data.get('quantity', 1),
                unit_price=item_data['unit_price'],
                total_price=item_data['total_price']
            )
            db.session.add(item)
    
    db.session.commit()
    
    return jsonify({'message': 'Billing record updated successfully', 'billing_record': record.to_dict()}), 200

@billing_bp.route('/billing/<int:record_id>', methods=['DELETE'])
def delete_billing_record(record_id):
    record = BillingRecord.query.get_or_404(record_id)
    
    # Delete associated billing items first
    BillingItem.query.filter_by(billing_record_id=record_id).delete()
    
    # Delete the billing record
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'message': 'Billing record deleted successfully'}), 200

@billing_bp.route('/billing/<int:record_id>/items', methods=['GET'])
def get_billing_items(record_id):
    # Check if billing record exists
    record = BillingRecord.query.get_or_404(record_id)
    
    # Get all billing items for the record
    items = BillingItem.query.filter_by(billing_record_id=record_id).all()
    
    return jsonify({'billing_items': [item.to_dict() for item in items]}), 200
