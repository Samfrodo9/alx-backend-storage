#!/usr/bin/env python3
"""MongoDB Find"""


def schools_by_topic(mongo_collection, topic):
    """
    Used an aggregate to find docsx
    :param mongo_collection: Pymongo connection
    :param topic: The topic to search
    :return: The list of school that having the same topics
    """
    return [i for i in mongo_collection.find({"topics": topic})]
