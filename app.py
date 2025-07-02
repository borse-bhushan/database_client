from client.db import PyDBClient


db = PyDBClient()

db.connect()

db.ping()

data = db.create(data={"first_name": "hello"}, table="user")

print("data >>> ", data)

# db.update(data={"sadasd": "sad"}, query={"Asd": "asd"})
# db.find(query={"Asd": "asd"})
# db.delete(query={"Asd": "asd"})

db.close()
