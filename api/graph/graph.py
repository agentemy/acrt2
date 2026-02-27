from fastapi import Response, HTTPException
import pandas as pd
import matplotlib.pyplot as plt
import io
from typing import Optional

from api.db.data_extraction import get_nlp_metrics


async def chart(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> Response:

    data = await get_nlp_metrics(individual_number, expedition_id)

    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    df = pd.DataFrame(data)

    # Агрегируем по сессиям
    session_avg = df.groupby('session')[['alpha', 'beta', 'theta']].mean().reset_index()

    session_map = {1: 'утро', 2: 'день', 3: 'вечер'}
    session_avg['Сеанс'] = session_avg['session'].map(session_map)
    session_avg = session_avg.set_index('Сеанс')
    session_avg = session_avg.reindex(['утро', 'день', 'вечер'])

    fig, ax = plt.subplots(figsize=(10, 6))

    session_avg.plot(
        kind='bar',
        ax=ax,
        color=['#4682b4', '#32cd32', '#ff69b4'],
        width=0.75
    )

    # Добавляем значения на столбцы
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3, fontsize=9)

    ax.set_title('Средние значения мозговых волн по времени суток',
                 fontsize=14, pad=15)
    ax.set_xlabel('Время суток', fontsize=12)
    ax.set_ylabel('Средняя амплитуда', fontsize=12)
    ax.legend(['Alpha', 'Beta', 'Theta'], fontsize=11, loc='upper right')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Добавляем информацию об экспедиции если указана
    if expedition_id:
        ax.set_title(f'Экспедиция #{expedition_id} - {ax.get_title()}',
                     fontsize=14, pad=15)

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    return Response(
        content=buf.getvalue(),
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=chart.png"}
    )