from fastapi import Response, HTTPException
import pandas as pd
import matplotlib.pyplot as plt
import io
from typing import Optional
import numpy as np

from db.data_extraction import (
    get_nlp_metrics,
    get_physiological_metrics,
    get_cardio_metrics,
    get_productivity_metrics
)

plt.style.use('seaborn-v0_8-darkgrid')
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

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


def _fig_to_response(fig) -> Response:

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    buf.seek(0)
    plt.close(fig)

    return Response(
        content=buf.getvalue(),
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=chart.png"}
    )


async def create_alpha_beta_theta_chart(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> Response:
    """
    График 1: Alpha, Beta, Theta волны (столбчатая диаграмма по времени суток)
    """
    data = await get_nlp_metrics(individual_number, expedition_id)

    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    df = pd.DataFrame(data)

    # Маппинг номеров сессий на названия времени суток
    session_map = {1: 'утро', 2: 'день', 3: 'вечер'}

    # Добавляем колонку с текстовыми названиями сессий
    df['Сеанс'] = df['session'].map(session_map)

    # Группируем по сеансам и считаем средние
    brain_waves = df.groupby('Сеанс')[['alpha', 'beta', 'theta']].mean()

    # Устанавливаем правильный порядок сеансов
    brain_waves = brain_waves.reindex(['утро', 'день', 'вечер'])

    # Создаем фигуру
    fig, ax = plt.subplots(figsize=(10, 6))

    # Строим столбчатую диаграмму
    brain_waves.plot(
        kind='bar',
        ax=ax,
        color=['#4682b4', '#32cd32', '#ff69b4'],
        width=0.75
    )

    # Настройка графика
    ax.set_title(
        f'Средние значения мозговых волн по времени суток\nУчастник: {individual_number}',
        fontsize=14,
        pad=15
    )
    ax.set_xlabel('Время суток', fontsize=12)
    ax.set_ylabel('Средняя амплитуда волн', fontsize=12)
    ax.set_xticklabels(['Утро', 'День', 'Вечер'], rotation=0, fontsize=11)
    ax.legend(['Alpha', 'Beta', 'Theta'], fontsize=11, loc='upper right')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Добавляем значения на столбцы
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f', padding=3, fontsize=9)

    # Добавляем информацию об экспедиции если есть
    if expedition_id:
        ax.text(
            0.02, 0.98,
            f'Экспедиция: {expedition_id}',
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
        )

    plt.tight_layout()

    return _fig_to_response(fig)


async def create_fatigue_chart(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> Response:
    """
    График 2: Fatigue (утомление) по времени суток
    """
    # Получаем данные из разных таблиц
    physio_data = await get_physiological_metrics(individual_number, expedition_id)
    product_data = await get_productivity_metrics(individual_number, expedition_id)

    if not physio_data and not product_data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    # Маппинг номеров сессий на названия времени суток
    session_map = {1: 'утро', 2: 'день', 3: 'вечер'}

    fig, ax = plt.subplots(figsize=(10, 6))

    # Физиологическое утомление
    if physio_data:
        df_physio = pd.DataFrame(physio_data)
        df_physio['Сеанс'] = df_physio['session'].map(session_map)

        # Группируем по сеансам и считаем средние
        physio_fatigue = df_physio.groupby('Сеанс')['fatigue'].mean()
        physio_fatigue = physio_fatigue.reindex(['утро', 'день', 'вечер'])

        # Строим график
        ax.plot(physio_fatigue.index, physio_fatigue.values,
                marker='o', color='#1e90ff', linewidth=2, markersize=8,
                label='Физиологическое утомление')

        # Добавляем значения
        for i, (idx, val) in enumerate(physio_fatigue.items()):
            if pd.notna(val):
                ax.text(i, val + 0.02, f'{val:.2f}',
                        ha='center', va='bottom', fontsize=10)

    # Утомление из продуктивности
    if product_data:
        df_product = pd.DataFrame(product_data)
        df_product['Сеанс'] = df_product['session'].map(session_map)

        # Группируем по сеансам и считаем средние
        product_fatigue = df_product.groupby('Сеанс')['fatigue'].mean()
        product_fatigue = product_fatigue.reindex(['утро', 'день', 'вечер'])

        # Строим график
        ax.plot(product_fatigue.index, product_fatigue.values,
                marker='s', color='#ff6347', linewidth=2, markersize=8,
                label='Утомление (продуктивность)')

        # Добавляем значения
        for i, (idx, val) in enumerate(product_fatigue.items()):
            if pd.notna(val):
                ax.text(i, val + 0.02, f'{val:.2f}',
                        ha='center', va='bottom', fontsize=10, color='#ff6347')

    # Настройка графика
    ax.set_xlabel('Время суток', fontsize=12)
    ax.set_ylabel('Средний уровень утомления', fontsize=12)
    ax.set_ylim(0, 1)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)

    ax.axhline(y=0.7, color='red', linestyle='--', alpha=0.5, label='Критический уровень (0.7)')

    title = f'Динамика утомления по времени суток\nУчастник: {individual_number}'
    if expedition_id:
        title = f'Экспедиция #{expedition_id} - {title}'

    ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()

    return _fig_to_response(fig)


async def create_heart_rate_chart(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> Response:
    """
    График 3: Heart Rate (частота сердечных сокращений) по времени суток
    """
    data = await get_cardio_metrics(individual_number, expedition_id)

    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    df = pd.DataFrame(data)

    # Маппинг номеров сессий на названия времени суток
    session_map = {1: 'утро', 2: 'день', 3: 'вечер'}

    # Добавляем колонку с названиями сеансов
    df['Сеанс'] = df['session'].map(session_map)

    # Группируем по сеансам и считаем средние
    hr_by_session = df.groupby('Сеанс')['heart_rate'].mean()
    hr_by_session = hr_by_session.reindex(['утро', 'день', 'вечер'])

    # Строим график
    fig, ax = plt.subplots(figsize=(10, 6))

    # Основная линия
    line = ax.plot(hr_by_session.index, hr_by_session.values,
                   marker='o', color='#1e90ff', linewidth=2, markersize=10,
                   label='Средняя ЧСС')[0]

    # Добавляем значения
    for i, (idx, val) in enumerate(hr_by_session.items()):
        if pd.notna(val):
            ax.text(i, val + 2, f'{val:.0f}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Зоны ЧСС - располагаем легенды в разных местах
    norm_line = ax.axhline(y=60, color='green', linestyle='--', alpha=0.7, linewidth=1.5,
                           label='Нижняя граница нормы (60)')

    upper_norm_line = ax.axhline(y=80, color='orange', linestyle='--', alpha=0.7, linewidth=1.5,
                                 label='Верхняя граница нормы (80)')

    tachy_line = ax.axhline(y=100, color='red', linestyle='--', alpha=0.7, linewidth=1.5,
                            label='Тахикардия (100)')

    # Настройка осей
    ax.set_xlabel('Время суток', fontsize=12)
    ax.set_ylabel('Средняя ЧСС (уд/мин)', fontsize=12)
    ax.set_xticklabels(['Утро', 'День', 'Вечер'], fontsize=11)
    ax.grid(True, alpha=0.3)

    # РАСПОЛАГАЕМ ЛЕГЕНДЫ В РАЗНЫХ МЕСТАХ
    # Легенда для основной линии - вверху слева
    first_legend = ax.legend(handles=[line], loc='upper left', fontsize=10, framealpha=0.9)
    ax.add_artist(first_legend)

    # Легенда для норм - внизу слева
    ax.legend(handles=[norm_line, upper_norm_line, tachy_line],
              loc='lower left', fontsize=9, framealpha=0.9,
              title='Зоны ЧСС', title_fontsize=10)

    # Статистика - вверху справа
    stats_text = (
        f"Среднее: {hr_by_session.mean():.1f}\n"
        f"Мин: {df['heart_rate'].min():.1f}\n"
        f"Макс: {df['heart_rate'].max():.1f}"
    )

    ax.text(0.98, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    title = f'Частота сердечных сокращений по времени суток\nУчастник: {individual_number}'
    if expedition_id:
        title = f'Экспедиция #{expedition_id} - {title}'

    ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()

    return _fig_to_response(fig)


async def create_psychological_fatigue_chart(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> Response:
    """
    График 4: Psychological Metrics Fatigue
    """
    data = await get_physiological_metrics(individual_number, expedition_id)

    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df['datetime'], df['fatigue'],
            marker='o', color=COLORS[0], linewidth=2, markersize=6,
            label='Психологическое утомление')
    ax.fill_between(df['datetime'], df['fatigue'], alpha=0.3, color=COLORS[0])

    # Добавляем для сравнения другие метрики
    if 'stress' in df.columns:
        ax.plot(df['datetime'], df['stress'],
                marker='s', color=COLORS[1], linewidth=2, markersize=6,
                label='Стресс', alpha=0.7)

    ax.set_xlabel('Время', fontsize=12)
    ax.set_ylabel('Уровень', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    title = f'Психологическое утомление\nУчастник: {individual_number}'
    if expedition_id:
        title = f'Экспедиция #{expedition_id} - {title}'

    ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()

    return _fig_to_response(fig)


async def create_gravity_chart(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> Response:
    """
    График 5: Gravity (гравитация/вес?)
    """
    data = await get_productivity_metrics(individual_number, expedition_id)

    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df['datetime'], df['gravity'],
            marker='o', color=COLORS[0], linewidth=2, markersize=6)
    ax.fill_between(df['datetime'], df['gravity'], alpha=0.3, color=COLORS[0])

    ax.set_xlabel('Время', fontsize=12)
    ax.set_ylabel('Gravity', fontsize=12)
    ax.grid(True, alpha=0.3)

    title = f'Gravity метрика\nУчастник: {individual_number}'
    if expedition_id:
        title = f'Экспедиция #{expedition_id} - {title}'

    ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()

    return _fig_to_response(fig)


async def create_concentration_chart(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> Response:
    """
    График 6: Concentration (концентрация) из разных источников
    """
    # Получаем данные из разных таблиц
    physio_data = await get_physiological_metrics(individual_number, expedition_id)
    product_data = await get_productivity_metrics(individual_number, expedition_id)

    if not physio_data and not product_data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    fig, ax = plt.subplots(figsize=(12, 6))

    if physio_data:
        df_physio = pd.DataFrame(physio_data)
        df_physio['datetime'] = pd.to_datetime(df_physio['timestamp'], unit='ms')
        ax.plot(df_physio['datetime'], df_physio['concentration'],
                marker='o', color=COLORS[0], linewidth=2, markersize=6,
                label='Концентрация (физиологическая)')

    if product_data:
        df_product = pd.DataFrame(product_data)
        df_product['datetime'] = pd.to_datetime(df_product['timestamp'], unit='ms')
        ax.plot(df_product['datetime'], df_product['concentration'],
                marker='s', color=COLORS[1], linewidth=2, markersize=6,
                label='Концентрация (продуктивность)')

    ax.set_xlabel('Время', fontsize=12)
    ax.set_ylabel('Уровень концентрации', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    title = f'Динамика концентрации\nУчастник: {individual_number}'
    if expedition_id:
        title = f'Экспедиция #{expedition_id} - {title}'

    ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()

    return _fig_to_response(fig)


async def create_relaxation_chart(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> Response:
    """
    График 7: Relaxation (расслабление) из разных источников
    """
    # Получаем данные из разных таблиц
    physio_data = await get_physiological_metrics(individual_number, expedition_id)
    product_data = await get_productivity_metrics(individual_number, expedition_id)

    if not physio_data and not product_data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    fig, ax = plt.subplots(figsize=(12, 6))

    if physio_data:
        df_physio = pd.DataFrame(physio_data)
        df_physio['datetime'] = pd.to_datetime(df_physio['timestamp'], unit='ms')
        ax.plot(df_physio['datetime'], df_physio['relax'],
                marker='o', color=COLORS[0], linewidth=2, markersize=6,
                label='Расслабление (физиологическое)')

    if product_data:
        df_product = pd.DataFrame(product_data)
        df_product['datetime'] = pd.to_datetime(df_product['timestamp'], unit='ms')
        ax.plot(df_product['datetime'], df_product['relaxation'],
                marker='s', color=COLORS[1], linewidth=2, markersize=6,
                label='Расслабление (продуктивность)')

    ax.set_xlabel('Время', fontsize=12)
    ax.set_ylabel('Уровень расслабления', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    title = f'Динамика расслабления\nУчастник: {individual_number}'
    if expedition_id:
        title = f'Экспедиция #{expedition_id} - {title}'

    ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()

    return _fig_to_response(fig)