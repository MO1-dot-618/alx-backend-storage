#!/usr/bin/env python3

"""
Module: 12-log_stats.py

Provides statistics about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient

def log_stats():
    """
    Provides statistics about Nginx logs stored in MongoDB.

    It connects to the MongoDB instance, retrieves statistics about the Nginx logs,
    and prints out the results in the specified format.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx

    # Get the total number of logs
    total_logs = collection.count_documents({})

    # Get the count of each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method}) for method in methods}

    # Get the count of status check
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    # Get the top 10 most present IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    # Display the statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check_count} status check")

    print("IPs:")
    for idx, ip_info in enumerate(top_ips, 1):
        print(f"\t{ip_info['_id']}: {ip_info['count']}")

if __name__ == "__main__":
    log_stats()
