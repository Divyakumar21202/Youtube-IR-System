import logging
import sys

# Configure logger
logging.basicConfig(
    level=logging.INFO, 
    format="Level : [%(levelname)s] \n provider : %(name)s \n Message : %(message)s\n\n",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Stream logs to console (works with Docker)
    ]
)


logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.INFO)
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

# Logger instance
logger = logging.getLogger("youtube-ir-system")

