from fastapi import APIRouter


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

metrics = APIRouter()

# Индивидуальные графики
@metrics.get("/alpha-beta-theta/{ind_num}/{expedition_id}")
async def get_alpha_beta_theta_chart(
    ind_num: str,
    expedition_id: int
):
    """График мозговой активности: Alpha, Beta, Theta волны"""
    return await create_alpha_beta_theta_chart(ind_num, expedition_id)

@metrics.get("/fatigue/{ind_num}/{expedition_id}")
async def get_fatigue_chart(
    ind_num: str,
    expedition_id: int
):
    """График утомления (Fatigue)"""
    return await create_fatigue_chart(ind_num, expedition_id)

@metrics.get("/heart-rate/{ind_num}/{expedition_id}")
async def get_heart_rate_chart(
    ind_num: str,
    expedition_id: int
):
    """График частоты сердечных сокращений"""
    return await create_heart_rate_chart(ind_num, expedition_id)

@metrics.get("/psychological-fatigue/{ind_num}/{expedition_id}")
async def get_psychological_fatigue_chart(
    ind_num: str,
    expedition_id: int
):
    """График психологического утомления"""
    return await create_psychological_fatigue_chart(ind_num, expedition_id)

@metrics.get("/gravity/{ind_num}/{expedition_id}")
async def get_gravity_chart(
    ind_num: str,
    expedition_id: int
):
    """График Gravity метрики"""
    return await create_gravity_chart(ind_num, expedition_id)

@metrics.get("/concentration/{ind_num}/{expedition_id}")
async def get_concentration_chart(
    ind_num: str,
    expedition_id: int
):
    """График концентрации"""
    return await create_concentration_chart(ind_num, expedition_id)

@metrics.get("/relaxation/{ind_num}/expedition_id}")
async def get_relaxation_chart(
    ind_num: str,
    expedition_id: int
):
    """График расслабления"""
    return await create_relaxation_chart(ind_num, expedition_id)

# Для обратной совместимости
@metrics.get("/nlp/{ind_num}/{expedition_id}")
async def get_nlp_chart(
    ind_num: str,
    expedition_id: int
):
    """График мозговой активности (для обратной совместимости)"""
    return await chart(ind_num, expedition_id)