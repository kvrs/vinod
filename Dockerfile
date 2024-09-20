FROM python:3.10-slim
WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
