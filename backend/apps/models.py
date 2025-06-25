from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    mobile_number = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(80), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_flagged = db.Column(db.Boolean, default=False)
    prof_profile = db.Column(db.String(80), nullable=True)
    prof_experience = db.Column(db.String(80), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    service = db.relationship('Services', back_populates="professionals")
    cust_request = db.relationship('ServiceRequest', back_populates='customer', foreign_keys='ServiceRequest.customer_id')
    prof_request = db.relationship('ServiceRequest', back_populates='professional', foreign_keys='ServiceRequest.professional_id')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'location': self.location,
            'pincode': self.pincode,
            'mobile_number': self.mobile_number,
            'role': self.role,
            'is_approved': self.is_approved,
            'is_flagged': self.is_flagged,
            'prof_profile': self.prof_profile,
            'prof_experience': self.prof_experience,
            'service_id': self.service_id
        }

class Services(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), nullable=True)
    base_price = db.Column(db.Integer, nullable=True)
    time_required = db.Column(db.String(80), nullable=True)
    professionals = db.relationship('User', back_populates="service")
    service_requests = db.relationship('ServiceRequest', back_populates="service", cascade="all, delete")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'base_price': self.base_price,
            'time_required': self.time_required
        }

class ServiceRequest(db.Model):
    __tablename__ = "serviceRequest"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(80), nullable=True)
    date_created = db.Column(db.Date, nullable=False, default=datetime.now().date())
    date_closed = db.Column(db.Date, nullable=True)
    service = db.relationship('Services', back_populates='service_requests')
    customer = db.relationship('User', back_populates='cust_request', foreign_keys=[customer_id])
    professional = db.relationship('User', back_populates='prof_request', foreign_keys=[professional_id])


    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'customer_id': self.customer_id,
            'professional_id': self.professional_id,
            'description': self.description,
            'status': self.status,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_closed': self.date_closed.isoformat() if self.date_closed else None,
            'service': self.service.to_dict() if self.service else None,
            'customer': self.customer.to_dict() if self.customer else None,
            'professional': self.professional.to_dict() if self.professional else None
        }
