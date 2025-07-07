from datetime import datetime

from client.db import PyDBClient
from client.exc import PYDBException

try:

    db = PyDBClient()

    db.connect()

    # db.drop_table(table="user")

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
    # db.create_table("user", schema_def)

    # data = db.create(
    #     data={
    #         "age": 21,
    #         "salary": 34345.345,
    #         "is_active": True,
    #         "first_name": "world",
    #         "join_date": datetime.now().isoformat(),
    #     },
    #     table="user",
    # )

    # updated = db.update(
    #     data={
    #         "age": 40,
    #         # "salary": 34345.345,
    #         # "is_active": True,
    #         # "first_name": "Hello",
    #         # "join_date": datetime.now().isoformat(),
    #     },
    #     query={"first_name": "World"},
    #     table="user",
    # )

    updated = db.delete(
        query={"first_name": "World"},
        table="user",
    )

    print(updated)

    # db.drop_table(table="user")

except PYDBException as e:
    print(e, e.ref_data or "")


# print(data)
# data = db.find(query={"first_name": "HIIII"}, table="user")

# print("data >>> ", data)


# db.update(data={"sadasd": "sad"}, query={"Asd": "asd"})
# db.find(query={"Asd": "asd"})
# db.delete(query={"Asd": "asd"})

db.close()
