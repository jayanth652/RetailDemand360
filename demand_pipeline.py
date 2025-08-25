from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("retail_demand_daily",
         start_date=datetime(2024,1,1),
         schedule_interval="@daily",
         catchup=False) as dag:

    bronze_to_silver_gold = BashOperator(
        task_id="batch_etl",
        bash_command="spark-submit /opt/airflow/dags/../..//spark/batch_etl.py"
    )
    build_features = BashOperator(
        task_id="feature_store",
        bash_command="spark-submit /opt/airflow/dags/../..//feature_store/feature_build.py"
    )
    train = BashOperator(
        task_id="train_model",
        bash_command="python /opt/airflow/dags/../..//ml/train_forecast.py"
    )

    bronze_to_silver_gold >> build_features >> train
