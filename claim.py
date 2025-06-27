from datetime import datetime
from src.models import db

class Claim(db.Model):
    __tablename__ = 'claims'
    
    id = db.Column(db.Integer, primary_key=True)
    billing_record_id = db.Column(db.Integer, db.ForeignKey('billing_records.id'), nullable=False)
    hmo_id = db.Column(db.Integer, db.ForeignKey('hmo_providers.id'), nullable=False)
    insurance_detail_id = db.Column(db.Integer, db.ForeignKey('insurance_details.id'), nullable=False)
    claim_number = db.Column(db.String(64), unique=True, nullable=False)
    submission_date = db.Column(db.Date, nullable=False)
    service_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    approved_amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='pending')  # pending, approved, partially_approved, denied
    denial_reason = db.Column(db.Text)
    payment_date = db.Column(db.Date)
    payment_amount = db.Column(db.Numeric(10, 2))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    insurance_detail = db.relationship('InsuranceDetail', backref='claims')
    reconciliations = db.relationship('ClaimReconciliation', backref='claim', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'billing_record_id': self.billing_record_id,
            'hmo_id': self.hmo_id,
            'insurance_detail_id': self.insurance_detail_id,
            'claim_number': self.claim_number,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'service_date': self.service_date.isoformat() if self.service_date else None,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'approved_amount': float(self.approved_amount) if self.approved_amount else 0,
            'status': self.status,
            'denial_reason': self.denial_reason,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_amount': float(self.payment_amount) if self.payment_amount else 0,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
