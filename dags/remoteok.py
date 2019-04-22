import pymongo
from pymongo import UpdateOne
import requests
import redis
import json
import dateutil.parser as dateparser


MONGO_DB = "remotejobs"
REDIS_KEY = 'remoteokio'
store = redis.Redis(host='redis')
client = pymongo.MongoClient('mongo', 27017)

def fetch_data():
    r = requests.get('https://remoteok.io/api')
    if r.text:
        store.set(REDIS_KEY, r.text)

def process_data():
        data = store.get(REDIS_KEY)
        data = json.loads(data)
        data.pop(0)
        for item in data:
                item['location'] = 'remote'
                item['date'] = dateparser.parse(item.get('date', 'None')).isoformat() 
                item['source'] = REDIS_KEY
        store.set(REDIS_KEY, json.dumps(data))
        
def store_data():
    db = client[MONGO_DB]
    data = store.get(REDIS_KEY)
    data = json.loads(data)
    JobsTable = db.jobs
    ids=[item.pop("id") for item in data]
    operations=[UpdateOne({"id":idn},{'$set':data}, upsert=True) for idn ,data in zip(ids,data)]
    JobsTable.bulk_write(operations)