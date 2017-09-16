import json
import copy
import types

_run_parallel = False
try:
    from deco import synchronized, concurrent
    _run_parallel = True
except:
    _run_parallel = False
    concurrent = lambda x: x
    synchronized = lambda x: x


__version__ = "0.0.1"


_OPERATORS = {
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


@concurrent
def _check_record(qr, record):
    include = True
    for key, qual in qr.items():
        if isinstance(qual, dict):
            for op, val in qual.items():
                if op not in _OPERATORS:
                    raise ValueError(
                        "'{}' is not a valid operator.".format(op)
                    )
                if not _OPERATORS[op](record[key], val):
                    return False
        elif isinstance(qual, types.FunctionType):
            if not qual(record[key]):
                return False
        else:
            if key != qual:
                include = False
    return include

class jque:
    """
    A JSON query class that subsets the behavior of MongoDB queries.

    Uses $-notation for mongo operators.

        data = jque.jsonque([{
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
            "current_planet": "earth",
            "age": { "$lte": 20, "$gte": 10 }
        })
        """

    OPERATORS = _OPERATORS

    def __init__(self, data):
        """
        Create a new jque object. Pass `data`, which must be a
        string or a list. If a list, each item should be a dictionary.
        If a string, it can either be a JSON string (from Python's
        json.dumps or JS's JSON.stringify) or a filename that points
        to a .json file on disk.
        """
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                data = json.loads(open(data, 'r').read())
        elif not isinstance(data, list):
            raise ValueError("'data' argument must be a string or a list.")

        self.data = data

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)

    @synchronized
    def _sync_query(self, qr):
        filtered_data = {}
        for ind, record in enumerate(self.data):
            filtered_data[ind] = (_check_record(qr, record), record)
            if include:
                filtered_data.append(record)
        return [
            f[1] for f in filtered_data.values()
            if f[0]
        ]

    def query(self, qr, maintain_order=False, parallel=True, wrap=True):
        """
        Query the records for a desired trait.

        Arguments:
            qr (dict): a dict where all keys are included in all records.
            maintain_order (bool : False): If record order is important.
                Note: prevents parallelism, if available.
            parallel (bool : True): If the operations should be 
                parallelized, recordwise.
            wrap (bool : True): If the result should be rewrapped in a
                new jque object.
        """
        if not maintain_order and _run_parallel and parallel:
            return self._sync_query(qr)

        filtered_data = []
        for record in self.data:
            include = _check_record(qr, record)
            if include:
                filtered_data.append(record)
        if wrap:
            return jque(filtered_data)
        return filtered_data
