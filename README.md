## Build the Docker Image:
docker build -t your-image-name .
## Push the Docker Image to Google Container Registry:

gcloud auth configure-docker

docker tag your-image-name gcr.io/your-project-id/your-image-name

docker push gcr.io/your-project-id/your-image-name



