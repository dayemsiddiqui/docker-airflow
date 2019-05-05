from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from cleanup import remove_no_company_name

dag = DAG('cleanup', description='DAG cleaning up bad data',
          schedule_interval = '@daily',
          start_date=datetime(2019, 3, 20), catchup=False)


no_company_name = PythonOperator(task_id='remove_no_company_name', python_callable=remove_no_company_name, dag=dag)

no_company_name