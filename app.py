from datetime import datetime

from client.db import PyDBClient
from client.exc import PYDBException

db = PyDBClient()

db.connect()

try:
    db.drop_table(table="user")
except PYDBException as e:
    print(e)

try:
    schema_def = {
        "first_name": {
            "type": "str",
            "required": True,
            "min_length": 2,
            "max_length": 20,
            "pattern": "^[a-zA-Z]+$",
            "unique": True,
        },
        "age": {
            "type": "int",
            "required": True,
            "min": 18,
            "max": 99,
        },
        "salary": {
            "type": "float",
            "required": False,
            "min": 0.0,
        },
        "is_active": {
            "type": "bool",
            "required": False,
            "default": True,
        },
        "join_date": {"type": "datetime", "required": True, "format": "iso"},
    }
    db.create_table("user", schema_def)

    db.create(
        data={
            "age": 25,
            "salary": 3245,
            "is_active": True,
            "first_name": "Bhushan",
            "join_date": datetime.now().isoformat(),
        },
        table="user",
    )
    db.create(
        data={
            "age": 28,
            "salary": 324,
            "is_active": True,
            "first_name": "Vaibhav",
            "join_date": datetime.now().isoformat(),
        },
        table="user",
    )

    db.create(
        data={
            "age": 35,
            "salary": 324,
            "is_active": True,
            "first_name": "Shubham",
            "join_date": datetime.now().isoformat(),
        },
        table="user",
    )

    # Supports: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin
    results = db.find(
        table="user", query={"age": {"$gte": 24, "$lte": 35}, "first_name": "Bhushan"}
    )

    print("FIND: ", results)

    db.update(
        data={
            "age": 40,
        },
        query={"first_name": "Vaibhav"},
        table="user",
    )

    results = db.find(
        table="user",
        query={"first_name": "Vaibhav"},
    )

    print("After UPDATE", results)

    updated = db.delete(
        query={"first_name": "Vaibhav"},
        table="user",
    )

    results = db.find(table="user", query={})
    print("AFTER DELETE", results, len(results))


except PYDBException as e:
    print(e, e.ref_data or "")


db.close()
