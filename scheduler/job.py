# import time
# import redis
# from rq import Queue

# r = redis.Redis(host='localhost', port=6379, db=0)
# q = Queue('notifications', connection=r)

# def send_notification():
#     message = f"Notification at {time.strftime('%Y-%m-%d %H:%M:%S')}"
#     r.rpush('notifications', message)
#     print(f"Added notification: {message}")

import time
from pydantic import BaseModel
import redis
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class JobData(BaseModel):
    lowest : int
    highest: int

class AppointmentData(BaseModel):
    date: str  # Date in 'YYYY-MM-DD' format
    time: str  # Time in 'HH:MM' format
    description: str

# Setup Redis connection
r = redis.Redis(host='localhost', port=6379)

def send_notification():
    try:
        message = f"Notification at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        r.rpush('notifications', message)
        print("================")
        print(f"Added notification: {message}")
        print("================")
    except Exception as e:
        logging.error(f"Failed to add notification: {e}")
        raise  # Reraise the exception to ensure the job fails properly



def print_number(lowest, highest):
    print("== Job processing started")
    x = lowest
    while x<=highest :
        print("{}\n".format(x))
        x = x+1
    print("== End ==")


# Function to add appointment data to Redis list
def add_appointment_to_redis(date, time, description):
    try:
        appointment_message = f"Appointment on {date} at {time}: {description}"
        r.rpush('appointments', appointment_message)
        logging.info(f"Scheduled appointment: {appointment_message}")
    except Exception as e:
        logging.error(f"Failed to schedule appointment: {e}")
        raise