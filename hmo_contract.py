from datetime import datetime
from src.models import db

class HMOContract(db.Model):
    __tablename__ = 'hmo_contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    hmo_id = db.Column(db.Integer, db.ForeignKey('hmo_providers.id'), nullable=False)
    contract_number = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    contract_terms = db.Column(db.Text)
    payment_terms = db.Column(db.Text)
    service_coverage = db.Column(db.Text)
    reimbursement_rates = db.Column(db.Text)
    claim_submission_guidelines = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'hmo_id': self.hmo_id,
            'contract_number': self.contract_number,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'contract_terms': self.contract_terms,
            'payment_terms': self.payment_terms,
            'service_coverage': self.service_coverage,
            'reimbursement_rates': self.reimbursement_rates,
            'claim_submission_guidelines': self.claim_submission_guidelines,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
