from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import init_models, async_engine
from graph.graph import chart

@asynccontextmanager
async def lifespan(app):
    init_models()
    yield
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def func():
    return {"Hello": "World"}

@app.get("/metrics/{ind_num}")
async def metrics(ind_num: str):
    return await chart(ind_num)
