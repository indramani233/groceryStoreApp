from celery import shared_task
from datetime import datetime, timedelta
from models import User, PurchaseHistory
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment

@shared_task
def generate_monthly_report():
    # Calculate the timeframe for the previous month
    today = datetime.utcnow()
    first_day_previous_month = today.replace(day=1) - timedelta(days=1)
    first_day_current_month = today.replace(day=1)
    
    # Query purchases made in the previous month
    purchases = PurchaseHistory.query.filter(
        PurchaseHistory.purchase_date >= first_day_previous_month,
        PurchaseHistory.purchase_date <= first_day_current_month
    ).all()

    # Aggregate user-wise purchase data
    user_purchase_data = {}
    for purchase in purchases:
        if purchase.user_id not in user_purchase_data:
            user_purchase_data[purchase.user_id] = {
                'user_id': purchase.user_id,
                'total_expenditure': 0,
                'total_orders': 0
            }
        user_purchase_data[purchase.user_id]['total_expenditure'] += purchase.amount
        user_purchase_data[purchase.user_id]['total_orders'] += 1

    # Prepare monthly activity report as HTML content
    report_content = '<h1>Monthly Activity Report</h1>'
    for user_id, data in user_purchase_data.items():
        user = User.query.get(user_id)
        report_content += f'<p>User: {user.name}, Total Orders: {data["total_orders"]}, Total Expenditure: {data["total_expenditure"]}</p>'

    # Prepare and send the report as an email attachment
    message = Mail(
        from_email='your_email@example.com',
        to_emails='recipient@example.com',
        subject='Monthly Activity Report',
        html_content=report_content)
    
    # Create an attachment (optional)
    attachment = Attachment()
    attachment.file_content = report_content
    attachment.file_name = 'monthly_report.html'
    attachment.file_type = 'text/html'
    attachment.disposition = 'attachment'
    message.attachment = attachment

    try:
        # Use SendGrid API to send emails (configure your SendGrid API key)
        sg = SendGridAPIClient('your_sendgrid_api_key')
        response = sg.send(message)
        print(response.status_code)  # Check if email sent successfully (200 indicates success)
    except Exception as e:
        print(e.message)  # Handle email sending errors
