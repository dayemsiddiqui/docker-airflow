from pymongo import MongoClient
from bson import json_util
import json
import pymongo
from flask import jsonify

client = MongoClient('mongo', 27017)
db = client.remotejobs

def fetch_latest_jobs(page=1, per_page=10):
    jobs = db.jobs.find().sort('date', pymongo.ASCENDING).skip((page - 1) * per_page).limit(per_page)
    jobs = list(jobs)
    jobs = json.dumps({'result': jobs, 'prev_url': '', 'next_url': ''}, indent=4, default=json_util.default)

    return jsonify(json.loads(jobs))