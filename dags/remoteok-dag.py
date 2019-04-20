from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from remoteok import fetch_data, process_data, store_data

dag = DAG('remoteok', description='DAG for fetching data from remoteok',
          schedule_interval = '@daily',
          start_date=datetime(2019, 3, 20), catchup=False)


get_data = PythonOperator(task_id='get_data', python_callable=fetch_data, dag=dag)
process_data = PythonOperator(task_id='process_data', python_callable=process_data, dag=dag)
store_data = PythonOperator(task_id='store_data', python_callable=store_data, dag=dag)

get_data >> process_data >> store_data