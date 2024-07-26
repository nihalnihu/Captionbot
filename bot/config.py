import os

class Config:
    API_ID = int(os.environ.get("API_ID", "25731065"))
    API_HASH = os.environ.get("API_HASH", "be534fb5a5afd8c3308c9ca92afde672")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7213907869:AAFsNNoro8CcZSM1hkh_-a6-R41U3pqC6lA")
    SESSION_NAME = os.environ.get("SESSION_NAME", "my_bot")
    HOST = os.environ.get("HOST", "localhost")  # Use 'localhost' for local testing
    IAM_HEADER = os.environ.get("IAM_HEADER", "")
    SAMPLE_VIDEO_DURATION = int(os.environ.get("SAMPLE_VIDEO_DURATION", 10))  # Default to 10 seconds
