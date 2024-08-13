#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs
in the collection nginx of the database logs
"""

from pymongo import MongoClient


def log_stats():
    """
    Prints a collection of nginx database log:
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    total_logs = logs_collection.count_documents({})
    get_logs = logs_collection.count_documents({"method": "GET"})
    post_logs = logs_collection.count_documents({"method": "POST"})
    put_logs = logs_collection.count_documents({"method": "PUT"})
    patch_logs = logs_collection.count_documents({"method": "PATCH"})
    delete_logs = logs_collection.count_documents({"method": "DELETE"})
    path = logs_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{total_logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_logs}")
    print(f"\tmethod POST: {post_logs}")
    print(f"\tmethod PUT: {put_logs}")
    print(f"\tmethod PATCH: {patch_logs}")
    print(f"\tmethod DELETE: {delete_logs}")
    print(f"{path} status check")
    print("IPs:")
    sorted_ips = logs_collection.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    i = 0
    for s in sorted_ips:
        if i == 10:
            break
        print(f"\t{s.get_logs('_id')}: {s.get_logs('count')}")
        i += 1


if __name__ == "__main__":
    log_stats()
