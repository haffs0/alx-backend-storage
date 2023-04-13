#!/usr/bin/env python3
"""update all topics in a documents into a collection"""


def update_topics(mongo_collection, name, topics):
    """update documnets in mongo_collection"""
    mongo_collection.update_many(
        {'name': name},
        {"$set": {'topics': topics}}
    )
