# jsonque

Query JSON in memory as though it were a Mongo database.


```python
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
```
