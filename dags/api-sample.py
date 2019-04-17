from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
import redis
import logging
from sshtunnel import SSHTunnelForwarder
import pymongo

def fetch_data():
    r = requests.get('https://remoteok.io/api')
    if r.text:
        store = redis.Redis(host='redis')
        store.set('remoteokio', r.text)

def process_data():
    store = redis.Redis(host='redis')
    if store:
        data = store.get('remoteokio')
        logging.info(data)

def store_data():
    MONGO_HOST = "134.209.244.189"
    MONGO_DB = "remotejobs"
    MONGO_USER = "root"
    MONGO_PASS = "kibo1234"
    server = SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_password=MONGO_PASS,
        remote_bind_address=('127.0.0.1', 27017)
    )
    server.start()
    client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
    db = client[MONGO_DB]
    logging.info(db.collection_names())
    server.stop()

dag = DAG('api-sample', description='Sample DAG for fetching data from api',
          schedule_interval = '@daily',
          start_date=datetime(2019, 3, 20), catchup=False)


get_data = PythonOperator(task_id='get_data', python_callable=fetch_data, dag=dag)
process_data = PythonOperator(task_id='process_data', python_callable=process_data, dag=dag)
store_data = PythonOperator(task_id='store_data', python_callable=store_data, dag=dag)

get_data >> process_data >> store_data