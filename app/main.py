import os
import schedule
import threading
import time
import uvicorn
from telegram.client import Telegram, AuthorizationState
from handler import make_handler
from models import Base
from db import engine
from stats import collect_stats

def run_api():
    uvicorn.run("api:app", host="0.0.0.0", port=8000, log_level="info")

def run_scheduler():
    schedule.every(1).minutes.do(collect_stats)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Create tables if needed
    Base.metadata.create_all(engine)

    # Start API and scheduler in separate threads
    api_thread = threading.Thread(target=run_api)
    scheduler_thread = threading.Thread(target=run_scheduler)

    api_thread.start()
    scheduler_thread.start()

    # Optionally join threads to keep the main thread alive
    api_thread.join()
    scheduler_thread.join()
