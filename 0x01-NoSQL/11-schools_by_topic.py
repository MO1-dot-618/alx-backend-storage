#!/usr/bin/env python3
"""
Module: 11-schools_by_topic.py

Contains a function to return the list of schools having a specific topic.
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: A PyMongo collection object.
        topic (str): The topic searched.

    Returns:
        A list of dictionaries representing schools having the specified topic.
    """
    # Find all schools with the specified topic
    schools = mongo_collection.find({"topics": topic})

    # Convert the cursor to a list of dictionaries
    return schools
