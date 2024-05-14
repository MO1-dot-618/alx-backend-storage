"""
Module: 8-all.py
"""

def list_all(mongo_collection):
    """
    Lists all documents in the given MongoDB collection.

    Args:
        mongo_collection: A PyMongo collection object.

    Returns:
        A list containing all documents in the collection. Returns an empty list if no documents found.
    """
    documents = mongo_collection.find({})

    result = []

    for doc in documents:
        result.append(doc)

    return result

