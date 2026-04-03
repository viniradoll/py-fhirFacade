from fastapi import FastAPI, Depends
from app.middleware.auth import validate_api_key
import app.routes as routes

app = FastAPI(dependencies=[Depends(validate_api_key)])

app.include_router(routes.patient)