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
    График 1: Alpha, Beta, Theta волны
    """
    data = await get_nlp_metrics(individual_number, expedition_id)

    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # Alpha волны
    axes[0].plot(df['datetime'], df['alpha'],
                 marker='o', color=COLORS[0], linewidth=2, markersize=4)
    axes[0].fill_between(df['datetime'], df['alpha'], alpha=0.3, color=COLORS[0])
    axes[0].set_ylabel('Alpha', fontsize=11)
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(y=df['alpha'].mean(), color=COLORS[0], linestyle='--', alpha=0.5)

    # Beta волны
    axes[1].plot(df['datetime'], df['beta'],
                 marker='s', color=COLORS[1], linewidth=2, markersize=4)
    axes[1].fill_between(df['datetime'], df['beta'], alpha=0.3, color=COLORS[1])
    axes[1].set_ylabel('Beta', fontsize=11)
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=df['beta'].mean(), color=COLORS[1], linestyle='--', alpha=0.5)

    # Theta волны
    axes[2].plot(df['datetime'], df['theta'],
                 marker='^', color=COLORS[2], linewidth=2, markersize=4)
    axes[2].fill_between(df['datetime'], df['theta'], alpha=0.3, color=COLORS[2])
    axes[2].set_ylabel('Theta', fontsize=11)
    axes[2].set_xlabel('Время', fontsize=11)
    axes[2].grid(True, alpha=0.3)
    axes[2].axhline(y=df['theta'].mean(), color=COLORS[2], linestyle='--', alpha=0.5)

    title = f'Мозговая активность: Alpha, Beta, Theta волны\nУчастник: {individual_number}'
    if expedition_id:
        title = f'Экспедиция #{expedition_id} - {title}'

    plt.suptitle(title, fontsize=14, y=1.02)
    plt.tight_layout()

    return _fig_to_response(fig)


async def create_fatigue_chart(
        individual_number: str,
        expedition_id: Optional[int] = None
) -> Response:
    """
    График 2: Fatigue (утомление) из разных источников
    """
    # Получаем данные из разных таблиц
    physio_data = await get_physiological_metrics(individual_number, expedition_id)
    product_data = await get_productivity_metrics(individual_number, expedition_id)

    if not physio_data and not product_data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    fig, ax = plt.subplots(figsize=(12, 6))

    # Физиологическое утомление
    if physio_data:
        df_physio = pd.DataFrame(physio_data)
        df_physio['datetime'] = pd.to_datetime(df_physio['timestamp'], unit='ms')
        ax.plot(df_physio['datetime'], df_physio['fatigue'],
                marker='o', color=COLORS[0], linewidth=2, markersize=6,
                label='Физиологическое утомление')

    # Утомление из продуктивности
    if product_data:
        df_product = pd.DataFrame(product_data)
        df_product['datetime'] = pd.to_datetime(df_product['timestamp'], unit='ms')
        ax.plot(df_product['datetime'], df_product['fatigue'],
                marker='s', color=COLORS[1], linewidth=2, markersize=6,
                label='Утомление (продуктивность)')

    ax.set_xlabel('Время', fontsize=12)
    ax.set_ylabel('Уровень утомления', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    title = f'Динамика утомления (Fatigue)\nУчастник: {individual_number}'
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
    График 3: Heart Rate (частота сердечных сокращений)
    """
    data = await get_cardio_metrics(individual_number, expedition_id)

    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df['datetime'], df['heart_rate'],
            marker='o', color=COLORS[0], linewidth=2, markersize=6)
    ax.fill_between(df['datetime'], df['heart_rate'], alpha=0.3, color=COLORS[0])

    # Добавляем зоны ЧСС
    ax.axhline(y=60, color='green', linestyle='--', alpha=0.5, label='Норма (60)')
    ax.axhline(y=100, color='red', linestyle='--', alpha=0.5, label='Тахикардия (100)')

    ax.set_xlabel('Время', fontsize=12)
    ax.set_ylabel('ЧСС (уд/мин)', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    # Статистика
    stats_text = f"Среднее: {df['heart_rate'].mean():.1f}\nМин: {df['heart_rate'].min():.1f}\nМакс: {df['heart_rate'].max():.1f}"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    title = f'Частота сердечных сокращений\nУчастник: {individual_number}'
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