from scrapy import Spider
from scrapy.utils.test import get_crawler

from scrapyu import MongoDBPipeline



def find_items(pipe):
    return list(pipe.collection.find({}, {'_id': 0}))


def drop_collection(pipe):
    pipe.collection.drop()


def collection_length(pipe):
    return pipe.collection.estimated_document_count()


def open_pipe(**kwargs):
    ITEM_PIPELINES = {
        'scrapyu.MongoDBPipeline': 300,
    }
    settings = dict(
        ITEM_PIPELINES=ITEM_PIPELINES,
        MONGODB_HOST='localhost',
        MONGODB_PORT=27017,
        MONGODB_DATABASE='test-mongodb-pipeline-database',
        MONGODB_COLLECTION='test-mongodb-pipeline-collection',
    )
    settings.update(kwargs)
    crawler = get_crawler(Spider, settings_dict=settings)
    spider = crawler._create_spider('foo')
    pipe = MongoDBPipeline()
    pipe.open_spider(spider)
    drop_collection(pipe)
    return pipe, spider


def test_mongodb_pipeline():
    pipe, spider = open_pipe()

    item1 = dict(id=1, name='one')
    item2 = dict(id=2, name='two')
    pipe.process_item(item1, spider)
    pipe.process_item(item1, spider)
    pipe.process_item(item2, spider)

    assert collection_length(pipe) == 3
    assert find_items(pipe) == [item1, item1, item2]

    drop_collection(pipe)


def test_str_unique_key():
    pipe, spider = open_pipe(MONGODB_UNIQUE_KEY='id')

    item1 = dict(id=1, name='one')
    item2 = dict(id=2, name='two')
    item3 = dict(id=1, name='two')
    item4 = dict(id=2, name='one')

    pipe.process_item(item1, spider)
    pipe.process_item(item2, spider)
    pipe.process_item(item3, spider)
    pipe.process_item(item4, spider)

    assert collection_length(pipe) == 2
    assert find_items(pipe) == [item3, item4]

    drop_collection(pipe)


def test_list_unique_key():
    pipe, spider = open_pipe(MONGODB_UNIQUE_KEY=['id'])

    item1 = dict(id=1, name='one')
    item2 = dict(id=2, name='two')
    item3 = dict(id=1, name='two')
    item4 = dict(id=2, name='one')

    pipe.process_item(item1, spider)
    pipe.process_item(item2, spider)
    pipe.process_item(item3, spider)
    pipe.process_item(item4, spider)

    assert collection_length(pipe) == 2
    assert find_items(pipe) == [item3, item4]

    drop_collection(pipe)


def test_buffer():
    pipe, spider = open_pipe(
        MONGODB_UNIQUE_KEY='id',
        MONGODB_BUFFER_LENGTH=3,
        )

    item1 = dict(id=1, name='one')
    item2 = dict(id=2, name='two')
    item3 = dict(id=1, name='two')
    item4 = dict(id=2, name='one')

    pipe.process_item(item1, spider)
    assert pipe._item_buffer == [item1]
    assert find_items(pipe) == []

    pipe.process_item(item2, spider)
    assert pipe._item_buffer == [item1, item2]
    assert find_items(pipe) == []

    pipe.process_item(item3, spider)
    assert pipe._item_buffer == []
    assert find_items(pipe) == [item1, item2, item3]

    pipe.process_item(item4, spider)
    assert pipe._item_buffer == [item4]
    assert find_items(pipe) == [item1, item2, item3]

    pipe.close_spider(spider)
    assert pipe._item_buffer == []
    assert find_items(pipe) == [item1, item2, item3, item4]

    drop_collection(pipe)
