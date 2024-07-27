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

# Make entrypoint.sh executable
RUN chmod +x entrypoint.sh

# Expose the port that your Flask app will run on
EXPOSE 8000

# Define the command to run the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
