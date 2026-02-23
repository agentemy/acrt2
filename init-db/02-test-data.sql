-- =============================================================================
-- 1. Пользователи (users)
-- =============================================================================
INSERT INTO users (first_name, last_name, email, password_hash, individual_number)
VALUES
    ('Алексей',    'Иванов',     'alex.ivanov@example.com',    'pbkdf2:sha256:600000$abc$...', 'IND-000001'),
    ('Мария',      'Петрова',    'maria.petrova@example.com',  'pbkdf2:sha256:600000$def$...', 'IND-000002'),
    ('Дмитрий',    'Соколов',    'dmitry.sokolov@example.com', 'pbkdf2:sha256:600000$ghi$...', 'IND-000003'),
    ('Екатерина',  'Кузнецова',  'ekaterina.k@example.com',    'pbkdf2:sha256:600000$jkl$...', 'IND-000004');

-- =============================================================================
-- 2. Роли пользователей (user_roles)
-- =============================================================================
INSERT INTO user_roles (user_id, role) VALUES
    (1, 'admin'),
    (1, 'leader'),
    (2, 'participant'),
    (3, 'participant'),
    (3, 'medic'),
    (4, 'participant');

-- =============================================================================
-- 3. Экспедиции (expeditions)
-- =============================================================================
INSERT INTO expeditions (name, description, start_date, end_date, leader_id)
VALUES
    ('Арктика-2025', 'Исследование ледников и биоразнообразия', '2025-03-15', '2025-04-10', 1),
    ('Памир-2025',   'Высотная акклиматизация и геология',      '2025-07-05', '2025-08-20', 1),
    ('Байкал-Зима',  'Зимние исследования озера Байкал',       '2025-01-10', '2025-02-05', 3);

-- =============================================================================
-- 4. Участники экспедиций (participants)
-- =============================================================================
INSERT INTO participants (user_id, expedition_id) VALUES
    (2, 1),   -- Мария → Арктика
    (3, 1),   -- Дмитрий → Арктика
    (4, 1),   -- Екатерина → Арктика
    (2, 2),   -- Мария → Памир
    (4, 2),   -- Екатерина → Памир
    (3, 3);   -- Дмитрий → Байкал

-- =============================================================================
-- 5. Тестовые метрики (примерно по 3–5 записей на человека/экспедицию)
-- =============================================================================

-- cardio_metrics
INSERT INTO cardio_metrics (individual_number, expedition_id, timestamp, session, heart_rate, stress_index, skin_contact)
VALUES
    ('IND-000002', 1, 1741800000000, 1, 78.5,  22.3, 95),
    ('IND-000002', 1, 1741803600000, 1, 92.1,  38.7, 88),
    ('IND-000003', 1, 1741807200000, 2, 65.4,  12.1, 99),
    ('IND-000004', 1, 1741810800000, 1, 84.0,  29.5, 92);

-- eeg_artifacts_metrics
INSERT INTO eeg_artifacts_metrics (expedition_id, individual_number, timestamp, session, artifacts_channel_1, quality_channel_1)
VALUES
    (1, 'IND-000002', 1741801200000, 1, 12, 92),
    (1, 'IND-000003', 1741804800000, 1, 28, 78),
    (1, 'IND-000004', 1741808400000, 1, 5,  96);

-- eeg_proceed_metrics (обработанные)
INSERT INTO eeg_proceed_metrics (expedition_id, individual_number, timestamp, session, channel_1, channel_2)
VALUES
    (1, 'IND-000002', 1741801500000, 1, 12.45, -3.21),
    (1, 'IND-000003', 1741805100000, 1, 8.76,  4.12);

-- emotional_metrics
INSERT INTO emotional_metrics (expedition_id, individual_number, timestamp, session, attention, relaxation, stress, cognitive_load)
VALUES
    (1, 'IND-000002', 1741802000000, 1, 0.82, 0.65, 0.38, 0.71),
    (1, 'IND-000003', 1741805600000, 1, 0.91, 0.48, 0.22, 0.85),
    (1, 'IND-000004', 1741809200000, 1, 0.67, 0.79, 0.55, 0.62);

-- mems_metrics (акселерометр + гироскоп)
INSERT INTO mems_metrics (expedition_id, individual_number, timestamp, session,
    accelerometer_x, accelerometer_y, accelerometer_z,
    gyroscope_x, gyroscope_y, gyroscope_z)
VALUES
    (1, 'IND-000002', 1741803000000, 1, 0.02, -0.01, 9.81, 0.05, -0.03, 0.01),
    (1, 'IND-000003', 1741806600000, 1, 0.15, 0.08, 9.75, 0.12, 0.07, -0.04);

-- nlp_metrics (спектральные мощности — здесь, видимо, EEG bands)
INSERT INTO nlp_metrics (expedition_id, individual_number, timestamp, session, alpha, beta, theta, delta)
VALUES
    (1, 'IND-000002', 1741804000000, 1, 12.4, 8.7, 15.2, 4.1),
    (1, 'IND-000002', 1741804000000, 2, 12.4, 8.7, 15.2, 4.1),
    (1, 'IND-000002', 1741804000000, 3, 12.4, 8.7, 15.2, 4.1),
    (1, 'IND-000004', 1741807600000, 1, 9.8, 11.3, 18.6, 5.9);

-- physiological_metrics
INSERT INTO physiological_metrics (expedition_id, individual_number, timestamp, session, relax, fatigue, concentration, stress)
VALUES
    (1, 'IND-000002', 1741805000000, 1, 0.68, 0.42, 0.75, 0.33),
    (1, 'IND-000003', 1741808600000, 1, 0.81, 0.29, 0.88, 0.19);

-- productivity_metrics
INSERT INTO productivity_metrics (expedition_id, individual_number, timestamp, session, productivity, fatigue, concentration)
VALUES
    (1, 'IND-000002', 1741806000000, 1, 0.76, 0.38, 0.82),
    (1, 'IND-000004', 1741809600000, 1, 0.64, 0.51, 0.69);