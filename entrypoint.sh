#!/bin/bash

# Start Flask server
gunicorn -b 0.0.0.0:8000 bot.web:app &

# Start Pyrogram bot
python bot/sample_video_bot.py
