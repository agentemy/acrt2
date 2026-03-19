from fastapi import APIRouter

expedition = APIRouter()

@expedition.get("/{expedition_id}/stress")
async def get_expedition_stress_chart(
    expedition_id: int
):
    from graph.charts import create_aggregated_stress_chart
    return await create_aggregated_stress_chart(expedition_id)