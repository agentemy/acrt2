from sqlalchemy import select
from typing import List, Dict, Any

from .database import Base
from .database import async_session_maker

async def get_from_nlp_metrics(
    individual_number: str,
) -> List[Dict[str, Any]]:
    async with async_session_maker() as session:
        NlpMetrics = Base.classes.nlp_metrics

        async with async_session_maker() as session:
            result = await session.scalars(
                select(NlpMetrics)
                .where(NlpMetrics.individual_number == individual_number)
            )

            rows = result.all()

            return [
                {
                    'session': r.session,
                    'avg_alpha': r.alpha,
                    'avg_beta': r.beta,
                    'avg_theta': r.theta
                }
                for r in rows
            ]


async def get_from_physical_metrics(
    individual_number: str,
) -> List[Dict[str, Any]]:
    pass