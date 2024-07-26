# Use a specific Python version to ensure consistency
FROM python:3.12-slim

# Install ffmpeg
RUN apt-get update -qq && apt-get -y install ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy the application code
COPY . .

# Install Python dependencies
RUN pip install -U -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Start the Flask app with Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "bot.app:app"]
