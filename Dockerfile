# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port that your Flask app will run on
EXPOSE 8000

# Define the command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "bot.web:app"]
