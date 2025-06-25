from datetime import datetime
import csv
import io
from flask import render_template
from flask_mail import Message, Mail
from celery.schedules import crontab
from .models import User, ServiceRequest, Services
from .celery_workers import celery, ContextTask
from flask import current_app as app

mail = Mail()



@celery.task
def send_daily_reminders():
    professionals = User.query.filter_by(role="professional", is_approved=True, is_flagged=False).all()
    
    for professional in professionals:
        pending_requests = ServiceRequest.query.filter_by(
            professional_id=professional.id, 
            status="Pending"
        ).all()
        
        if pending_requests:
            msg = Message(
                subject="Reminder: You have pending service requests",
                recipients=[professional.email],
                body=f"Hello {professional.name},\n\nYou have {len(pending_requests)} pending service requests. "
                     f"Please log in to your account to accept or reject them.\n\nThank you,\nNestCare Team"
            )
            mail.send(msg)
    
    return f"Daily reminders sent at {datetime.now()}"

@celery.task
def generate_monthly_report():

    customers = User.query.filter_by(role="customer", is_flagged=False).all()
    
    for customer in customers:
   
        service_requests = ServiceRequest.query.filter_by(customer_id=customer.id).all()
        
        if service_requests:
     
            total_requests = len(service_requests)
            pending_requests = sum(1 for req in service_requests if req.status == "Pending")
            accepted_requests = sum(1 for req in service_requests if req.status == "Accepted")
            closed_requests = sum(1 for req in service_requests if req.status == "Closed")
            rejected_requests = sum(1 for req in service_requests if req.status == "Rejected")
            
         
            html_content = render_template(
                'monthly_report.html',
                customer=customer,
                total_requests=total_requests,
                pending_requests=pending_requests,
                accepted_requests=accepted_requests,
                closed_requests=closed_requests,
                rejected_requests=rejected_requests,
                month=datetime.now().strftime('%B %Y'),
                requests=service_requests
            )
            
        
            msg = Message(
                subject=f"Monthly Activity Report - {datetime.now().strftime('%B %Y')}",
                recipients=[customer.email],
                html=html_content
            )
            mail.send(msg)
    
    return f"Monthly reports generated and sent at {datetime.now()}"

@celery.task
def export_closed_requests_csv(admin_email):
    closed_requests = ServiceRequest.query.filter_by(status="Closed").all()
    
    if not closed_requests:
        msg = Message(
            subject="CSV Export - No Data",
            recipients=[admin_email],
            body="There are no closed service requests to export."
        )
        mail.send(msg)
        return "No data to export"
    
  
    output = io.StringIO()
    writer = csv.writer(output)
    
 
    writer.writerow([
        'Request ID', 'Service Name', 'Customer Name', 'Professional Name',
        'Description', 'Date Created', 'Date Closed'
    ])
    
  
    for request in closed_requests:
        service = Services.query.get(request.service_id)
        customer = User.query.get(request.customer_id)
        professional = User.query.get(request.professional_id)
        
        writer.writerow([
            request.id,
            service.name if service else 'N/A',
            customer.name if customer else 'N/A',
            professional.name if professional else 'N/A',
            request.description,
            request.date_created,
            request.date_closed
        ])
    
    
    msg = Message(
        subject="Closed Service Requests CSV Export",
        recipients=[admin_email],
        body="Please find attached the CSV export of all closed service requests."
    )
    
    msg.attach(
        filename="closed_requests.csv",
        content_type="text/csv",
        data=output.getvalue()
    )
    
    mail.send(msg)
    return f"CSV export completed and sent to {admin_email} at {datetime.now()}"
