from google.cloud.devtools import cloudbuild_v1
from google.protobuf import timestamp_pb2

def trigger_cloud_build(project_id, branch_name, trigger_id, substitutions=None):
    # Initialize the Cloud Build client
    client = cloudbuild_v1.CloudBuildClient()

    # Prepare the source with branch name
    repo_source = cloudbuild_v1.RepoSource(
        branch_name=branch_name
    )

    # Set substitutions in build parameters if provided
    build_trigger_request = cloudbuild_v1.RunBuildTriggerRequest(
        project_id=project_id,
        trigger_id=trigger_id,
        source=repo_source
    )

    # Trigger the build
    operation = client.run_build_trigger(request=build_trigger_request)

    # Wait for the operation to complete
    response = operation.result()

    print(f"Build triggered: {response.id}")
    return response

if __name__ == "__main__":
    # Your project ID, branch name, and trigger ID
    project_id = "cloud-run-job-435501"
    branch_name = "main"
    trigger_id = "6869d783-b517-4393-b645-eb85a7ff494d"

    # Call the function to trigger the build
    trigger_cloud_build(project_id, branch_name, trigger_id)

