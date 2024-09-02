#
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend's domain if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobRequest(BaseModel):
    user_id: str
    job_id: str
    git_repo: str

@app.post("/submit-job/")
async def submit_job(request: JobRequest):
    return {
        "status": "Job submitted successfully",
        "user_id": request.user_id,
        "job_id": request.job_id,
        "git_repo": request.git_repo
    }

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application with Uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8000)
