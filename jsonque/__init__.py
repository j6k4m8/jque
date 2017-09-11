import json
import copy


__version__ = "0.0.1"


class jsonque:
    """
    A JSON query class that subsets the behavior of MongoDB queries.

        data = jsonque.jsonque([{
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
        }])

        teenage_earthlings = data.query({
            "current_planet": {"$eq": "earth"},
            "age": { "$lte": 20, "$gte": 10 }
        })
        """

    OPERATORS = {
        "$eq": lambda x, y: x == y,
        "$neq": lambda x, y: x != y,
        "$lt": lambda x, y: x < y,
        "$lte": lambda x, y: x <= y,
        "$gt": lambda x, y: x > y,
        "$gte": lambda x, y: x >= y,
        "$in": lambda x, y: y in x,
        "$nin": lambda x, y: y not in x,
        # TODO: Add operators as useful.
    }

    def __init__(self, data):
        """
        Create a new jsonque object. Pass `data`, which must be a
        string or a list. If a list, each item should be a dictionary.
        If a string, it can either be a JSON string (from Python's
        json.dumps or JS's JSON.stringify) or a filename that points
        to a .json file on disk.
        """
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as ex:
                data = json.loads(open(data, 'r').read())
        elif not isinstance(data, list):
            raise ValueError("'data' argument must be a string or a list.")

        self.data = data

    def query(self, qr):
        """
        Query the records for a desired trait. qr should be a dict
        where all keys are included in all records.
        """
        filtered_data = []
        for record in self.data:
            include = True
            for key, qual in qr.items():
                for op, val in qual.items():
                    if op not in self.OPERATORS:
                        raise ValueError(
                            "'{}' is not a valid operator.".format(op)
                        )
                    if not self.OPERATORS[op](record[key], val):
                        include = False
            if include:
                filtered_data.append(record)
        return filtered_data
