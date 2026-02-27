from fastapi import FastAPI, Query
from contextlib import asynccontextmanager

from db.database import init_models, async_engine
from routes.metrics import metrics
from routes.expedition import expedition
from routes.gigachat_routes import gigachat_router

@asynccontextmanager
async def lifespan(app):
    init_models()
    yield
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(metrics, prefix="/metrics")
app.include_router(expedition, prefix="/expedition")
app.include_router(gigachat_router, prefix="/giga")


@app.get("/")
async def root():
    return {
        "message": "Arctic Analytics Service",
        "endpoints": {
            "Базовые": {
                "/health": "Проверка здоровья сервиса"
            },
            "Графики по участнику": {
                "/metrics/alpha-beta-theta/{ind_num}/{expedition_id}": "Alpha, Beta, Theta волны",
                "/metrics/fatigue/{ind_num}/{expedition_id}": "Утомление (Fatigue)",
                "/metrics/heart-rate/{ind_num}/{expedition_id}": "Частота сердечных сокращений",
                "/metrics/psychological-fatigue/{ind_num}/{expedition_id}": "Психологическое утомление",
                "/metrics/gravity/{ind_num}/{expedition_id}": "Gravity метрика",
                "/metrics/concentration/{ind_num}/{expedition_id}": "Концентрация",
                "/metrics/relaxation/{ind_num}/{expedition_id}": "Расслабление"
            },
            "Агрегированные": {
                "/expedition/{expedition_id}/stress": "Стресс по экспедиции"
            }
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}