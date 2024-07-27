import os

class Config:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    SESSION_NAME = os.environ.get("SESSION_NAME", "my_bot")
    HOST = os.environ.get("HOST", "localhost")  # Use 'localhost' for local testing
    IAM_HEADER = os.environ.get("IAM_HEADER", "")
    SAMPLE_VIDEO_DURATION = int(os.environ.get("SAMPLE_VIDEO_DURATION", 10))  # Default to 10 seconds
