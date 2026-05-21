# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo


class MongoPipeline:

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["pricetech"]
        self.collection = self.db["productos"]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item