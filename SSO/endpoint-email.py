# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, EmailStr
# import smtplib
# from dotenv import load_dotenv
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os

# load_dotenv()

# # Set up email credentials (using environment variables for security)
# SMTP_USER = os.getenv("SMTP_USER")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# # Define the SMTP server settings
# smtp_server = "smtp.gmail.com"
# smtp_port = 587

# app = FastAPI()

# # Pydantic model for request body
# class EmailRequest(BaseModel):
#     to_email: EmailStr
#     subject: str
#     body: str

# @app.post("/send-email/")
# async def send_email(request: EmailRequest):
#     try:
#         # Create a MIMEText object to represent the email
#         message = MIMEMultipart()
#         message["From"] = SMTP_USER
#         message["To"] = request.to_email
#         message["Subject"] = request.subject

#         # Attach the email body
#         body_part = MIMEText(request.body, "plain", _charset="utf-8")
#         message.attach(body_part)

#         # Send the email
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(SMTP_USER, SMTP_PASSWORD)
#             server.sendmail(SMTP_USER, request.to_email, message.as_string())

#         return {"message": "Email sent successfully!"}

#     except smtplib.SMTPAuthenticationError as auth_error:
#         raise HTTPException(status_code=401, detail=f"Authentication Error: {auth_error}")
#     except smtplib.SMTPException as smtp_error:
#         raise HTTPException(status_code=500, detail=f"SMTP Error: {smtp_error}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")




# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, EmailStr
# import smtplib
# from dotenv import load_dotenv
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os
# import random

# load_dotenv()

# # Set up email credentials (using environment variables for security)
# SMTP_USER = os.getenv("SMTP_USER")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# # Define the SMTP server settings
# smtp_server = "smtp.gmail.com"
# smtp_port = 587

# app = FastAPI()

# # Function to generate a 4-digit OTP
# def generate_otp():
#     """Generates a 4-digit OTP."""
#     otp = random.randint(1000, 9999)
#     return otp

# # Pydantic model for request body
# class OTPRequest(BaseModel):
#     to_email: EmailStr

# # Function to create a custom email template with OTP
# def create_otp_email_template(otp: int) -> str:
#     """Creates a custom email template for the OTP."""
#     template = f"""
#     <html>
#     <body>
#         <h2>Your OTP Code</h2>
#         <p>Your one-time password (OTP) is: <strong>{otp}</strong></p>
#         <p>This OTP is valid for 10 minutes.</p>
#         <p>If you did not request this code, please ignore this email.</p>
#     </body>
#     </html>
#     """
#     return template

# @app.post("/send-otp/")
# async def send_otp(request: OTPRequest):
#     try:
#         # Generate the OTP
#         otp = generate_otp()

#         # Create the email content
#         subject = "Your OTP Code"
#         body = create_otp_email_template(otp)

#         # Create a MIMEText object to represent the email
#         message = MIMEMultipart("alternative")
#         message["From"] = SMTP_USER
#         message["To"] = request.to_email
#         message["Subject"] = subject

#         # Attach the HTML body to the email
#         body_part = MIMEText(body, "html", _charset="utf-8")
#         message.attach(body_part)

#         # Send the email
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(SMTP_USER, SMTP_PASSWORD)
#             server.sendmail(SMTP_USER, request.to_email, message.as_string())

#         return {"message": "OTP sent successfully!", "otp": otp}  # Include OTP in response for testing purposes

#     except smtplib.SMTPAuthenticationError as auth_error:
#         raise HTTPException(status_code=401, detail=f"Authentication Error: {auth_error}")
#     except smtplib.SMTPException as smtp_error:
#         raise HTTPException(status_code=500, detail=f"SMTP Error: {smtp_error}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send OTP: {e}")





from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random
from typing import Dict, Tuple
from datetime import datetime, timedelta

from tools import generate_otp,create_otp_email_template
load_dotenv()

# Set up email credentials (using environment variables for security)
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Define the SMTP server settings
smtp_server = "smtp.gmail.com"
smtp_port = 587

app = FastAPI()

# Store OTPs in-memory for simplicity (email -> (otp, expiration_time))
otp_store: Dict[str, Tuple[int, datetime]] = {}

# # Function to generate a 4-digit OTP
# def generate_otp():
#     """Generates a 4-digit OTP."""
#     otp = random.randint(1000, 9999)
#     return otp

# Function to create a custom email template with OTP
# def create_otp_email_template(otp: int) -> str:
#     """Creates a custom email template for the OTP."""
#     template = f"""
#     <html>
#     <body>
#         <h2>Your OTP Code</h2>
#         <p>Your one-time password (OTP) is: <strong>{otp}</strong></p>
#         <p>This OTP is valid for 10 minutes.</p>
#         <p>If you did not request this code, please ignore this email.</p>
#     </body>
#     </html>
#     """
#     return template

# Pydantic model for sending OTP request
class OTPRequest(BaseModel):
    to_email: EmailStr

# Pydantic model for verifying OTP request
class OTPVerifyRequest(BaseModel):
    to_email: EmailStr
    otp: int

@app.post("/send-email-otp")
async def send_otp(request: OTPRequest):
    try:
        # Generate the OTP
        otp = generate_otp()
        expiration_time = datetime.now() + timedelta(minutes=10)

        # Store OTP and its expiration time
        otp_store[request.to_email] = (otp, expiration_time)

        # Create the email content
        subject = "Your OTP Code"
        body = create_otp_email_template(otp)

        # Create a MIMEText object to represent the email
        message = MIMEMultipart("alternative")
        message["From"] = SMTP_USER
        message["To"] = request.to_email
        message["Subject"] = subject

        # Attach the HTML body to the email
        body_part = MIMEText(body, "html", _charset="utf-8")
        message.attach(body_part)

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, request.to_email, message.as_string())

        return {"message": "OTP sent successfully!"}

    except smtplib.SMTPAuthenticationError as auth_error:
        raise HTTPException(status_code=401, detail=f"Authentication Error: {auth_error}")
    except smtplib.SMTPException as smtp_error:
        raise HTTPException(status_code=500, detail=f"SMTP Error: {smtp_error}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP: {e}")

@app.post("/verify-email-otp")
async def verify_otp(request: OTPVerifyRequest):
    # Check if OTP was sent to this email
    if request.to_email not in otp_store:
        raise HTTPException(status_code=400, detail="OTP not found for this email")

    stored_otp, expiration_time = otp_store[request.to_email]

    # Check if OTP has expired
    if datetime.now() > expiration_time:
        raise HTTPException(status_code=400, detail="OTP has expired")

    # Check if provided OTP matches the stored OTP
    if request.otp == stored_otp:
        # OTP is correct, remove it from store
        del otp_store[request.to_email]
        return {"message": "OTP verified successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")


