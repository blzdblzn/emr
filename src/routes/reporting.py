from flask import Blueprint, request, jsonify
from src.models.claim import Claim, db
from src.models.claim_reconciliation import ClaimReconciliation
from src.models.billing import BillingRecord
from src.models.billing_item import BillingItem
from src.models.hmo_provider import HMOProvider
from src.models.patient import Patient
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import json

reporting_bp = Blueprint('reporting', __name__)

@reporting_bp.route('/reports/financial-summary', methods=['GET'])
def financial_summary_report():
    """
    Generate a financial summary report with revenue, outstanding claims, and collection metrics
    """
    # Get query parameters for date range
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Default to last 30 days if not specified
    if not end_date_str:
        end_date = datetime.utcnow().date()
    else:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
    if not start_date_str:
        start_date = end_date - timedelta(days=30)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    # Total billing amount
    total_billed = db.session.query(func.sum(BillingRecord.total_amount)).filter(
        BillingRecord.invoice_date >= start_date,
        BillingRecord.invoice_date <= end_date
    ).scalar() or 0
    
    # Total payments received
    total_paid = db.session.query(func.sum(BillingRecord.paid_amount)).filter(
        BillingRecord.invoice_date >= start_date,
        BillingRecord.invoice_date <= end_date
    ).scalar() or 0
    
    # Outstanding balance
    outstanding_balance = db.session.query(func.sum(BillingRecord.balance)).filter(
        BillingRecord.invoice_date >= start_date,
        BillingRecord.invoice_date <= end_date
    ).scalar() or 0
    
    # Claims statistics
    total_claims = Claim.query.filter(
        Claim.submission_date >= start_date,
        Claim.submission_date <= end_date
    ).count()
    
    approved_claims = Claim.query.filter(
        Claim.submission_date >= start_date,
        Claim.submission_date <= end_date,
        Claim.status == 'approved'
    ).count()
    
    pending_claims = Claim.query.filter(
        Claim.submission_date >= start_date,
        Claim.submission_date <= end_date,
        Claim.status == 'pending'
    ).count()
    
    denied_claims = Claim.query.filter(
        Claim.submission_date >= start_date,
        Claim.submission_date <= end_date,
        Claim.status == 'denied'
    ).count()
    
    # Claims amount statistics
    total_claim_amount = db.session.query(func.sum(Claim.total_amount)).filter(
        Claim.submission_date >= start_date,
        Claim.submission_date <= end_date
    ).scalar() or 0
    
    approved_claim_amount = db.session.query(func.sum(Claim.approved_amount)).filter(
        Claim.submission_date >= start_date,
        Claim.submission_date <= end_date,
        Claim.status.in_(['approved', 'partially_approved'])
    ).scalar() or 0
    
    # Collection rate
    collection_rate = (total_paid / total_billed * 100) if total_billed > 0 else 0
    
    # Claim approval rate
    claim_approval_rate = (approved_claims / total_claims * 100) if total_claims > 0 else 0
    
    return jsonify({
        'date_range': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'billing_summary': {
            'total_billed': float(total_billed),
            'total_paid': float(total_paid),
            'outstanding_balance': float(outstanding_balance),
            'collection_rate': float(collection_rate)
        },
        'claims_summary': {
            'total_claims': total_claims,
            'approved_claims': approved_claims,
            'pending_claims': pending_claims,
            'denied_claims': denied_claims,
            'approval_rate': float(claim_approval_rate),
            'total_claim_amount': float(total_claim_amount),
            'approved_claim_amount': float(approved_claim_amount)
        }
    }), 200

