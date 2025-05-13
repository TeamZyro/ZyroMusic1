import pymongo
from pymongo.errors import ConnectionFailure

class MongoDB:
    def __init__(self, mongo_uri: str = "mongodb+srv://harshmanjhi1801:webapp@cluster0.xxwc4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", db_name: str = "TEAMZYRO", collection_name: str = "catbox_cache"):
        try:
            self.client = pymongo.MongoClient(mongo_uri)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            # Create an index on vidid for faster lookups
            self.collection.create_index("vidid", unique=True)
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    async def get_catbox_link(self, vidid: str) -> str | None:
        try:
            doc = self.collection.find_one({"vidid": vidid})
            return doc["catbox_link"] if doc else None
        except Exception as e:
            print(f"Error fetching from MongoDB: {e}")
            return None

    async def save_catbox_link(self, vidid: str, catbox_link: str) -> bool:
        try:
            self.collection.update_one(
                {"vidid": vidid},
                {"$set": {"vidid": vidid, "catbox_link": catbox_link}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error saving to MongoDB: {e}")
            return False

    def close(self):
        self.client.close()
