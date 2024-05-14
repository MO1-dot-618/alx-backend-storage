#!/usr/bin/env python3
"""
Module: 10-update_topics.py

Contains a function to update the topics of a school document based on the school name.
"""

def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.

    Args:
        mongo_collection: A PyMongo collection object.
        name (str): The school name to update.
        topics (list of str): The list of topics approached in the school.
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
