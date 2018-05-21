#!/usr/bin/env python3

import os
import unittest

import jque

USERS = open(os.path.dirname(__file__) + "/data/users.json").read()

SMALL = [{
    "_id": "ABC",
    "name": "Arthur Dent",
    "age": 42,
    "current_planet": "earth"
}, {
    "_id": "DE2",
    "name": "Penny Lane",
    "age": 19,
    "current_planet": "earth"
}, {
    "_id": "123",
    "name": "Ford Prefect",
    "age": 240,
    "current_planet": "Brontitall"
}]


class TestJque(unittest.TestCase):

    def test_initialize(self):
        self.assertIsNotNone(jque.jque(USERS).data)

    def test_basic_filter(self):
        self.assertEquals(
            jque.jque(SMALL).query({"name": {"$eq": "Ford Prefect"}}).data[0]['_id'],
            "123"
        )

    def test_literal_filter(self):
        self.assertEquals(
            jque.jque(SMALL).query({"name": "Ford Prefect"}).data[0]['_id'],
            "123"
        )

    def test_multi_literal_filter(self):
        self.assertEquals(
            jque.jque(USERS).query({
                "name": "Glenna Reichert",
                "username": "Delphine",
            }).data[0]['id'],
            9
        )

    def test_multi_filter(self):
        self.assertEquals(
            jque.jque(USERS).query({
                "username": "Delphine",
                "id": {"$gt": 9}
            }).data[0]['id'],
            109
        )

    def test_can_index(self):
        self.assertEquals(
            jque.jque(USERS).data[0],
            jque.jque(USERS)[0]
        )


    def test_length(self):
        self.assertEquals(
            len(jque.jque(USERS).data),
            len(jque.jque(USERS))
        )


    def test_accepts_filename(self):
        self.assertEquals(
            len(jque.jque(os.path.dirname(__file__) + "/data/users.json").data),
            len(jque.jque(USERS).data)
        )

    def test_list_in(self):
        self.assertEquals(
            len(jque.jque(USERS).query({
                "id": {
                    "$in": [9, 109]
                }
            })),
            2
        )

    def test_list_nin(self):
        self.assertEquals(
            len(jque.jque(USERS).query({
                "id": {
                    "$nin": [9, 109]
                }
            })),
            len(jque.jque(USERS)) - 2
        )


    def test_lambda(self):
        self.assertEquals(
            len(jque.jque(USERS).query({
                "id": lambda x: x not in [9, 109, 10]
            })),
            len(jque.jque(USERS)) - 3
        )

