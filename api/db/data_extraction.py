from sqlalchemy import select, and_
from typing import List, Dict, Any, Optional
from .database import Base, async_session_maker


async def get_nlp_metrics(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> List[Dict[str, Any]]:

    async with async_session_maker() as session:
        NlpMetrics = Base.classes.nlp_metrics

        query = select(NlpMetrics).where(
            NlpMetrics.individual_number == individual_number
        )

        if expedition_id:
            query = query.where(NlpMetrics.expedition_id == expedition_id)

        query = query.order_by(NlpMetrics.timestamp)

        result = await session.execute(query)
        rows = result.scalars().all()

        return [
            {
                'session': r.session,
                'timestamp': r.timestamp,
                'alpha': r.alpha,
                'beta': r.beta,
                'theta': r.theta,
                'delta': r.delta,
                'smr': r.smr,
                'expedition_id': r.expedition_id
            }
            for r in rows
        ]


async def get_physiological_metrics(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Получение физиологических метрик (fatigue, relax, concentration, stress)
    """
    async with async_session_maker() as session:
        PhysiologicalMetrics = Base.classes.physiological_metrics

        query = select(PhysiologicalMetrics).where(
            PhysiologicalMetrics.individual_number == individual_number
        )

        if expedition_id:
            query = query.where(PhysiologicalMetrics.expedition_id == expedition_id)

        query = query.order_by(PhysiologicalMetrics.timestamp)

        result = await session.execute(query)
        rows = result.scalars().all()

        return [
            {
                'session': r.session,
                'timestamp': r.timestamp,
                'relax': r.relax,
                'fatigue': r.fatigue,
                'concentration': r.concentration,
                'stress': r.stress,
                'involvement': r.involvement,
                'expedition_id': r.expedition_id
            }
            for r in rows
        ]


async def get_cardio_metrics(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Получение кардио метрик (heart_rate, stress_index)
    """
    async with async_session_maker() as session:
        CardioMetrics = Base.classes.cardio_metrics

        query = select(CardioMetrics).where(
            CardioMetrics.individual_number == individual_number
        )

        if expedition_id:
            query = query.where(CardioMetrics.expedition_id == expedition_id)

        query = query.order_by(CardioMetrics.timestamp)

        result = await session.execute(query)
        rows = result.scalars().all()

        return [
            {
                'session': r.session,
                'timestamp': r.timestamp,
                'heart_rate': r.heart_rate,
                'stress_index': r.stress_index,
                'kaplan_index': r.kaplan_index,
                'expedition_id': r.expedition_id
            }
            for r in rows
        ]


async def get_productivity_metrics(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Получение метрик продуктивности (gravity, productivity, fatigue, concentration, relaxation)
    """
    async with async_session_maker() as session:
        ProductivityMetrics = Base.classes.productivity_metrics

        query = select(ProductivityMetrics).where(
            ProductivityMetrics.individual_number == individual_number
        )

        if expedition_id:
            query = query.where(ProductivityMetrics.expedition_id == expedition_id)

        query = query.order_by(ProductivityMetrics.timestamp)

        result = await session.execute(query)
        rows = result.scalars().all()

        return [
            {
                'session': r.session,
                'timestamp': r.timestamp,
                'gravity': r.gravity,
                'productivity': r.productivity,
                'fatigue': r.fatigue,
                'concentration': r.concentration,
                'relaxation': r.relaxation,
                'expedition_id': r.expedition_id
            }
            for r in rows
        ]