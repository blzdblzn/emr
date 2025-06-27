from datetime import datetime
from src.models import db

class ClaimReconciliation(db.Model):
    __tablename__ = 'claim_reconciliations'
    
    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claims.id'), nullable=False)
    reconciliation_date = db.Column(db.Date, nullable=False)
    billed_amount = db.Column(db.Numeric(10, 2), nullable=False)
    approved_amount = db.Column(db.Numeric(10, 2), nullable=False)
    paid_amount = db.Column(db.Numeric(10, 2), nullable=False)
    variance_amount = db.Column(db.Numeric(10, 2), nullable=False)
    variance_reason = db.Column(db.Text)
    action_taken = db.Column(db.String(64))  # accepted, disputed, adjusted
    resolution_status = db.Column(db.String(64), default='pending')  # pending, resolved, escalated
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='reconciliations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'claim_id': self.claim_id,
            'reconciliation_date': self.reconciliation_date.isoformat() if self.reconciliation_date else None,
            'billed_amount': float(self.billed_amount) if self.billed_amount else 0,
            'approved_amount': float(self.approved_amount) if self.approved_amount else 0,
            'paid_amount': float(self.paid_amount) if self.paid_amount else 0,
            'variance_amount': float(self.variance_amount) if self.variance_amount else 0,
            'variance_reason': self.variance_reason,
            'action_taken': self.action_taken,
            'resolution_status': self.resolution_status,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
