# crypto pipeline dag

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'alin',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='crypto_pipeline',
    default_args=default_args,
    description='Pipeline ETL crypto: ingestie + dbt',
    schedule_interval='0 8 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False
) as dag:

    ingest_task = BashOperator(
        task_id='ingest_coins',
        bash_command='python /opt/airflow/project/scripts/ingest_coins.py'
    )

    dbt_run_task = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/project && dbt run --profiles-dir /opt/airflow/project'
    )

    dbt_test_task = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/project && dbt test --profiles-dir /opt/airflow/project'
    )

    ingest_task >> dbt_run_task >> dbt_test_task
