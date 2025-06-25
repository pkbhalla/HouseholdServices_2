from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import request, jsonify
from .models import db, User, Services, ServiceRequest
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os, json
from flask import current_app as app
from werkzeug.utils import secure_filename
from flask import current_app as app
from flask_caching import Cache

mycache = Cache(app)


def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = User.query.get(json.loads(get_jwt_identity()))
        if not current_user or current_user.role != 'admin':
            return {'message': 'Admin access required'}, 403
        return fn(*args, **kwargs)
    return wrapper

class AdminAuthResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email'], role="admin").first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=json.dumps(user.id))
            return {
                'access_token': access_token,
                'user_id': user.id,
                'role': user.role
            }, 200
        return {'message': 'Invalid credentials'}, 401



class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.role == "professional":
                if not user.is_approved:
                    return {'message': 'Your account is not yet approved'}, 403
                if user.is_flagged:
                    return {'message': 'Your account has been flagged'}, 403
            elif user.role == "customer":
                if user.is_flagged:
                    return {'message': 'Your account has been flagged'}, 403
            
            access_token = create_access_token(identity=json.dumps(user.id))
            return {
                'access_token': access_token,
                'user_id': user.id,
                'role': user.role
            }, 200
        else:
            return {'message': 'Invalid email or password'}, 401

class CustomerRegisterResource(Resource):
    def post(self):
        data = request.json
        
        
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Account with this Email already exists'}, 409
            
    
        if User.query.filter_by(name=data['name']).first():
            return {'message': 'Account with this Name already exists'}, 409
            
        new_user = User(
            name=data['name'],
            email=data['email'],
            location=data['location'],
            pincode=data['pincode'],
            mobile_number=data['mobile_number'],
            role="customer",
            is_approved=True
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'Registration successful'}, 201

class ProfessionalRegisterResource(Resource):
    def post(self):
        data = request.form
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Account with this Email already exists'}, 409
        if User.query.filter_by(name=data['name']).first():
            return {'message': 'Account with this Name already exists'}, 409
        if 'prof_profile' not in request.files:
            return {'message': 'No profile file provided'}, 400
            
        prof_profile = request.files['prof_profile']
        if prof_profile.filename == '':
            return {'message': 'No file selected'}, 400
        prof_filename = secure_filename(prof_profile.filename)
        file_ext = prof_filename.split(".")[-1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return {'message': 'Invalid file extension'}, 400
        renamed_prof_filename = f"{data['email'].split('@')[0]}.{file_ext}"
        prof_profile.save(os.path.join(app.config['UPLOAD_PATH'], renamed_prof_filename))
        service_id = Services.query.filter_by(name=data['service']).first().id
        new_user = User(
            name=data['name'],
            email=data['email'],
            location=data['location'],
            pincode=data['pincode'],
            mobile_number=data['mobile_number'],
            role="professional",
            is_approved=False,
            prof_profile=renamed_prof_filename,
            prof_experience=data['prof_experience'],
            service_id=service_id
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Registration successful'}, 201


class AdminDashboardResource(Resource):
    @admin_required
    # @mycache.cached(timeout=5)
    def get(self):
        users = User.query.all()
        services = Services.query.all()
        service_requests = ServiceRequest.query.all()
        unapproved_professionals = User.query.filter_by(role="professional", is_approved=False).all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'services': [service.to_dict() for service in services],
            'service_requests': [request.to_dict() for request in service_requests],
            'unapproved_professionals': [prof.to_dict() for prof in unapproved_professionals]
        })

