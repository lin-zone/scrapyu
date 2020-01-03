import logging

from pymongo import MongoClient
from scrapy.exceptions import CloseSpider


class MongoDBPipeline(object):

    config = {
        'uri': 'mongodb://localhost:270017',
        'database': 'scrapyu',
        'collection': 'items',
        'unique_key': None,
        'buffer_length': 0,
    }

    def open_spider(self, spider):
        self.logger = logging.getLogger('scrapyu.MongoDBPipeline')
        self.configure(spider.settings)
        config = self.config
        self.connection = MongoClient(config['uri'])
        self.database = self.connection[config['database']]
        self.collection = self.database[config['collection']]
        self.logger.info(
            f"Connected to MongoDB {config['uri']}, "
            f"using {config['database']}.{config['collection']}"
        )
        self.has_buffer = bool(config['buffer_length'])
        if self.has_buffer:
            self._item_buffer = []

    def close_spider(self, spider):
        if self.has_buffer and len(self._item_buffer):
            self._commit_buffer()
        self.connection.close()

    def process_item(self, item, spider):
        item_dict = dict(item)
        if self.has_buffer:
            self.insert_buffer(item_dict)
        else:
            self.insert_one(item_dict)
        return item

    def _commit_buffer(self):
        items = self._item_buffer.copy()
        self.collection.insert_many(items)
        self._item_buffer.clear()

    def insert_buffer(self, item):
        self._item_buffer.append(item)
        if len(self._item_buffer) >= self.config['buffer_length']:
            self._commit_buffer()

    def insert_one(self, item):
        unique_key = self.config['unique_key']
        if unique_key is None:
            self.collection.insert_one(item)
        else:
            spec = {}
            try:
                for k in unique_key:
                    spec[k] = item[k]
                self.collection.update_one(spec, {'$set': item}, upsert=True)
            except KeyError as e:
                msg = f"unique_key defined error, item has no {str(e)} field"
                CloseSpider(msg)

    def configure(self, settings):
        uri = settings.get('MONGODB_URI')
        if uri is None:
            host = settings.get('MONGODB_HOST', 'localhost')
            port = settings.get('MONGODB_PORT', 27017)
            uri = f'mongodb://{host}:{port}'
        self.config['uri'] = uri
        self.config['database'] = settings.get('MONGODB_DATABASE', 'scrapyu')
        self.config['collection'] = settings.get('MONGODB_COLLECTION', 'items')
        unique_key = settings.get('MONGODB_UNIQUE_KEY')
        if unique_key is not None:
            if isinstance(unique_key, str):
                unique_key = unique_key.split()
            else:
                unique_key = list(unique_key)
        self.config['unique_key'] = unique_key
        self.config['buffer_length'] = settings.get('MONGODB_BUFFER_LENGTH', 0)
