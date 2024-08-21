from celery import shared_task
from datetime import datetime, timedelta
from models import User, PurchaseHistory
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

@shared_task
def send_daily_reminder():
    # Calculate the time threshold for inactivity (24 hours ago)
    threshold_time = datetime.utcnow() - timedelta(hours=24)

    # Find users who haven't visited or made a purchase in the last 24 hours
    inactive_users = User.query.filter(User.last_login < threshold_time).all()

    # Prepare and send reminders to inactive users via email
    for user in inactive_users:
        # Prepare and send an email reminder
        message = Mail(
            from_email='your_email@example.com',
            to_emails=user.email,
            subject='Reminder: Visit our store!',
            html_content='<p>Hello, it seems you haven\'t visited our store recently. Come and check out our latest products!</p>')
        
        try:
            # Use SendGrid API to send emails (configure your SendGrid API key)
            sg = SendGridAPIClient('your_sendgrid_api_key')
            response = sg.send(message)
            print(response.status_code)  # Check if email sent successfully (200 indicates success)
        except Exception as e:
            print(e.message)  # Handle email sending errors
