from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from typing import Optional

from db.database import init_models, async_engine
from graph.charts import (
    chart,
    create_alpha_beta_theta_chart,
    create_fatigue_chart,
    create_heart_rate_chart,
    create_psychological_fatigue_chart,
    create_gravity_chart,
    create_concentration_chart,
    create_relaxation_chart
)

@asynccontextmanager
async def lifespan(app):
    init_models()
    yield
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {
        "message": "Arctic Analytics Service",
        "endpoints": {
            "Базовые": {
                "/health": "Проверка здоровья сервиса"
            },
            "Графики по участнику": {
                "/metrics/alpha-beta-theta/{ind_num}": "Alpha, Beta, Theta волны",
                "/metrics/fatigue/{ind_num}": "Утомление (Fatigue)",
                "/metrics/heart-rate/{ind_num}": "Частота сердечных сокращений",
                "/metrics/psychological-fatigue/{ind_num}": "Психологическое утомление",
                "/metrics/gravity/{ind_num}": "Gravity метрика",
                "/metrics/concentration/{ind_num}": "Концентрация",
                "/metrics/relaxation/{ind_num}": "Расслабление"
            },
            "Агрегированные": {
                "/expedition/{expedition_id}/stress": "Стресс по экспедиции"
            }
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Индивидуальные графики
@app.get("/metrics/alpha-beta-theta/{ind_num}/{expedition_id}")
async def get_alpha_beta_theta_chart(
    ind_num: str,
    expedition_id: int
):
    """График мозговой активности: Alpha, Beta, Theta волны"""
    return await create_alpha_beta_theta_chart(ind_num, expedition_id)

@app.get("/metrics/fatigue/{ind_num}")
async def get_fatigue_chart(
    ind_num: str,
    expedition_id: Optional[int] = Query(None, description="ID экспедиции")
):
    """График утомления (Fatigue)"""
    return await create_fatigue_chart(ind_num, expedition_id)

@app.get("/metrics/heart-rate/{ind_num}")
async def get_heart_rate_chart(
    ind_num: str,
    expedition_id: Optional[int] = Query(None, description="ID экспедиции")
):
    """График частоты сердечных сокращений"""
    return await create_heart_rate_chart(ind_num, expedition_id)

@app.get("/metrics/psychological-fatigue/{ind_num}")
async def get_psychological_fatigue_chart(
    ind_num: str,
    expedition_id: Optional[int] = Query(None, description="ID экспедиции")
):
    """График психологического утомления"""
    return await create_psychological_fatigue_chart(ind_num, expedition_id)

@app.get("/metrics/gravity/{ind_num}")
async def get_gravity_chart(
    ind_num: str,
    expedition_id: Optional[int] = Query(None, description="ID экспедиции")
):
    """График Gravity метрики"""
    return await create_gravity_chart(ind_num, expedition_id)

@app.get("/metrics/concentration/{ind_num}")
async def get_concentration_chart(
    ind_num: str,
    expedition_id: Optional[int] = Query(None, description="ID экспедиции")
):
    """График концентрации"""
    return await create_concentration_chart(ind_num, expedition_id)

@app.get("/metrics/relaxation/{ind_num}")
async def get_relaxation_chart(
    ind_num: str,
    expedition_id: Optional[int] = Query(None, description="ID экспедиции")
):
    """График расслабления"""
    return await create_relaxation_chart(ind_num, expedition_id)

# Для обратной совместимости
@app.get("/metrics/nlp/{ind_num}")
async def get_nlp_chart(
    ind_num: str,
    expedition_id: Optional[int] = Query(None, description="ID экспедиции")
):
    """График мозговой активности (для обратной совместимости)"""
    return await chart(ind_num, expedition_id)

@app.get("/expedition/{expedition_id}/stress")
async def get_expedition_stress_chart(
    expedition_id: int
):
    """Агрегированный график стресса для всей экспедиции"""
    # Здесь можно добавить агрегированный график
    from graph.charts import create_aggregated_stress_chart
    return await create_aggregated_stress_chart(expedition_id)