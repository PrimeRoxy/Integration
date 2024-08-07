import logging
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from rq import Queue
from redis import Redis
from rq_dashboard_fast import RedisQueueDashboard
import time
from job import print_number, send_notification
from threading import Thread

app = FastAPI()

class JobData(BaseModel):
    lowest : int
    highest: int


# Setup the connection with Redis
redis_conn = Redis(host='localhost', port=6379, db=0)
q = Queue('notifications', connection=redis_conn)


# Dashboard for job queue in Redis
dashboard = RedisQueueDashboard("redis://localhost:6379/", "/rq")
app.mount("/rq", dashboard)


# Background Task Enqueuing
# A background thread is used to enqueue tasks periodically.
def enqueue_task():
    while True:
        job = q.enqueue(send_notification)
        print(job)
        print(f"Enqueued job {job.id}")
        time.sleep(30)

# Start a thread to enqueue tasks every 300 seconds
enqueue_thread = Thread(target=enqueue_task)
enqueue_thread.daemon = True
enqueue_thread.start()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "START"}


# Notifications Endpoint
# Retrieves notifications from a Redis list.
@app.get("/notifications")
def get_notifications():
    notifications = []
    while True:
        notification = redis_conn.lpop('notifications')
        if notification is None:
            break
        logging.info(f"Retrieved notifications: {notifications}")
        notifications.append(notification.decode())
    return {"notifications": notifications}

# Job Status Endpoint
# Fetches the status of a job by its ID.
@app.get("/job-status/{job_id}")
def get_job_status(job_id: str):
    job = q.fetch_job(job_id)
    if job:
        return {"job_id": job_id, "status": job.get_status()}
    else:
        return {"error": "Job not found"}
    

# User provided the two number then it perform tast
@app.post("/job")
def post_job(job: JobData):
    lowest = job.lowest
    highest = job.highest
    job_instance = q.enqueue(print_number, lowest, highest)
    return {
        "success": True,
        "job_id": job_instance.id
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




# Dependencies
# FastAPI: A modern, fast web framework for building APIs with Python.
# uvicorn: ASGI server for running the FastAPI application.
# rq: Simple Python library for queueing jobs and processing them in the background.
# redis: Python client for Redis.
# rq_dashboard_fast: Dashboard for monitoring RQ job queues.
# job: file containing the send_notification and print_number job function

# Running the Worker
# To process the queued jobs, you need to start a worker that will execute the send_notification function. You can do this by using the rq worker command from the command line.

# Command ===>    rq worker notifications
# This command run into WSL/ Linux
# reference code:
# q = Queue('notifications', connection=redis_conn)

# Run the server frist to connect with redis 
#  sudo service redis-server start 


