# main.py
import os
import uvicorn
from fastapi import FastAPI
from rq_dashboard_fast import RedisQueueDashboard
from threading import Thread
from routes import router, enqueue_task
from dotenv import load_dotenv
load_dotenv()

REDIS_DASHBOARD_URL = os.getenv('REDIS_DASHBOARD_URL')

app = FastAPI()

# Dashboard for job queue in Redis
dashboard = RedisQueueDashboard(REDIS_DASHBOARD_URL, "/rq")
app.mount("/rq", dashboard)

# Start a thread to enqueue tasks periodically
enqueue_thread = Thread(target=enqueue_task)
enqueue_thread.daemon = True
enqueue_thread.start()

# Include the routes from the separate routes file
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
