# # Use an official Python runtime as a base image
# FROM python:3.10-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install dependencies
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Expose the port Flask will run on
# EXPOSE 8080

# # Command to run the Flask app
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
FROM python:3.12-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install -r requirements.txt
RUN pip install Flask gunicorn\
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
