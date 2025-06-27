from datetime import datetime
from src.models import db

class BillingItem(db.Model):
    __tablename__ = 'billing_items'
    
    id = db.Column(db.Integer, primary_key=True)
    billing_record_id = db.Column(db.Integer, db.ForeignKey('billing_records.id'), nullable=False)
    service_code = db.Column(db.String(20), nullable=False)
    service_description = db.Column(db.String(256), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'billing_record_id': self.billing_record_id,
            'service_code': self.service_code,
            'service_description': self.service_description,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_price': float(self.total_price) if self.total_price else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
