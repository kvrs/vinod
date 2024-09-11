import sys
import logging
from google.cloud.devtools import cloudbuild_v1
from google.protobuf import duration_pb2

# Enable logging
logging.basicConfig(level=logging.INFO)

def trigger_cloud_build(git_url, usr_id, job_id, project_id, branch_name="main"):
    try:
        client = cloudbuild_v1.CloudBuildClient()

        # Prepare the Cloud Build config
        build = {
            "steps": [
                {
                    "name": "gcr.io/cloud-builders/git",
                    "args": ["clone", git_url]
                },
                {
                    "name": "gcr.io/cloud-builders/docker",
                    "args": ["build", "-t", f"gcr.io/{project_id}/{job_id}:latest", "."]
                }
            ],
            "timeout": duration_pb2.Duration(seconds=600),
            "source": {
                "repo_source": {
                    "project_id": project_id,
                    "repo_name": git_url.split("/")[-1].replace(".git", ""),
                    "branch_name": branch_name
                }
            }
        }

        # Start the build
        operation = client.create_build(project_id=project_id, build=build)
        result = operation.result()

        logging.info(f"Build triggered successfully for {git_url}")
        return result
    except Exception as e:
        logging.error(f"Error during Cloud Build: {str(e)}")
        raise

if __name__ == "__main__":
    # Parse command-line arguments passed from the Flask API
    if len(sys.argv) != 4:
        print("Usage: trigger_cloud_build.py <git_url> <usr_id> <job_id>")
        sys.exit(1)

    git_url = sys.argv[1]
    usr_id = sys.argv[2]
    job_id = sys.argv[3]

    # Set your GCP project ID
    project_id = "your-gcp-project-id"

    # Trigger the Cloud Build with the values provided
    trigger_cloud_build(git_url, usr_id, job_id, project_id)
