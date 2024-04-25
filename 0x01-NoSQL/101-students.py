#!/usr/bin/env python3
"""give all students sorted by score"""


def top_students(mongo_collection):
    """ Gives all students sorted by score """
    return mongo_collection.aggregate([
        {
            '$project': {
                'name': '$name',
                'averageScore': {
                    '$avg': "$topics.score"
                }
            }
        },
        {
            '$sort': {
                "averageScore": -1
            }
        }
    ])
