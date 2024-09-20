from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud.devtools import cloudbuild_v1

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def trigger_cloud_build(project_id, branch_name, trigger_id, user_id=None,job_id=None, file_path=None, substitutions=None):
    client = cloudbuild_v1.CloudBuildClient()
    repo_source = cloudbuild_v1.RepoSource(branch_name=branch_name)
    build_trigger_request = cloudbuild_v1.RunBuildTriggerRequest(
        project_id=project_id,
        trigger_id=trigger_id,
        source=repo_source
    )
    
    # Print the user_id for logging purposes (you can use it as needed)
    print(f"Build triggered by user: {user_id}")
    print(f"Build triggered by job id: {job_id}")
    print(f"Build triggered by file path : {file_path}")

    operation = client.run_build_trigger(request=build_trigger_request)
    response = operation.result()

    print(f"Build triggered: {response.id}")
    return response

@app.route('/trigger-build', methods=['POST'])
def trigger_build():
    data = request.json
    project_id = data.get('project_id')
    branch_name = data.get('branch_name')
    trigger_id = data.get('trigger_id')
    user_id = data.get('user_id')  # Capture user_id from the request
    job_id = data.get('job_id')  # Capture user_id from the request
    file_path = data.get('file_path')  # Capture user_id from the request
    
    if not project_id or not branch_name or not trigger_id:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        response = trigger_cloud_build(project_id, branch_name, trigger_id, user_id=user_id,job_id=job_id,file_path=file_path)
        return jsonify({"message": f"Build triggered: {response.id}", "user_id": user_id, "job_id": job_id, "file_path": file_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
