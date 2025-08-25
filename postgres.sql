CREATE TABLE IF NOT EXISTS model_metrics (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP DEFAULT NOW(),
    model_version TEXT,
    mae DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS api_requests (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP DEFAULT NOW(),
    store_id TEXT,
    product_id TEXT,
    forecast_units DOUBLE PRECISION
);
