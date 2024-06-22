# Use an official Python runtime as the base image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# install cron
RUN apt-get update && \
    apt-get install -y cron

# Copy the rest of the application code into the container
COPY . .

# Give execution rights to the script
RUN chmod +x /app/riddle_update.py

# Add the cron job
RUN echo "0 0 * * * /usr/local/bin/python /app/riddle_update.py >> /tmp/cronlog 2>&1" > /etc/cron.d/riddle-update-job

# Apply the cron job
RUN crontab /etc/cron.d/riddle-update-job

# Expose the port your app runs on
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=webapp.py
ENV PYTHONUNBUFFERED=1

# Ensure the cron service is started when the container starts
# and run the Flask app as well
CMD cron && flask run --host=0.0.0.0