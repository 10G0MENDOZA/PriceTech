import pymongo

class MongoPipeline:

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["pricetech"]
        self.collection = self.db["productos"]

    def process_item(self, item, spider):
        self.collection.update_one(
            {
                "nombre": item["nombre"],
                "tienda": item["tienda"]
            },
            {"$set": dict(item)},
            upsert=True
        )
        return item