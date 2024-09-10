# FastAPI Redis Queue (RQ) Notification System

This project is a FastAPI-based notification system that uses Redis Queue (RQ) for background job processing. The system includes endpoints for scheduling appointments, submitting jobs, and viewing job statuses, with background jobs such as sending notifications being enqueued periodically.


How the Worker Operates
The Redis Queue (RQ) worker listens on the notifications queue, waiting for jobs to be enqueued. Jobs can be enqueued through FastAPI endpoints like /job or /schedule-appointment, and each job is assigned a unique job ID. The worker processes these jobs, executes the task (like sending a notification), and logs the result.


Example of Job Submission and Worker Logs
When a job is submitted through the API (e.g., POST /job or POST /schedule-appointment), the system logs the enqueuing of the job:
INFO:     127.0.0.1:55740 - "POST /job HTTP/1.1" 200 OK
<Job 76e3f9f5-f194-487f-b805-0ab91bfd3a27: job.send_notification()>
Enqueued job 76e3f9f5-f194-487f-b805-0ab91bfd3a27
INFO:     127.0.0.1:55750 - "GET /rq/jobs/json?state=all&queue_name=all&page=1 HTTP/1.1" 200 OK


The worker then processes the job, logs the execution and result, and stores the result for a period (e.g., 500 seconds):
INFO:rq.worker:notifications: Job OK (723b4679-6dd1-4298-89c1-68de3ac5a58f)
16:46:41 Result is kept for 500 seconds
INFO:rq.worker:Result is kept for 500 seconds
================
Added notification: Notification at 2024-09-10 16:46:41
================


Periodic Job Enqueuing
The system is designed to enqueue a job that sends notifications every 30 seconds using a background thread. This is an example of how periodic tasks can be automatically enqueued:
<Job 18937ca0-67e3-4732-8fe5-bae8c867b86d: job.send_notification()>
Enqueued job 18937ca0-67e3-4732-8fe5-bae8c867b86d
INFO:rq.worker:notifications: Job OK (b1ee8ff7-6231-4191-9726-e75d1f1f30d2)

These logs show when jobs are enqueued, processed, and the results returned.

### Explanation of the Worker

- **Job Enqueuing**: Each time a job is submitted, it is added to the `notifications` queue with a unique ID.
- **Worker Processing**: The worker processes jobs from the queue, logging each step (job execution, job completion, result storage).
- **Result Storage**: Results are stored for a configured period (e.g., 500 seconds), and the worker logs the result retention details.

## Project Structure

 main.py # Entry point for running the FastAPI application.
├── routes.py # API endpoints for notifications, jobs, and appointments.
├── job.py # Job functions that are enqueued and executed in the background.
├── init.py # (Optional) To make the directory a package if necessary.


### Features
- Background job queuing using Redis Queue (RQ)
- FastAPI endpoints for job submission and job status tracking
- Notifications system using Redis
- Periodic enqueuing of notification jobs
- **Redis Queue Dashboard** for monitoring job queues

### Redis Queue Dashboard
The project includes a dashboard for monitoring the Redis job queue, which can be accessed through the /rq endpoint. This dashboard provides a real-time view of job states (queued, started, finished, failed) and other metrics for tracking job processing.

The RedisQueueDashboard provides a simple, interactive UI for viewing and managing Redis queues. You can access the dashboard by navigating to:
 http://127.0.0.1:8000/rq
 

## Installation

### Prerequisites

- Python 3.12
- Redis server running on `localhost:6379`

Install dependencies:
pip install -r requirements.txt

Run Redis server:
redis-server

### Running the Application

# Start the FastAPI application:
uvicorn main:app --reload

# Start the Redis worker:
rq worker notifications


Endpoints
1. Root Endpoint
GET / Returns a simple message to indicate the server is running.

2. Notifications Endpoint
GET /notifications Retrieves notifications from Redis.

response:
{
  "notifications": [
    "Notification at 2024-09-10 15:57:01",
    "Notification at 2024-09-10 16:03:36",
    "Notification at 2024-09-10 16:04:13",
    "Notification at 2024-09-10 16:04:54",
    "Notification at 2024-09-10 16:05:33",
    "Notification at 2024-09-10 16:06:13",
    "Notification at 2024-09-10 16:06:53",
    "Notification at 2024-09-10 16:07:33",
    "Notification at 2024-09-10 16:08:13",
    "Notification at 2024-09-10 16:08:45",
  ]
}

3. Job Status Endpoint
GET /job-status/{job_id} Fetches the status of a job by its ID.

Required:
{
    "job_id": "782feef6-7393-4c18-9cc5-d5c55d0143ed"
}

Response:
{
  "job_id": "782feef6-7393-4c18-9cc5-d5c55d0143ed",
  "status": "queued"
}

4. Job Submission
POST /job Submits a job to process two numbers and returns the job ID.
Required:
{
  "lowest": 2,
  "highest": 7
}

Response:
{
  "success": true,
  "job_id": "dfbd50c2-00d6-4cf6-994e-71eb934ecb9f"
}

5. Appointment Scheduling
POST /schedule-appointment Schedules an appointment and returns the job ID.
Request body:
{
  "date": "12-09-2024",
  "time": "11:00 am",
  "description": "test schedule"
}

	
Response body:
{
  "success": true,
  "job_id": "68a3ab28-bbaf-476a-b7c9-a2aee7907bfa",
  "message": "Appointment scheduled for 12-09-2024 at 11:00 am"
}

## Periodic Task Enqueuing
The system automatically enqueues a notification job every 30 seconds using a background thread.
