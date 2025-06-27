from client.db import PyDBClient


db = PyDBClient()

db.connect()

db.ping()

db.close()
