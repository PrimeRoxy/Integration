# Function to generate a 4-digit OTP
import random


def generate_otp():
    """Generates a 4-digit OTP."""
    otp = random.randint(1000, 9999)
    return otp

def create_otp_email_template(otp: int) -> str:
    """Creates a custom email template for the OTP."""
    template = f"""
    <html>
    <body>
        <h2>Your OTP Code</h2>
        <p>Your one-time password (OTP) is: <strong>{otp}</strong></p>
        <p>This OTP is valid for 10 minutes.</p>
        <p>If you did not request this code, please ignore this email.</p>
    </body>
    </html>
    """
    return template



