from fastapi import APIRouter

from giga_chat.giga import chat
from db.data_extraction import (
    get_nlp_metrics,
    get_physiological_metrics,
    get_cardio_metrics,
    get_productivity_metrics
)
gigachat_router = APIRouter()

@gigachat_router.get("/advices/{ind_num}/{expedition_id}")
async def giga(ind_num: str,
               expedition_id: int):
    nlp_metrics = await get_nlp_metrics(ind_num, expedition_id)
    physiological_metrics = await get_physiological_metrics(ind_num, expedition_id)
    cardio_metrics = await get_cardio_metrics(ind_num, expedition_id)
    productivity_metrics = await get_productivity_metrics(ind_num, expedition_id)
    response = chat(nlp_metrics, physiological_metrics, cardio_metrics, productivity_metrics)
    return {"response": response.choices[0].message.content}