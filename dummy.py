from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud.devtools import cloudbuild_v1

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def trigger_cloud_build(project_id, trigger_id, user_id, job_id, file_path):
    client = cloudbuild_v1.CloudBuildClient()

    # Prepare the RunBuildTriggerRequest with substitutions
    build_trigger_request = cloudbuild_v1.RunBuildTriggerRequest(
        project_id=project_id,
        trigger_id=trigger_id,
        substitutions={
            '_USER_ID': user_id,
            '_JOB_ID': job_id,
            '_FILE_PATH': file_path
        }
    )

    # Execute the trigger
    operation = client.run_build_trigger(request=build_trigger_request)
    response = operation.result()

    print(f"Build triggered: {response.id}")
    return response

@app.route('/trigger-build', methods=['POST'])
def trigger_build():
    data = request.json
    project_id = data.get('project_id')
    trigger_id = data.get('trigger_id')
    user_id = data.get('user_id')
    job_id = data.get('job_id')
    file_path = data.get('file_path')

    # Check for missing parameters
    if not all([project_id, trigger_id, user_id, job_id, file_path]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        response = trigger_cloud_build(project_id, trigger_id, user_id, job_id, file_path)
        return jsonify({"message": f"Build triggered: {response.id}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
