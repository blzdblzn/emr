from flask import Blueprint, request, jsonify
from src.models.claim_reconciliation import ClaimReconciliation, db
from src.models.claim import Claim
from src.models.billing import BillingRecord
from src.models.user import User
from datetime import datetime

reconciliation_bp = Blueprint('reconciliation', __name__)

@reconciliation_bp.route('/reconciliations', methods=['GET'])
def get_reconciliations():
    reconciliations = ClaimReconciliation.query.all()
    return jsonify({'reconciliations': [rec.to_dict() for rec in reconciliations]}), 200

@reconciliation_bp.route('/reconciliations/<int:reconciliation_id>', methods=['GET'])
def get_reconciliation(reconciliation_id):
    reconciliation = ClaimReconciliation.query.get_or_404(reconciliation_id)
    return jsonify({'reconciliation': reconciliation.to_dict()}), 200

@reconciliation_bp.route('/reconciliations', methods=['POST'])
def create_reconciliation():
    data = request.get_json()
    
    # Check if required fields are present
    required_fields = ['claim_id', 'reconciliation_date', 'billed_amount', 
                      'approved_amount', 'paid_amount', 'variance_amount', 'created_by']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if claim exists
    claim = Claim.query.get(data['claim_id'])
    if not claim:
        return jsonify({'error': 'Claim not found'}), 404
    
    # Check if user exists
    user = User.query.get(data['created_by'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create new reconciliation
    new_reconciliation = ClaimReconciliation(
        claim_id=data['claim_id'],
        reconciliation_date=data['reconciliation_date'],
        billed_amount=data['billed_amount'],
        approved_amount=data['approved_amount'],
        paid_amount=data['paid_amount'],
        variance_amount=data['variance_amount'],
        variance_reason=data.get('variance_reason'),
        action_taken=data.get('action_taken'),
        resolution_status=data.get('resolution_status', 'pending'),
        notes=data.get('notes'),
        created_by=data['created_by']
    )
    
    db.session.add(new_reconciliation)
    db.session.commit()
    
    return jsonify({'message': 'Reconciliation created successfully', 'reconciliation': new_reconciliation.to_dict()}), 201

@reconciliation_bp.route('/reconciliations/<int:reconciliation_id>', methods=['PUT'])
def update_reconciliation(reconciliation_id):
    reconciliation = ClaimReconciliation.query.get_or_404(reconciliation_id)
    data = request.get_json()
    
    # Update reconciliation fields
    for key, value in data.items():
        if hasattr(reconciliation, key):
            setattr(reconciliation, key, value)
    
    db.session.commit()
    
    return jsonify({'message': 'Reconciliation updated successfully', 'reconciliation': reconciliation.to_dict()}), 200

@reconciliation_bp.route('/reconciliations/by-claim/<int:claim_id>', methods=['GET'])
def get_reconciliations_by_claim(claim_id):
    reconciliations = ClaimReconciliation.query.filter_by(claim_id=claim_id).all()
    return jsonify({'reconciliations': [rec.to_dict() for rec in reconciliations]}), 200

@reconciliation_bp.route('/reconciliations/by-status/<status>', methods=['GET'])
def get_reconciliations_by_status(status):
    reconciliations = ClaimReconciliation.query.filter_by(resolution_status=status).all()
    return jsonify({'reconciliations': [rec.to_dict() for rec in reconciliations]}), 200

@reconciliation_bp.route('/reconciliations/auto-reconcile', methods=['POST'])
def auto_reconcile_claims():
    """
    Automatically reconcile claims by comparing billed amounts with approved/paid amounts
    """
    data = request.get_json()
    
    if 'user_id' not in data:
        return jsonify({'error': 'User ID is required'}), 400
    
    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get claims that need reconciliation (approved or partially approved but not reconciled)
    claims_to_reconcile = Claim.query.filter(
        Claim.status.in_(['approved', 'partially_approved']),
        ~Claim.id.in_(
            db.session.query(ClaimReconciliation.claim_id)
        )
    ).all()
    
    reconciliations_created = []
    
    for claim in claims_to_reconcile:
        # Calculate variance
        billed_amount = float(claim.total_amount)
        approved_amount = float(claim.approved_amount) if claim.approved_amount else 0
        paid_amount = float(claim.payment_amount) if claim.payment_amount else 0
        variance_amount = billed_amount - paid_amount
        
        # Determine variance reason and action
        if variance_amount == 0:
            variance_reason = "No variance"
            action_taken = "accepted"
            resolution_status = "resolved"
        elif variance_amount > 0:
            if approved_amount < billed_amount:
                variance_reason = "Partial approval by HMO"
                action_taken = "accepted"
                resolution_status = "resolved"
            else:
                variance_reason = "Approved but underpaid"
                action_taken = "disputed"
                resolution_status = "pending"
        else:
            variance_reason = "Overpayment"
            action_taken = "adjusted"
            resolution_status = "pending"
        
        # Create reconciliation record
        new_reconciliation = ClaimReconciliation(
            claim_id=claim.id,
            reconciliation_date=datetime.utcnow().date(),
            billed_amount=billed_amount,
            approved_amount=approved_amount,
            paid_amount=paid_amount,
            variance_amount=variance_amount,
            variance_reason=variance_reason,
            action_taken=action_taken,
            resolution_status=resolution_status,
            notes=f"Auto-reconciled on {datetime.utcnow()}",
            created_by=data['user_id']
        )
        
        db.session.add(new_reconciliation)
        reconciliations_created.append(new_reconciliation)
    
    db.session.commit()
    
    return jsonify({
        'message': f'{len(reconciliations_created)} claims auto-reconciled successfully',
        'reconciliations': [rec.to_dict() for rec in reconciliations_created]
    }), 200

@reconciliation_bp.route('/reconciliations/report', methods=['GET'])
def get_reconciliation_report():
    """
    Generate a reconciliation report with summary statistics
    """
    # Get all reconciliations
    reconciliations = ClaimReconciliation.query.all()
    
    # Calculate summary statistics
    total_count = len(reconciliations)
    total_billed = sum(float(rec.billed_amount) for rec in reconciliations)
    total_approved = sum(float(rec.approved_amount) for rec in reconciliations)
    total_paid = sum(float(rec.paid_amount) for rec in reconciliations)
    total_variance = sum(float(rec.variance_amount) for rec in reconciliations)
    
    # Count by status
    status_counts = {}
    for rec in reconciliations:
        status = rec.resolution_status
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1
    
    # Count by action
    action_counts = {}
    for rec in reconciliations:
        action = rec.action_taken
        if action in action_counts:
            action_counts[action] += 1
        else:
            action_counts[action] = 1
    
    return jsonify({
        'summary': {
            'total_count': total_count,
            'total_billed': total_billed,
            'total_approved': total_approved,
            'total_paid': total_paid,
            'total_variance': total_variance,
            'average_variance': total_variance / total_count if total_count > 0 else 0,
            'collection_rate': (total_paid / total_billed * 100) if total_billed > 0 else 0
        },
        'by_status': status_counts,
        'by_action': action_counts
    }), 200
