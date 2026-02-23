CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    individual_number VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enabled BOOLEAN DEFAULT TRUE,
    account_non_expired BOOLEAN DEFAULT TRUE,
    account_non_locked BOOLEAN DEFAULT TRUE,
    credentials_non_expired BOOLEAN DEFAULT TRUE
);

CREATE TABLE user_roles (
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, role)
);

CREATE TABLE expeditions (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    leader_id BIGINT NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE participants (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    expedition_id BIGINT NOT NULL REFERENCES expeditions(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, expedition_id)
);

CREATE TABLE cardio_metrics (
    id BIGSERIAL PRIMARY KEY,
    individual_number VARCHAR(255) NOT NULL,
    expedition_id BIGSERIAL,
    timestamp BIGINT NOT NULL,
    session INTEGER,
    heart_rate DOUBLE PRECISION,
    has_artifacts INTEGER,
    kaplan_index DOUBLE PRECISION,
    metrics_available INTEGER,
    motion_artifacts INTEGER,
    skin_contact INTEGER,
    stress_index DOUBLE PRECISION
);

CREATE TABLE eeg_artifacts_metrics (
    id BIGSERIAL PRIMARY KEY,
    expedition_id BIGSERIAL,
    artifacts_channel_1 INTEGER,
    artifacts_channel_2 INTEGER,
    quality_channel_1 INTEGER,
    quality_channel_2 INTEGER,
    individual_number VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    session INTEGER
);

CREATE TABLE eeg_proceed_metrics (
    id BIGSERIAL PRIMARY KEY,
    expedition_id BIGSERIAL,
    channel_1 REAL,
    channel_2 REAL,
    individual_number VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    session INTEGER
);

CREATE TABLE eeg_raw_metrics (
    id BIGSERIAL PRIMARY KEY,
    expedition_id BIGSERIAL,
    channel_1 REAL,
    channel_2 REAL,
    individual_number VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    session INTEGER
);

CREATE TABLE emotional_metrics (
    id BIGSERIAL PRIMARY KEY,
    expedition_id BIGSERIAL,
    individual_number VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    session INTEGER,
    attention DOUBLE PRECISION,
    relaxation DOUBLE PRECISION,
    cognitive_load DOUBLE PRECISION,
    cognitive_control DOUBLE PRECISION,
    self_control DOUBLE PRECISION
);

CREATE TABLE mems_metrics (
    id BIGSERIAL PRIMARY KEY,
    expedition_id BIGSERIAL,
    individual_number VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    session INTEGER,
    accelerometer_x DOUBLE PRECISION,
    accelerometer_y DOUBLE PRECISION,
    accelerometer_z DOUBLE PRECISION,
    gyroscope_x DOUBLE PRECISION,
    gyroscope_y DOUBLE PRECISION,
    gyroscope_z DOUBLE PRECISION
);

CREATE TABLE nlp_metrics (
    id BIGSERIAL PRIMARY KEY,
    expedition_id BIGSERIAL,
    individual_number VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    session INTEGER,
    alpha DOUBLE PRECISION,
    beta DOUBLE PRECISION,
    theta DOUBLE PRECISION,
    delta DOUBLE PRECISION,
    smr DOUBLE PRECISION
);

CREATE TABLE physiological_metrics (
    id BIGSERIAL PRIMARY KEY,
    expedition_id BIGSERIAL,
    individual_number VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    session INTEGER,
    relax DOUBLE PRECISION,
    fatigue DOUBLE PRECISION,
    none DOUBLE PRECISION,
    concentration DOUBLE PRECISION,
    involvement DOUBLE PRECISION,
    stress DOUBLE PRECISION,
    nfb_artifacts INTEGER,
    cardio_artifacts INTEGER
);

CREATE TABLE productivity_metrics (
    id BIGSERIAL PRIMARY KEY,
    expedition_id BIGSERIAL,
    individual_number VARCHAR(255) NOT NULL,
    timestamp BIGINT NOT NULL,
    session INTEGER,
    gravity DOUBLE PRECISION,
    productivity DOUBLE PRECISION,
    fatigue DOUBLE PRECISION,
    reverse_fatigue DOUBLE PRECISION,
    relaxation DOUBLE PRECISION,
    concentration DOUBLE PRECISION
);