from datetime import datetime
from src.models import db

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(256))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip_code = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    emergency_contact_name = db.Column(db.String(128))
    emergency_contact_phone = db.Column(db.String(20))
    blood_type = db.Column(db.String(10))
    allergies = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    insurance_details = db.relationship('InsuranceDetail', backref='patient', lazy=True)
    billing_records = db.relationship('BillingRecord', backref='patient', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'email': self.email,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'blood_type': self.blood_type,
            'allergies': self.allergies,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