@reporting_bp.route('/reports/hmo-performance', methods=['GET'])
def hmo_performance_report():
    """
    Generate a report on HMO performance metrics
    """
    # Get query parameters for date range
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Default to last 30 days if not specified
    if not end_date_str:
        end_date = datetime.utcnow().date()
    else:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
    if not start_date_str:
        start_date = end_date - timedelta(days=30)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    # Get all HMO providers
    hmo_providers = HMOProvider.query.all()
    
    hmo_performance = []
    
    for hmo in hmo_providers:
        # Total claims for this HMO
        total_claims = Claim.query.filter(
            Claim.submission_date >= start_date,
            Claim.submission_date <= end_date,
            Claim.hmo_id == hmo.id
        ).count()
        
        if total_claims == 0:
            continue  # Skip HMOs with no claims in this period
        
        # Approved claims
        approved_claims = Claim.query.filter(
            Claim.submission_date >= start_date,
            Claim.submission_date <= end_date,
            Claim.hmo_id == hmo.id,
            Claim.status == 'approved'
        ).count()
        
        # Partially approved claims
        partially_approved_claims = Claim.query.filter(
            Claim.submission_date >= start_date,
            Claim.submission_date <= end_date,
            Claim.hmo_id == hmo.id,
            Claim.status == 'partially_approved'
        ).count()
        
        # Denied claims
        denied_claims = Claim.query.filter(
            Claim.submission_date >= start_date,
            Claim.submission_date <= end_date,
            Claim.hmo_id == hmo.id,
            Claim.status == 'denied'
        ).count()
        
        # Pending claims
        pending_claims = Claim.query.filter(
            Claim.submission_date >= start_date,
            Claim.submission_date <= end_date,
            Claim.hmo_id == hmo.id,
            Claim.status == 'pending'
        ).count()
        
        # Total amount billed to this HMO
        total_billed = db.session.query(func.sum(Claim.total_amount)).filter(
            Claim.submission_date >= start_date,
            Claim.submission_date <= end_date,
            Claim.hmo_id == hmo.id
        ).scalar() or 0
        
        # Total amount approved by this HMO
        total_approved = db.session.query(func.sum(Claim.approved_amount)).filter(
            Claim.submission_date >= start_date,
            Claim.submission_date <= end_date,
            Claim.hmo_id == hmo.id,
            Claim.status.in_(['approved', 'partially_approved'])
        ).scalar() or 0
        
        # Total amount paid by this HMO
        total_paid = db.session.query(func.sum(Claim.payment_amount)).filter(
            Claim.submission_date >= start_date,
            Claim.submission_date <= end_date,
            Claim.hmo_id == hmo.id,
            Claim.payment_amount.isnot(None)
        ).scalar() or 0
        
        # Average processing time (days between submission and payment)
        processing_time_query = db.session.query(
            func.avg(func.julianday(Claim.payment_date) - func.julianday(Claim.submission_date))
        ).filter(
            Claim.submission_date >= start_date,
            Claim.submission_date <= end_date,
            Claim.hmo_id == hmo.id,
            Claim.payment_date.isnot(None)
        ).scalar()
        
        avg_processing_time = float(processing_time_query) if processing_time_query else None
        
        # Calculate approval and payment rates
        approval_rate = ((approved_claims + partially_approved_claims) / total_claims * 100) if total_claims > 0 else 0
        payment_rate = (total_paid / total_billed * 100) if total_billed > 0 else 0
        
        hmo_performance.append({
            'hmo_id': hmo.id,
            'hmo_name': hmo.name,
            'total_claims': total_claims,
            'approved_claims': approved_claims,
            'partially_approved_claims': partially_approved_claims,
            'denied_claims': denied_claims,
            'pending_claims': pending_claims,
            'approval_rate': float(approval_rate),
            'total_billed': float(total_billed),
            'total_approved': float(total_approved),
            'total_paid': float(total_paid),
            'payment_rate': float(payment_rate),
            'avg_processing_time_days': avg_processing_time
        })
    
    # Sort by approval rate (descending)
    hmo_performance.sort(key=lambda x: x['approval_rate'], reverse=True)
    
    return jsonify({
        'date_range': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'hmo_performance': hmo_performance
    }), 200

@reporting_bp.route('/reports/claim-aging', methods=['GET'])
def claim_aging_report():
    """
    Generate a report on aging claims by time periods
    """
    today = datetime.utcnow().date()
    
    # Define aging buckets (in days)
    buckets = {
        '0-30': (0, 30),
        '31-60': (31, 60),
        '61-90': (61, 90),
        '91-120': (91, 120),
        'over_120': (121, 9999)
    }
    
    aging_report = {}
    
    for bucket_name, (min_days, max_days) in buckets.items():
        min_date = today - timedelta(days=max_days)
        max_date = today - timedelta(days=min_days) if min_days > 0 else today
        
        # Count claims in this bucket
        claims_count = Claim.query.filter(
            Claim.submission_date >= min_date,
            Claim.submission_date <= max_date,
            Claim.status.in_(['pending', 'partially_approved'])
        ).count()
        
        # Sum claim amounts in this bucket
        claims_amount = db.session.query(func.sum(Claim.total_amount)).filter(
            Claim.submission_date >= min_date,
            Claim.submission_date <= max_date,
            Claim.status.in_(['pending', 'partially_approved'])
        ).scalar() or 0
        
        aging_report[bucket_name] = {
            'claims_count': claims_count,
            'claims_amount': float(claims_amount)
        }
    
    # Get total pending claims
    total_pending_claims = Claim.query.filter(
        Claim.status.in_(['pending', 'partially_approved'])
    ).count()
    
    total_pending_amount = db.session.query(func.sum(Claim.total_amount)).filter(
        Claim.status.in_(['pending', 'partially_approved'])
    ).scalar() or 0
    
    return jsonify({
        'report_date': today.isoformat(),
        'total_pending_claims': total_pending_claims,
        'total_pending_amount': float(total_pending_amount),
        'aging_buckets': aging_report
    }), 200

