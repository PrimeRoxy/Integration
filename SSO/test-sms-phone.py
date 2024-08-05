# import os
# import random
# from dotenv import load_dotenv
# import requests

# def generate_otp():
#     """Generates a 4-digit OTP."""
#     otp = random.randint(1000, 9999)
#     return otp
 
# # Load environment variables from .env file
# load_dotenv()

# # Get Kaleyra credentials from environment variables
# KALEYRA_API_KEY = os.getenv("SSO_KALEYRA_API_KEY")
# KALEYRA_SID = os.getenv("SSO_KALEYRA_SID")


# def send_otp_phone(to_number):
#     """Sends OTP via email and phone using the Kaleyra API."""
#     otp = generate_otp()
#     try:
        
#         url = f"https://api.kaleyra.io/v1/{KALEYRA_SID}/messages"
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded",
#             "api-key": KALEYRA_API_KEY,
#         }
#         # template_id and sender message must be same that approve by dlt by kaleyra
#         data = {
#             "to": f"+91{to_number}",
#             "type": "OTP",
#             "sender": "ELEANC",  # Replace with your sender ID
#             "body": str(otp)+" is your OTP to login and access the app - ELEGANCE.",
#             "template_id": "1707170071594360463",  # Replace with your template ID
#         }

#         response = requests.post(url, headers=headers, data=data)
#         if response.status_code // 100 == 2:
#             print("OTP sent successfully via SMS.")
#         else:
#             print(f"Failed to send OTP via SMS: {response.text}")
#     except Exception as e:
#         print(f"Error sending SMS: {e}")


# to_number = 9113797240

# send_otp_phone(to_number)


import os
import random
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

# In-memory store for OTPs (for demonstration purposes)
otp_store = {}

# Load environment variables from .env file
load_dotenv()

# Get Kaleyra credentials from environment variables
KALEYRA_API_KEY = os.getenv("SSO_KALEYRA_API_KEY")
KALEYRA_SID = os.getenv("SSO_KALEYRA_SID")

def generate_otp():
    """Generates a 4-digit OTP."""
    otp = random.randint(1000, 9999)
    return otp

def send_otp_phone(to_number):
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
            print("OTP sent successfully via SMS.")
        else:
            print(f"Failed to send OTP via SMS: {response.text}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def verify_otp(to_number, input_otp):
    """Verifies the OTP provided by the user."""
    record = otp_store.get(to_number)
    if record:
        stored_otp = record['otp']
        expires_at = record['expires_at']
        if datetime.now() > expires_at:
            print("OTP has expired.")
            return False
        if input_otp == stored_otp:
            print("OTP verified successfully.")
            # OTP is correct, remove it from the store
            del otp_store[to_number]
            return True
        else:
            print("Incorrect OTP.")
            return False
    else:
        print("No OTP found for this number.")
        return False

# Example usage
to_number = "9113797240"

# Send OTP
send_otp_phone(to_number)

# User input for OTP (this would typically come from the user interface)
input_otp = int(input("Enter the OTP sent to your phone: "))

# Verify OTP
verify_otp(to_number, input_otp)
