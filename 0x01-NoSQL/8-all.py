#!/usr/bin/env python3
"""lists all documents in a collection"""


def list_all(mongo_collection):
    """return all documnets in mongo_collection"""
    return [doc for doc in mongo_collection.find()]
