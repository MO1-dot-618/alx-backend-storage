#!/usr/bin/env python3
"""
top student
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
        mongo_collection: A PyMongo collection object.

    Returns:
        A list of dictionaries representing students, sorted by average score.
        Each dictionary contains the student's information
        along with the average score.
    """
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ]

    result = mongo_collection.aggregate(pipeline)

    return list(result)
