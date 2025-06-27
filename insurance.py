from datetime import datetime
from src.models import db

class InsuranceDetail(db.Model):
    __tablename__ = 'insurance_details'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    hmo_id = db.Column(db.Integer, db.ForeignKey('hmo_providers.id'), nullable=False)
    policy_number = db.Column(db.String(64), nullable=False)
    group_number = db.Column(db.String(64))
    coverage_start_date = db.Column(db.Date, nullable=False)
    coverage_end_date = db.Column(db.Date)
    primary_holder_name = db.Column(db.String(128))
    relationship_to_primary = db.Column(db.String(64))
    coverage_type = db.Column(db.String(64))  # e.g., full, partial, specific services
    coverage_details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    hmo_provider = db.relationship('HMOProvider', backref='insurance_details')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'hmo_id': self.hmo_id,
            'policy_number': self.policy_number,
            'group_number': self.group_number,
            'coverage_start_date': self.coverage_start_date.isoformat() if self.coverage_start_date else None,
            'coverage_end_date': self.coverage_end_date.isoformat() if self.coverage_end_date else None,
            'primary_holder_name': self.primary_holder_name,
            'relationship_to_primary': self.relationship_to_primary,
            'coverage_type': self.coverage_type,
            'coverage_details': self.coverage_details,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
