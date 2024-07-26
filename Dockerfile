# Use a specific Python version to ensure consistency
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update -qq && \
    apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install -U -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Use a non-root user (optional for better security)
# RUN useradd -ms /bin/sh appuser
# USER appuser

# Start the Flask app with Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "bot.app:app"]
