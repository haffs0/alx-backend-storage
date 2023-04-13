#!/usr/bin/env python3
"""insert documents into a collection"""


def insert_school(mongo_collection, **kwargs):
    """return id of insert documnets into mongo_collection"""
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
