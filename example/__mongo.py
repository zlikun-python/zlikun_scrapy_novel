# -*- coding: utf-8 -*-
from datetime import datetime

import pymongo
from pymongo import MongoClient

with MongoClient(host='localhost') as client:
    db = client.get_database('novels_example')

    collection = db.get_collection('novel')

    # 插入小说数据
    result = collection.insert_one({
        'number': 1,
        'name': '牛B是怎么吹起来的',
        'author': '张三'
    })

    # <class 'pymongo.results.InsertOneResult'> <pymongo.results.InsertOneResult object at 0x000001947089CE48>
    print(type(result), result)
    # 5bb9927de7c87e7490e7952f
    print(result.inserted_id)

    # 更新小说最新章节ID
    result = collection.update_one({'number': 1},
                                   {'$set': {'latest_chapter_number': 128, 'update_time': datetime.now()}})
    # <class 'pymongo.results.UpdateResult'>
    print(type(result), result)
    # {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}
    print(result.raw_result)

    # 查询列表中最大值（number）
    result = collection.find({}, {'_id': 0, 'number': 1}).sort('number', direction=pymongo.DESCENDING).limit(1)
    try:
        record = result.next()
        # <class 'dict'> {'_id': ObjectId('5bb996e7e7c87e7ddc64ab23'), 'number': 1, 'name': '牛B是怎么吹起来的', 'author': '张三', 'latest_chapter_number': 128, 'update_time': datetime.datetime(2018, 10, 7, 13, 17, 27, 882000)}
        # <class 'dict'> {'number': 1}
        print(type(record), record)
    except StopIteration:
        pass

    # 简单查询单列最大值（我记得是可以实现的，想不起来了~）
    # result = collection.find({}, {'_id': -1, 'number': 1}).max(['number'])
    # print(type(result), result)

    # 清除测试数据
    result = collection.delete_one({'number': 1})
    # <class 'pymongo.results.DeleteResult'> <pymongo.results.DeleteResult object at 0x0000024148197A08>
    print(type(result), result)
    # {'n': 1, 'ok': 1.0}
    print(result.raw_result)

    pass

with MongoClient(host='localhost') as client:
    db = client.get_database('novels')

    novel_number = '39_39672'

    # 查询小说数据
    for novel in db.get_collection('novel').find():
        print(novel)

    # 查询章节列表
    for chapter in db.get_collection('novel_{}'.format(novel_number)).find().sort('number',
                                                                                  direction=pymongo.DESCENDING):
        print(chapter)

    # 查询最新章节
    result = db.get_collection('novel_{}'.format(novel_number)). \
        find({}, {'_id': 0, 'number': 1}).sort('number', direction=pymongo.DESCENDING) \
        .limit(1)
    try:
        record = next(result)
        if record:
            print(record)
            # 将其更新至小说记录中
            latest_chapter_number = record['number']
            print('latest_chapter_number => ', latest_chapter_number)
    except StopIteration:
        print('--empty--')
        pass
