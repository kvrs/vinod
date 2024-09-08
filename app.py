from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Enable logging
logging.basicConfig(level=logging.INFO)

# Trigger GCP Cloud Build function
def trigger_cloud_build(git_url, usr_id, job_id, project_id, branch_name="main"):
    try:
        from google.cloud.devtools import cloudbuild_v1
        from google.protobuf import duration_pb2

        client = cloudbuild_v1.CloudBuildClient()
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
        return operation.result()
    except Exception as e:
        logging.error(f"Error during Cloud Build: {str(e)}")
        raise e

# API route to handle front-end requests
@app.route('/trigger-build', methods=['POST'])
def trigger_build():
    try:
        data = request.get_json()

        # Log the incoming data
        logging.info(f"Received data: {data}")

        git_url = data.get('git_url')
        usr_id = data.get('usr_id')
        job_id = data.get('job_id')

        # Project ID from GCP
        project_id = "your-gcp-project-id"

        # Trigger the build
        result = trigger_cloud_build(git_url, usr_id, job_id, project_id)

        return jsonify({"message": "Build triggered successfully", "build_result": str(result)})
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
