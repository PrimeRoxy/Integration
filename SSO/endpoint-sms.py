from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import os
import random
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
from tools import generate_otp
# Load environment variables from .env file
load_dotenv()

# Get Kaleyra credentials from environment variables
KALEYRA_API_KEY = os.getenv("SSO_KALEYRA_API_KEY")
KALEYRA_SID = os.getenv("SSO_KALEYRA_SID")

# In-memory store for OTPs (for demonstration purposes)
otp_store = {}

# Initialize FastAPI app
app = FastAPI()

class OTPRequest(BaseModel):
    to_number: str

class OTPVerification(BaseModel):
    to_number: str
    otp: int

def generate_otp():
    """Generates a 4-digit OTP."""
    return random.randint(1000, 9999)

def send_otp_phone(to_number: str):
    """Sends OTP via phone using the Kaleyra API."""
    otp = generate_otp()
    try:
        url = f"https://api.kaleyra.io/v1/{KALEYRA_SID}/messages"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "api-key": KALEYRA_API_KEY,
        }
        data = {
            "to": f"+91{to_number}",
            "type": "OTP",
            "sender": "ELEANC",  # Replace with your sender ID
            "body": f"{otp} is your OTP to login and access the app - ELEGANCE.",
            "template_id": "1707170071594360463",  # Replace with your template ID
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code // 100 == 2:
            # Store OTP in the in-memory store with a timestamp
            otp_store[to_number] = {
                'otp': otp,
                'expires_at': datetime.now() + timedelta(minutes=5)  # OTP valid for 5 minutes
            }
            return {"status": "success", "message": "OTP sent successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send OTP via SMS")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/send-otp", response_model=dict)
async def send_otp_endpoint(request: OTPRequest):
    """Endpoint to send OTP to a phone number."""
    return send_otp_phone(request.to_number)

@app.post("/verify-otp", response_model=dict)
async def verify_otp_endpoint(request: OTPVerification):
    """Endpoint to verify OTP."""
    to_number = request.to_number
    input_otp = request.otp
    
    record = otp_store.get(to_number)
    if record:
        stored_otp = record['otp']
        expires_at = record['expires_at']
        if datetime.now() > expires_at:
            del otp_store[to_number]
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP has expired")
        if input_otp == stored_otp:
            del otp_store[to_number]
            return {"status": "success", "message": "OTP verified successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect OTP")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No OTP found for this number")
