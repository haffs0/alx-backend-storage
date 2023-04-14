#!/usr/bin/env python3
""" logs stats """
from pymongo import MongoClient


def logs_stats(mongo_collection):
    """Print stats about Nginx logs stored in MongoDB"""
    log_info = {
      'GET': 0,
      'POST': 0,
      'PUT': 0,
      'PATCH': 0,
      'DELETE': 0
    }
    status_count = 0
    nginx_logs = [doc for doc in mongo_collection.find()]
    total_file_size = len(nginx_logs)
    for log in nginx_logs:
        if log['method'] in log_info:
            log_info[log['method']] += 1
        if log['path'] == '/status':
            status_count += 1
    print(f"{total_file_size} logs")
    print("Methods:")
    for method in log_info.keys():
        str_res = f"\tmethod {method}: {log_info[method]}"
        result = str_res.expandtabs(4)
        print(result)
    print(f"{status_count} status check")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx
    logs_stats(nginx)
