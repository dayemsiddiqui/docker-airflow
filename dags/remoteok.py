from sshtunnel import SSHTunnelForwarder
import pymongo
from pymongo import UpdateOne
import requests
import redis
import json

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
store = redis.Redis(host='redis')

def fetch_data():
    r = requests.get('https://remoteok.io/api')
    if r.text:
        store.set('remoteokio', r.text)

def process_data():
        data = store.get('remoteokio')
        data = json.loads(data)
        data.pop(0)
        store.set('remoteokio', json.dumps(data))
        
        

def store_data():
    server.start()
    client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)
    db = client[MONGO_DB]
    data = store.get('remoteokio')
    data = json.loads(data)
    JobsTable = db.jobs
    ids=[item.pop("id") for item in data]
    operations=[UpdateOne({"id":idn},{'$set':data}, upsert=True) for idn ,data in zip(ids,data)]
    JobsTable.bulk_write(operations)
    server.stop()