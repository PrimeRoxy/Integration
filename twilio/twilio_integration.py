import random
import string
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID= os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
MESSAGE_TEMPLATE = os.getenv('MESSAGE_TEMPLATE')

client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_phone_sms(to_phone: int):
    otp = generate_otp()

    message = client.messages.create(
        from_ = TWILIO_PHONE_NUMBER,
        body = MESSAGE_TEMPLATE.format(otp=otp),
        to= to_phone
    )

    print(message)

to_phone = '+916386098744'
response = send_phone_sms(to_phone)
print(response)

