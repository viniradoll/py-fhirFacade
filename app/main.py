from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from db.connection import init_pool, close_pool
from middleware.auth import validate_api_key
from engine.loader import load_all_mappers
from engine.registry import registered_resources
from routes.fhir import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    load_all_mappers()
    print(f"Mappers carregados: {registered_resources()}")
    yield
    close_pool()

app = FastAPI(title="FHIR Facade", lifespan=lifespan, dependencies=[Depends(validate_api_key)])
app.include_router(router)