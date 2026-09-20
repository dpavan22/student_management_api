from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers.students import router as student_router
from app.config import settings
from app import models
from app.database import engine , Base
from app.utils.docs import setup_swagger_ui
from app.utils.logger import logger
import time 
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title= settings.PROJECT_NAME)
app.include_router(student_router)
setup_swagger_ui(app)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials= True,
                   allow_methods=['*'],
                   allow_headers=['*'])

@app.middleware("http")
async def incoming_request(request : Request , call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    logger.info(f"{request.method} | {request.url.path} | Status:{response.status_code} | Completion_time: {process_time:.4f}s")
    return response

@app.exception_handler(Exception)
async def error_handler(request : Request, exc : Exception):
    logger.error(f"Unhandled error: {exc}")
    error_content = {"error" : "Internal Server Error", "message" : "An unexpected error occured."}
    return JSONResponse(status_code=500, content=error_content)

@app.get('/', tags=['INFO'])
def root():
    return {
        'project_name': settings.PROJECT_NAME,
        'status' : 'online'
    }

@app.get('/health', tags=["INFO"])
def health_check():
    return {
        'status' : 'healthy',
        'debug_mode' : settings.DEBUG
    }
    


