from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Enable logging
logging.basicConfig(level=logging.INFO)

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

        # Log received values for debugging purposes
        logging.info(f"git_url: {git_url}, usr_id: {usr_id}, job_id: {job_id}")

        # Return success response without triggering any external action
        return jsonify({"message": "Received successfully", "git_url": git_url, "usr_id": usr_id, "job_id": job_id})
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"message": "Error occurred", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
