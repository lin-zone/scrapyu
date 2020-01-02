import logging

from pymongo import MongoClient


class MongoDBPipeline(object):

    config = {
        'uri': 'mongodb://localhost:270017',
        'database': 'scrapyu',
        'collection': 'items',
        'unique_key': None,
    }

    def open_spider(self, spider):
        self.logger = logging.getLogger('mongodb-pipeline')
        self.configure(spider.settings)
        config = self.config
        self.connection = MongoClient(config['uri'])
        self.database = self.connection[config['database']]
        self.collection = self.database[config['collection']]
        self.logger.info(
            f"Connected to MongoDB {config['uri']}, "
            f"using {config['database']}.{config['collection']}"
        )

    def process_item(self, item, spider):
        unique_key = self.config['unique_key']
        item_dict = dict(item)
        if unique_key is None:
            self.collection.insert_one(item_dict)
        else:
            spec = {}
            try:
                for k in unique_key:
                    spec[k] = item[k]
                self.collection.update_one(spec, {'$set': item_dict}, upsert=True)
            except KeyError as e:
                msg = f"unique_key defined error, item has no {str(e)} field"
                spider.crawler.engine.close_spider(spider, msg)
        return item

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