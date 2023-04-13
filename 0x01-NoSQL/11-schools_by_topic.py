#!/usr/bin/env python3
"""lists all documents in a collection have a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """return all school having a specfic topic in mongo_collection"""
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    results = mongo_collection.find(topic_filter)
    return [doc for doc in results]
