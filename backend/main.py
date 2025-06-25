from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from apps.config import Config
from apps.models import db, User, Services, ServiceRequest
import apps.celery_workers as celery_workers
import apps.tasks as tasks
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions

jwt = JWTManager(app)
api = Api(app)
mail = Mail(app)
# Initialize database
db.init_app(app)
app.app_context().push()

def admin_create():
    admin = User.query.filter_by(email='admin@hsapp.com').first()
    if not admin:
        admin = User(
            name='Admin',
            email='admin@hsapp.com',
            role='admin',
            is_approved=True
        )
        admin.set_password('0000')
        db.session.add(admin)
        db.session.commit()



celery = celery_workers.celery

celery.conf.update(
        broker_url='redis://localhost:6379',
        result_backend='redis://localhost:6379'
    )
celery.Task = celery_workers.ContextTask
app.app_context().push()


celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'apps.tasks.send_daily_reminders',
        'schedule': 15.0,  # Every 15 seconds for testing
        # Use this for production: crontab(hour=20, minute=30)  # 8:30 PM IST
    },
    'generate-monthly-report': {
        'task': 'apps.tasks.generate_monthly_report',
        'schedule': 15.0,  # Every 15 seconds for testing
        # Use this for production: crontab(day_of_month=1, hour=8)  # 1st day of month at 8 AM
    },
}






from apps.api import (
    AdminDashboardResource, CustomerDashboardResource, 
    ProfessionalDashboardResource, ServiceResource, ServiceRequestResource, 
    AdminAuthResource , AuthResource, AdminSummaryResource, ProfessionalApprovalResource,
    UserFlagResource, ServiceRequestStatusResource, CustomerServiceRequestCloseResource,
    CustomerRegisterResource, ProfessionalRegisterResource, CustomerSearchResource, AdminExportCSVResource
)


api.add_resource(AdminAuthResource, '/api/admin/auth')
api.add_resource(AuthResource, '/api/auth')
api.add_resource(AdminDashboardResource, '/api/admin/dashboard')
api.add_resource(CustomerDashboardResource, '/api/customer/dashboard')
api.add_resource(ProfessionalDashboardResource, '/api/professional/dashboard')
api.add_resource(ServiceResource, '/api/service', '/api/service/<int:service_id>')
api.add_resource(ServiceRequestResource, '/api/service-request', '/api/service-request/<int:request_id>')
api.add_resource(AdminSummaryResource, '/api/admin/summary')
api.add_resource(CustomerRegisterResource, '/api/register/customer')
api.add_resource(ProfessionalRegisterResource, '/api/register/professional')
api.add_resource(ServiceRequestStatusResource, '/api/professional/service-request/<int:request_id>')
api.add_resource(CustomerServiceRequestCloseResource, '/api/customer/service-request/close/<int:request_id>')
api.add_resource(ProfessionalApprovalResource, '/api/admin/approve-professional/<int:user_id>')
api.add_resource(UserFlagResource, '/api/admin/flag-user/<int:user_id>')
api.add_resource(CustomerSearchResource, '/api/customer/search')
api.add_resource(AdminExportCSVResource, '/api/admin/export-csv')



from flask import send_from_directory

@app.route('/api/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)



if __name__ == '__main__':
    db.create_all()
    admin_create()  
    app.run(debug=True)
