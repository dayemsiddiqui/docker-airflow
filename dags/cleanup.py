import pymongo
from pymongo import UpdateOne
import requests
import redis
import json
import dateutil.parser as dateparser


MONGO_DB = "remotejobs"
REDIS_KEY = 'cleanup'
store = redis.Redis(host='redis')
client = pymongo.MongoClient('mongo', 27017)

def remove_no_company_name():
    db = client[MONGO_DB]
    JobsTable = db.jobs
    JobsTable.delete_many({"company": ""})

