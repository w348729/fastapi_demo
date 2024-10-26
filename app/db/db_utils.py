from pymongo import MongoClient
from app.settings import MONGODB_URL

# client = MongoClient('mongodb://localhost:27017')
client = MongoClient(MONGODB_URL)
db_demo = client['demo']