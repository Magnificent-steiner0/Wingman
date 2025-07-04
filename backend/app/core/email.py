from app.core.config import settings
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient


def send_verification_email(to_email: str, token: str):
    subject = "Verify your email"
    verify_link = f"http://localhost:8000/auth/verify-email?token={token}"
    body = f"""
        <h2>Welcome to Wingman!<h2>
        <p>Please click the link below to verify your email: </p>
        <a href="{verify_link}">Verify Email</a>
    """
    
    mail = Mail(
        from_email =settings.SENDGRID_FROM_EMAIL,
        to_emails = to_email,
        subject = subject,
        html_content = body
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.set_sendgrid_data_residency("global")
        # response = sg.send(mail)
        response = sg.send(mail)
        print(response)
        print("Email sent!", response.status_code)
    except Exception as e:
        print("Failed to send email: ", str(e))



def send_password_reset_email(to_email: str, token: str):
    reset_link = f"http://localhost:8000/auth/reset-password?token={token}"
    subject = "Reset your password"
    body = f"""
        <h3>Reset Password Request</h3>
        <p>Click the link below to reset your password: </p>
        <a href="{reset_link}">Reset Password</a>
    """
    mail = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=body
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.set_sendgrid_data_residency("global")
        response = sg.send(mail)
        print(response)
        print("Password Reset Email Sent!", response.status_code)
    except Exception as e:
        print("Failed to send reset email: ", str(e))