from loguru import logger
import sys
import os

# Configure loguru to log to both console and a file
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logger.remove()  # Remove default logger
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
)
logger.add(
    LOG_FILE,
    rotation="1 week",
    retention="4 weeks",
    level="DEBUG",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function} - {message}",
)

# Usage example:
if __name__ == "__main__":
    logger.info("This is an info message")
    logger.error("This is an error message")
