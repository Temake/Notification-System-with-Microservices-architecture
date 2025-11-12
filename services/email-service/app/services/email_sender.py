import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


async def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send email via Gmail SMTP
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.smtp_from_name} <{settings.smtp_user}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        # Add HTML and plain text versions
        text_part = MIMEText(body, "plain")
        html_part = MIMEText(body, "html")
        message.attach(text_part)
        message.attach(html_part)
        
        # Send via Gmail SMTP
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            use_tls=True,
        )
        
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise e
