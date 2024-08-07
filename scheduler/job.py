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
import redis
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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