@reporting_bp.route('/reports/denial-analysis', methods=['GET'])
def denial_analysis_report():
    """
    Generate a report analyzing claim denials and their reasons
    """
    # Get query parameters for date range
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Default to last 90 days if not specified
    if not end_date_str:
        end_date = datetime.utcnow().date()
    else:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
    if not start_date_str:
        start_date = end_date - timedelta(days=90)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    # Get all denied claims in the period
    denied_claims = Claim.query.filter(
        Claim.submission_date >= start_date,
        Claim.submission_date <= end_date,
        Claim.status == 'denied'
    ).all()
    
    # Analyze denial reasons
    denial_reasons = {}
    
    for claim in denied_claims:
        reason = claim.denial_reason or 'Unspecified'
        
        if reason in denial_reasons:
            denial_reasons[reason]['count'] += 1
            denial_reasons[reason]['amount'] += float(claim.total_amount)
        else:
            denial_reasons[reason] = {
                'count': 1,
                'amount': float(claim.total_amount)
            }
    
    # Convert to list and sort by count
    denial_reasons_list = [
        {'reason': reason, 'count': data['count'], 'amount': data['amount']}
        for reason, data in denial_reasons.items()
    ]
    denial_reasons_list.sort(key=lambda x: x['count'], reverse=True)
    
    # Get denial rate
    total_claims = Claim.query.filter(
        Claim.submission_date >= start_date,
        Claim.submission_date <= end_date
    ).count()
    
    denial_rate = (len(denied_claims) / total_claims * 100) if total_claims > 0 else 0
    
    # Get denials by HMO
    denials_by_hmo = {}
    
    for claim in denied_claims:
        hmo_id = claim.hmo_id
        hmo = HMOProvider.query.get(hmo_id)
        hmo_name = hmo.name if hmo else f"HMO ID {hmo_id}"
        
        if hmo_name in denials_by_hmo:
            denials_by_hmo[hmo_name]['count'] += 1
            denials_by_hmo[hmo_name]['amount'] += float(claim.total_amount)
        else:
            denials_by_hmo[hmo_name] = {
                'count': 1,
                'amount': float(claim.total_amount)
            }
    
    # Convert to list and sort by count
    denials_by_hmo_list = [
        {'hmo': hmo, 'count': data['count'], 'amount': data['amount']}
        for hmo, data in denials_by_hmo.items()
    ]
    denials_by_hmo_list.sort(key=lambda x: x['count'], reverse=True)
    
    return jsonify({
        'date_range': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'total_claims': total_claims,
        'denied_claims': len(denied_claims),
        'denial_rate': float(denial_rate),
        'denial_reasons': denial_reasons_list,
        'denials_by_hmo': denials_by_hmo_list
    }), 200

@reporting_bp.route('/reports/reconciliation-audit', methods=['GET'])
def reconciliation_audit_report():
    """
    Generate an audit report for claim reconciliations
    """
    # Get query parameters for date range
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Default to last 30 days if not specified
    if not end_date_str:
        end_date = datetime.utcnow().date()
    else:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
    if not start_date_str:
        start_date = end_date - timedelta(days=30)
    else:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    
    # Get all reconciliations in the period
    reconciliations = ClaimReconciliation.query.filter(
        ClaimReconciliation.reconciliation_date >= start_date,
        ClaimReconciliation.reconciliation_date <= end_date
    ).all()
    
    # Prepare detailed audit data
    audit_entries = []
    
    for rec in reconciliations:
        claim = Claim.query.get(rec.claim_id)
        if not claim:
            continue
            
        billing_record = BillingRecord.query.get(claim.billing_record_id) if claim else None
        hmo = HMOProvider.query.get(claim.hmo_id) if claim else None
        
        audit_entries.append({
            'reconciliation_id': rec.id,
            'reconciliation_date': rec.reconciliation_date.isoformat() if rec.reconciliation_date else None,
            'claim_id': rec.claim_id,
            'claim_number': claim.claim_number if claim else None,
            'hmo_name': hmo.name if hmo else None,
            'invoice_number': billing_record.invoice_number if billing_record else None,
            'billed_amount': float(rec.billed_amount),
            'approved_amount': float(rec.approved_amount),
            'paid_amount': float(rec.paid_amount),
            'variance_amount': float(rec.variance_amount),
            'variance_reason': rec.variance_reason,
            'action_taken': rec.action_taken,
            'resolution_status': rec.resolution_status
        })
    
    # Summary statistics
    total_reconciliations = len(reconciliations)
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
        'date_range': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        },
        'summary': {
            'total_reconciliations': total_reconciliations,
            'total_billed': float(total_billed),
            'total_approved': float(total_approved),
            'total_paid': float(total_paid),
            'total_variance': float(total_variance),
            'average_variance': float(total_variance / total_reconciliations) if total_reconciliations > 0 else 0,
            'collection_rate': float(total_paid / total_billed * 100) if total_billed > 0 else 0
        },
        'by_status': status_counts,
        'by_action': action_counts,
        'audit_entries': audit_entries
    }), 200
