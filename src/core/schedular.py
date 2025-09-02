from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.background_tasks import fetch_videos_task

# Initialize the AsyncIO scheduler
app_scheduler = AsyncIOScheduler()

# Add a recurring job to the scheduler:
# - Calls fetch_and_save_videos function every 10 seconds
app_scheduler.add_job(
    fetch_videos_task.fetch_and_save_videos,  # Task to run
    "interval",                               # Run at fixed intervals
    seconds=10                                # Interval duration
)
