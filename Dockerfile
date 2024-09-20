# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8080  # Change this to 8080
ENV PYTHONUNBUFFERED=1

# Run the application on port 8080
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
