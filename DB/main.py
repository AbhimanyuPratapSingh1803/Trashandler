import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("DATABASE_URI"))
db = client[os.getenv("DB_NAME")]

def get_collection(collection_name):
    return db[collection_name]