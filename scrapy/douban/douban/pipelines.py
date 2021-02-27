# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .settings import mongo_host, mongo_port, mongo_db_name, mongo_db_collection

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DoubanPipeline:
    def __init__(self):
        client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
        mydb = client[mongo_db_name]
        self.post = mydb[mongo_db_collection]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
