if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    service_dir = Path(__file__).resolve().parent.parent
    project_dir = service_dir.parent.parent
    sys.path[:0] = [str(service_dir), str(project_dir)]

from fastapi import FastAPI

from app.api.routes import booking_routes

app = FastAPI(
    title="Last Mile Service Booking API",
    description="APIs for booking field engineer services",
    version="1.0.0"
)


app.include_router(
    booking_routes.router,
    prefix="/api"
)


@app.get("/health")
def health_check():

    return {
        "status": "success",
        "message": "Service Booking Service is running"
    }