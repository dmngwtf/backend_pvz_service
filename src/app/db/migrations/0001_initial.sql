CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('employee', 'moderator'))
);

CREATE TABLE IF NOT EXISTS pvzs (
    id UUID PRIMARY KEY,
    registration_date TIMESTAMP NOT NULL,
    city VARCHAR(50) NOT NULL CHECK (city IN ('Москва', 'Санкт-Петербург', 'Казань'))
);

CREATE TABLE IF NOT EXISTS receptions (
    id UUID PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    pvz_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('in_progress', 'close'))
);

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY,
    date_time TIMESTAMP NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('электроника', 'одежда', 'обувь')),
    reception_id UUID NOT NULL
);