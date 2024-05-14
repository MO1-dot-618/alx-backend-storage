#!/usr/bin/env python3
"""
Module: 9-insert_school.py

Contains a function to insert a new document into a MongoDB collection based on keyword arguments.
"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the given MongoDB collection based on the provided keyword arguments.

    Args:
        mongo_collection: A PyMongo collection object.
        **kwargs: Keyword arguments representing the fields and values of the new document.

    Returns:
        The _id of the newly inserted document.
    """
    # Insert the document into the collection and retrieve the inserted _id
    result = mongo_collection.insert_one(kwargs)

    # Return the _id of the newly inserted document
    return result.inserted_id
