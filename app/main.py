from fastapi import FastAPI
from app.routes import patient

app = FastAPI()

app.include_router(patient.router)