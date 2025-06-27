from datetime import datetime
from src.models import db

class BillingRecord(db.Model):
    __tablename__ = 'billing_records'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_records.id'))
    invoice_number = db.Column(db.String(64), unique=True, nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    paid_amount = db.Column(db.Numeric(10, 2), default=0)
    balance = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, partial, paid, overdue, cancelled
    payment_method = db.Column(db.String(64))
    payment_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medical_record = db.relationship('MedicalRecord', backref='billing_records')
    billing_items = db.relationship('BillingItem', backref='billing_record', lazy=True)
    claims = db.relationship('Claim', backref='billing_record', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'medical_record_id': self.medical_record_id,
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date.isoformat() if self.invoice_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'paid_amount': float(self.paid_amount) if self.paid_amount else 0,
            'balance': float(self.balance) if self.balance else 0,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