class CustomerDashboardResource(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.get(json.loads(get_jwt_identity()))
        if current_user.role != 'customer':
            return {'message': 'Access denied'}, 403
        
        services = Services.query.join(Services.professionals).filter(User.role == "professional", User.is_approved == True, User.is_flagged == False).distinct().all()
        service_requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
        professionals_by_service = {
            service.id: User.query.filter_by(service_id=service.id, role="professional", is_approved=True).all()
            for service in services
        }
        
        return jsonify({
            'services': [service.to_dict() for service in services],
            'service_requests': [request.to_dict() for request in service_requests],
            'professionals_by_service': {k: [p.to_dict() for p in v] for k, v in professionals_by_service.items()}
        })

class ProfessionalDashboardResource(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.get(json.loads(get_jwt_identity()))
        if current_user.role != 'professional':
            return {'message': 'Access denied'}, 403
        
        pending_requests = ServiceRequest.query.join(ServiceRequest.customer).filter(ServiceRequest.professional_id == current_user.id, ServiceRequest.status == "Pending", User.is_flagged == False).all()
        completed_requests = ServiceRequest.query.join(ServiceRequest.customer).filter(ServiceRequest.professional_id == current_user.id, ServiceRequest.status == "Closed", User.is_flagged == False).all()
        active_requests = ServiceRequest.query.join(ServiceRequest.customer).filter(ServiceRequest.professional_id == current_user.id, ServiceRequest.status == "Accepted", User.is_flagged == False).all()
        rejected_requests = ServiceRequest.query.join(ServiceRequest.customer).filter(ServiceRequest.professional_id == current_user.id, ServiceRequest.status == "Rejected", User.is_flagged == False).all()
        
        return jsonify({
            'pending_requests': [request.to_dict() for request in pending_requests],
            'completed_requests': [request.to_dict() for request in completed_requests],
            'active_requests': [request.to_dict() for request in active_requests],
            'rejected_requests': [request.to_dict() for request in rejected_requests]
        })

class ServiceResource(Resource):
    def get(self, service_id=None):
        if service_id:
            service = Services.query.get_or_404(service_id)
            return jsonify(service.to_dict())
        services = Services.query.all()
        return jsonify([service.to_dict() for service in services])

    @admin_required
    def post(self):
        data = request.get_json()
        new_service = Services(
            name=data['name'],
            description=data['description'],
            base_price=data['base_price'],
            time_required=data['time_required']
        )
        db.session.add(new_service)
        db.session.commit()
        return {'message': 'Service created successfully'}, 201

    @admin_required
    def put(self, service_id):
        service = Services.query.get_or_404(service_id)
        data = request.get_json()
        service.name = data.get('name', service.name)
        service.description = data.get('description', service.description)
        service.base_price = data.get('base_price', service.base_price)
        service.time_required = data.get('time_required', service.time_required)
        db.session.commit()
        return {'message': 'Service updated successfully'}

    @admin_required
    def delete(self, service_id):
        service = Services.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return {'message': 'Service deleted successfully'}

class ServiceRequestResource(Resource):
    @jwt_required()
    def get(self, request_id=None):
        if request_id:
            service_request = ServiceRequest.query.get_or_404(request_id)
            return jsonify(service_request.to_dict())
        service_requests = ServiceRequest.query.all()
        return jsonify([request.to_dict() for request in service_requests])

    @jwt_required()
    def post(self):
        current_user = User.query.get(json.loads(get_jwt_identity()))
        if current_user.role != 'customer':
            return {'message': 'Access denied'}, 403
        
        data = request.get_json()
        new_request = ServiceRequest(
            service_id=data['service_id'],
            customer_id=current_user.id,
            professional_id=data['professional_id'],
            description=data['description'],
            status='Pending'
        )
        db.session.add(new_request)
        db.session.commit()
        return {'message': 'Service request created successfully'}, 201

    @jwt_required()
    def put(self, request_id):
        service_request = ServiceRequest.query.get_or_404(request_id)
        current_user = User.query.get(json.loads(get_jwt_identity()))
        
        if current_user.role == 'customer' and service_request.customer_id != current_user.id:
            return {'message': 'Access denied'}, 403
        
        if current_user.role == 'professional' and service_request.professional_id != current_user.id:
            return {'message': 'Access denied'}, 403
        
        data = request.get_json()
        if current_user.role == 'customer':
            service_request.description = data.get('description', service_request.description)
        elif current_user.role == 'professional':
            service_request.status = data.get('status', service_request.status)
            if service_request.status == 'Closed':
                service_request.date_closed = datetime.now().date()
        
        db.session.commit()
        return {'message': 'Service request updated successfully'}

    @jwt_required()
    def delete(self, request_id):
        current_user = User.query.get(json.loads(get_jwt_identity()))
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        if current_user.role != 'customer' or service_request.customer_id != current_user.id:
            return {'message': 'Access denied'}, 403
        
        db.session.delete(service_request)
        db.session.commit()
        return {'message': 'Service request deleted successfully'}



class ProfessionalApprovalResource(Resource):
    @admin_required
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        if user.role != "professional":
            return {'message': 'User is not a professional'}, 400
        user.is_approved = True
        db.session.commit()
        return {'message': 'Professional approved successfully'}, 200

class UserFlagResource(Resource):
    @admin_required
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        if user.role == "admin":
            return {'message': 'Cannot flag admin user'}, 403
        user.is_flagged = not user.is_flagged 
        flag_status = "flagged" if user.is_flagged else "unflagged"
        db.session.commit()
        return {'message': f'User {flag_status} successfully'}, 200

class ServiceRequestStatusResource(Resource):
    @jwt_required()
    def put(self, request_id):
        current_user = User.query.get(json.loads(get_jwt_identity()))
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        if current_user.role != 'professional' or service_request.professional_id != current_user.id:
            return {'message': 'Access denied'}, 403
        
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ["Accepted", "Rejected"]:
            return {'message': 'Invalid status value'}, 400
            
        service_request.status = new_status
        db.session.commit()
        return {'message': f'Service request {new_status.lower()} successfully'}, 200

class CustomerServiceRequestCloseResource(Resource):
    @jwt_required()
    def put(self, request_id):
        current_user = User.query.get(json.loads(get_jwt_identity()))
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        if current_user.role != 'customer' or service_request.customer_id != current_user.id:
            return {'message': 'Access denied'}, 403
        
    
        if service_request.status != "Accepted":
            return {'message': 'Only accepted requests can be closed'}, 400
        
        service_request.status = "Closed"
        service_request.date_closed = datetime.now().date()
        db.session.commit()
        return {'message': 'Service request closed successfully'}, 200



class CustomerSearchResource(Resource):
    @jwt_required()
    def get(self):
        services = Services.query.all()
        result = []
        
        for service in services:
            service_data = service.to_dict()
            professionals = User.query.filter_by(
                service_id=service.id, 
                role="professional",
                is_approved=True,
                is_flagged=False
            ).all()
            
            service_data['professionals'] = [prof.to_dict() for prof in professionals]
            if service_data['professionals']: 
                result.append(service_data)
                
        return result





class AdminSummaryResource(Resource):
    @admin_required
    def get(self):
        pending_requests = ServiceRequest.query.filter(ServiceRequest.status == "Pending").count() or 0
        completed_requests = ServiceRequest.query.filter(ServiceRequest.status == "Closed").count() or 0
        active_requests = ServiceRequest.query.filter(ServiceRequest.status == "Accepted").count() or 0
        rejected_requests = ServiceRequest.query.filter(ServiceRequest.status == "Rejected").count() or 0
        professionals_count = User.query.filter(User.role == "professional").count() or 0
        customers_count = User.query.filter(User.role == "customer").count() or 0
        
      
        user_distribution = {
            'roles': ["Professional", "Customer"],
            'counts': [professionals_count, customers_count]
        }
        
        request_distribution = {
            'status': ['Accepted', 'Rejected', 'Closed', 'Pending'],
            'counts': [active_requests, rejected_requests, completed_requests, pending_requests]
        }
        
        return jsonify({
            'pending_requests': pending_requests,
            'completed_requests': completed_requests,
            'active_requests': active_requests,
            'rejected_requests': rejected_requests,
            'professionals_count': professionals_count,
            'customers_count': customers_count,
            'user_distribution': user_distribution,
            'request_distribution': request_distribution
        })



import time

@app.route('/api/testcache', methods=['GET'])
@mycache.cached(timeout=120)
def testingcache():
    time.sleep(20)
    return "I am now cached. Try reloading me, but I won't be reloading for next 120 seconds."



from .tasks import export_closed_requests_csv

class AdminExportCSVResource(Resource):
    @jwt_required()
    def post(self):
        current_user = User.query.get(json.loads(get_jwt_identity()))
        if not current_user or current_user.role != 'admin':
            return {'message': 'Admin access required'}, 403
        task = export_closed_requests_csv.delay(current_user.email)
        
        return {
            'message': 'CSV export job started. You will receive an email when it completes.',
            'task_id': task.id
        }