from pymongo import UpdateOne
import requests
import json
from lxml import etree, objectify
from lxml.etree import fromstring
import dateutil.parser as dateparser

from bootstrap import store, db

REDIS_KEY = "stackoverflow"

def fetch_data():
    r = requests.get('https://stackoverflow.com/jobs/feed')
    if r.text:
        store.set(REDIS_KEY, r.text.encode('utf-8'))
        

def process_data():
        xml = store.get(REDIS_KEY)
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = fromstring(xml, parser=parser)
        # objectify.deannotate(root, cleanup_namespaces=True)
        items = root.findall('.//item') 
        namespaces = {'a10': 'http://www.w3.org/2005/Atom'} 
        data = []
        for item in items:
            company_name = item.find(".//a10:name", namespaces)
            company_name = ''.join(company_name.itertext())
            tags = item.findall('category')
            tags_str = []
            for tag in tags:
                tags_str.append(''.join(tag.itertext()))
            temp = {}
            temp['id'] = item.findtext('guid', default = 'None') + '-stackoverflow'
            temp['company'] = company_name
            temp['date'] = dateparser.parse(item.findtext('pubDate', default = 'None')).isoformat() 
            temp['description'] = item.findtext('description', default = 'None')
            temp['position'] = item.findtext('title', default = 'None')
            temp['slug'] = item.findtext('title', default = 'None')
            temp['title'] = item.findtext('title', default = 'None')
            temp['tags'] = tags_str
            temp['url'] = item.findtext('link', default = 'None')
            temp['location'] = item.findtext('location', default = 'remote')
            temp['source'] = REDIS_KEY
            data.append(temp)
    
        store.set(REDIS_KEY, json.dumps(data))
        
def store_data():
    data = store.get(REDIS_KEY)
    data = json.loads(data)
    JobsTable = db.jobs
    ids=[item.pop("id") for item in data]
    operations=[UpdateOne({"id":idn},{'$set':data}, upsert=True) for idn ,data in zip(ids,data)]
    JobsTable.bulk_write(operations)
