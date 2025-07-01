from client.db import PyDBClient


db = PyDBClient()

db.connect()

db.ping()

# db.create(data={"sadasd": "sad"})
# db.update(data={"sadasd": "sad"}, query={"Asd": "asd"})
# db.find(query={"Asd": "asd"})
# db.delete(query={"Asd": "asd"})

db.close()
