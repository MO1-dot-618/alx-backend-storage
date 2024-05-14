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

    # Display the statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    log_stats()
