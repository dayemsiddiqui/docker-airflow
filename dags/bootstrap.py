import os
import pymongo
import redis
from dotenv import load_dotenv
import os
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASS = os.getenv("REDIS_PASS")
MONGO_DB   = os.getenv("MONGO_DB")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")

store = redis.Redis(
    host= REDIS_HOST,
    port= REDIS_PORT,
    password= REDIS_PASS)
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
db.authenticate(MONGO_USER, MONGO_PASS)
