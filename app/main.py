import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import analyzer, auth
from app.core.firebase import init_firebase

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize Firebase on startup
init_firebase()

app = FastAPI(
    title="Chinese App API",
    description="Backend API for the Chinese Learning App using Firebase and HanLP",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception on %s %s\n%s",
        request.method,
        request.url,
        traceback.format_exc(),
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(analyzer.router, prefix="/api", tags=["Text Analysis"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Chinese App API. Go to /docs for the API documentation."}
