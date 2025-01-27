import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject: str, body: str):
    # Gmail SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Your Gmail account credentials
    sender_email = "your_email"
    sender_password = "<your_app_password>"  # Use your App Password if 2FA is enabled

    # Recipient email address
    receiver_email = "your_email"

    # Create the email headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Create the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server and login with your Gmail credentials
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()  # Terminate the SMTP session

# Usage example
send_email("Test Email", "Bug alert in Algo")
