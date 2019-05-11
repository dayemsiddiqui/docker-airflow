
from pymongo import UpdateOne
import requests
import json
import dateutil.parser as dateparser

from bootstrap import store, db

REDIS_KEY = "cleanup"

def remove_no_company_name():
    JobsTable = db.jobs
    JobsTable.delete_many({"company": ""})

