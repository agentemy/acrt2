from fastapi import Response
import pandas as pd
import matplotlib.pyplot as plt
import io

from db.data_extraction import get_from_nlp_metrics

async def chart(individual_number):
    data = await get_from_nlp_metrics(individual_number)


    # Преобразуем список словарей в DataFrame
    df = pd.DataFrame(data)

    # Маппинг номеров сессий на названия времени суток
    session_map = {1: 'утро', 2: 'день', 3: 'вечер'}

    # Добавляем колонку с текстовыми названиями и устанавливаем её как индекс
    df['Сеанс'] = df['session'].map(session_map)
    df = df.drop('session', axis=1)           # убираем числовую колонку session
    df = df.set_index('Сеанс')

    # Устанавливаем желаемый порядок (на случай, если данные придут не по порядку)
    df = df.reindex(['утро', 'день', 'вечер'])

    # Строим график
    df.plot(
        kind='bar',
        figsize=(10, 6),
        color=['#4682b4', '#32cd32', '#ff69b4'],
        width=0.75
    )

    plt.title('Средние значения волн по времени суток', fontsize=14, pad=15)
    plt.xlabel('Время суток', fontsize=12)
    plt.ylabel('Средняя амплитуда волн', fontsize=12)
    plt.xticks(rotation=0, fontsize=11)
    plt.yticks(fontsize=11)
    plt.legend(['Alpha', 'Beta', 'Theta'], fontsize=11, loc='upper right')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)

    # Возвращаем как изображение
    return Response(
        content=buf.getvalue(),
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=chart.png"}
    )

