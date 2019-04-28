from pymongo import MongoClient
from bson import json_util
import json
import pymongo
from flask import jsonify
from werkzeug.contrib.cache import RedisCache
import sys

cache = RedisCache(host='redis')
client = MongoClient('mongo', 27017)
db = client.remotejobs

def fetch_latest_jobs(page=1, per_page=10):
    jobs = db.jobs.find().sort('date', pymongo.ASCENDING).skip((page - 1) * per_page).limit(per_page)
    jobs = list(jobs)
    jobs = json.dumps({'result': jobs, 'prev_url': '', 'next_url': ''}, indent=4, default=json_util.default)

    return jsonify(json.loads(jobs))

def get_total_jobs_count():
    rv = cache.get('total-jobs-count')
    if rv is None:
        print('Cache Miss', file=sys.stderr)
        count = db.jobs.find().count()
        response = json.dumps({'result': count})
        cache.set('total-jobs-count', response, timeout=60 * 60 * 24)
        return jsonify(json.loads(response))
    
    print('Cache Hit', file=sys.stderr)
    return jsonify(json.loads(rv))