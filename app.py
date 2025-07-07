from client.db import PyDBClient
from client.exc import PYDBException

try:

    db = PyDBClient()

    db.connect()

    db.ping()

    # data = db.create(data={"first_name": "Hello", "age": 324}, table="user")

    db.drop_table(table="user")

except PYDBException as e:
    print(e, e.ref_data or "")


# print(data)
# data = db.find(query={"first_name": "HIIII"}, table="user")

# print("data >>> ", data)


# schema_def = {
#     "first_name": {
#         "type": "str",
#         "required": True,
#         "min_length": 2,
#         "max_length": 20,
#         "pattern": "^[a-zA-Z]+$",
#         "unique": True,
#     },

#     "age": {"unique": True,"type": "int", "required": True, "min": 18, "max": 99},
#     "salary": {"type": "float", "required": False, "min": 0.0},
#     "is_active": {"type": "bool", "required": False, "default": True},
#     "join_date": {"type": "date", "required": True},
#     "last_login": {"type": "datetime", "required": False},
# }
# db.create_table("user", schema_def)


# db.update(data={"sadasd": "sad"}, query={"Asd": "asd"})
# db.find(query={"Asd": "asd"})
# db.delete(query={"Asd": "asd"})

db.close()
