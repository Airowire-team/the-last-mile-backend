
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app import create_app
from app.scripts.schedular import schedule_jobs
from app.utils.geoip_utils import ensure_geoip_database

# Ensure required resources are present
ensure_geoip_database()

# Create FastAPI application
app = create_app()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    schedule_jobs(app)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
