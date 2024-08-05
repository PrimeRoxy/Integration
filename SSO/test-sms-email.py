import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

load_dotenv()

# Set up email credentials (using environment variables for security)
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
# SMTP_USER ='primekiller444@gmail.com'
# SMTP_PASSWORD='pehp ggyo zjwt rnbv'

# Define the SMTP server settings
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Email content
to_email = "vipuldashingboy@gmail.com"
subject = "Test Email"
body = "This is a test email sent using smtplib."

# Create a MIMEText object to represent the email
message = MIMEMultipart()
message["From"] = SMTP_USER
message["To"] = to_email
message["Subject"] = subject

# Attach the email body
body_part = MIMEText(body, "plain", _charset="utf-8")
print(f"Body part: {body_part}")

if body_part is not None:
    message.attach(body_part)
else:
    print("Failed to create body_part")

# Check the email message
message_string = message.as_string()
if message_string is None:
    raise ValueError("The email message or its string representation is None")

# Send the email
try:
    # Set up the SMTP server and start the connection
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        print(server)
        server.starttls()
        print("login to server")
        server.login(SMTP_USER, SMTP_PASSWORD)

        # Send the email
        server.sendmail(SMTP_USER, to_email, message_string)
        print("Email sent successfully!")

except smtplib.SMTPAuthenticationError as auth_error:
    print(f"Authentication Error: {auth_error}")
except smtplib.SMTPException as smtp_error:
    print(f"SMTP Error: {smtp_error}")
except Exception as e:
    print(f"Failed to send email: {e}")
