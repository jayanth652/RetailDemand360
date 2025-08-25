# RetailDemand360 — Real-Time Demand Forecasting & Inventory Optimization

🚀 An enterprise-grade **Data Engineering + Data Science** project simulating a modern retail company.  
Covers **streaming ingestion (Kafka)**, **batch ETL (Spark)**, **feature store**,  
**demand forecasting models (XGBoost, Prophet) tracked with MLflow**,  
**orchestration with Airflow**, **model serving via FastAPI**, and  
**BI dashboards with Superset** — all containerized with **Docker Compose**.

---

## ✨ Features
- 📥 **Data Ingestion** — Synthetic POS & e-commerce events → Kafka topics  
- ⚙️ **ETL Pipeline** — Spark Structured Streaming (raw→bronze), Batch ETL (bronze→silver→gold)  
- 🏪 **Feature Store** — Point-in-time features for demand forecasting  
- 🤖 **ML Forecasting** — XGBoost/Prophet models logged & versioned in MLflow  
- 🌐 **Model Serving** — FastAPI REST endpoint for real-time forecasts  
- 📊 **Analytics** — Apache Superset dashboards (Revenue, Promotions, Forecast vs Actuals)  
- 🔄 **Orchestration** — Airflow DAGs for daily ETL + retraining  
- 🐳 **Infra** — Full stack in Docker Compose (Kafka, MinIO, Airflow, MLflow, Superset, PostgreSQL)  

---

## 🏗️ Architecture

mermaid
flowchart TD
    A[IoT POS + Online Orders<br/>(Data Generator)] -->|Kafka topics| B[Kafka]
    B --> C[Spark Structured Streaming<br/>Raw -> Bronze (MinIO)]
    C --> D[Batch Spark Jobs<br/>Bronze -> Silver -> Gold]
    D --> E[Feature Store<br/>Snapshot Features]
    E --> F[ML Training (XGBoost/Prophet)<br/>MLflow Tracking]
    F --> G[FastAPI Model Serving]
    D --> H[Superset Dashboards]
    I[Airflow] -->|Schedules & Orchestrates| C
    I --> D
    G --> J[Monitoring & Drift Metrics<br/>PostgreSQL]

# 1. Clone repository
git clone https://github.com/<your-username>/RetailDemand360.git
cd RetailDemand360

# 2. Start infrastructure
docker compose up -d

# 3. Generate synthetic data
python data/generator/generate_transactions.py --rate 5 --minutes 10

# 4. Run Spark ETL
spark-submit spark/streaming_demand.py
spark-submit spark/batch_etl.py

# 5. Build features
spark-submit feature_store/feature_build.py

# 6. Train & track models
python ml/train_forecast.py

# 7. Serve API
uvicorn services.api.app:app --reload


📊 Dashboards

Daily Revenue & Units by Store/Product

Promotion Impact on Sales

Forecast vs Actuals

Model Health (MAE, Drift Detection)

---

## 🛠️ Tech Stack

**Languages:** Python, SQL, PySpark  
**Data Engineering:** Apache Kafka, Apache Spark, Apache Airflow, MinIO (S3), Docker, Docker Compose  
**Machine Learning:** XGBoost, Prophet, MLflow  
**Serving & APIs:** FastAPI, Uvicorn  
**BI & Visualization:** Apache Superset  
**Database & Storage:** PostgreSQL, Parquet  

---
