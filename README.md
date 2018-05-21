<h2 align=center>j q u e</h2>
<p align=center>Query JSON in memory as though it were a Mongo database</p>
<p align=center><a href="https://circleci.com/gh/j6k4m8/jque">CircleCI: <img src="https://circleci.com/gh/j6k4m8/jque.svg?style=svg" /></a></p>

## Installation

```shell
pip3 install jque
```

## Usage

```python
import jque
```

`jque` accepts a variety of inputs to the constructor.

Pass a list of dicts:
```python
data = jque.jque([{ "name": "jque" }])
```

Pass a JSON filename:
```python
DATAFILE = "~/my/big/data.json"
data = jque.jque(DATAFILE)
```

Now you can query this dataset using Mongo-like syntax:
```python
data.query({ "name": {"$neq": "numpy"} })
```

### Arguments to `query`:

| Arg | Description |
|-----|-------------|
| `wrap` (`boolean` : `True`) | Whether to wrap the resultant dataset in a new `jque` object. This allows chaining, like `jque.query(...).query(...)`, if you're the sort of person to do that. Pass `False` to get back a `list` instead. |

### 


```python
data = jque.jque([{
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
```


Use Python lambdas as a filter:

```python
libraries = jque.jque([{"name": "jque", "language": "Python"}, {"name": "react", "language": "node"}])
list(libraries.query({ 'language': lambda x: x[:2] == "Py" }))
```

