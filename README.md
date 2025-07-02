# 🗄️ Database Client

A Python client for connecting to and interacting with a custom database server.
Easily perform CRUD operations, manage connections, and handle errors with a simple API.

## 🚀 Features

- Singleton-based client and connection management
- Simple CRUD operations: Create, Read, Update, Delete
- Custom exception handling
- Easy authentication and connection setup
- Modular and extensible codebase

## 📦 Installation

Clone this repository:

```sh
git clone https://github.com/borse-bhushan/database_client.git
cd database_client
```

## 🛠️ Usage

```python
from client.db import PyDBClient

db = PyDBClient()
db.connect()

db.ping()  # 🏓 Check server connectivity

# Create a record
db.create(data={"key": "value"})

# Find records
db.find(query={"key": "value"})

# Update records
db.update(query={"key": "value"}, data={"key": "new_value"})

# Delete records
db.delete(query={"key": "value"})

db.close()
```

## ⚙️ Configuration

You can customize the connection parameters:

```python
db = PyDBClient(
    host="127.0.0.1",
    port=9000,
    database="py_db",
    username="root",
    password="root@123"
)
```

## 🧩 Project Structure

```bash
database_client/
├── app.py
├── client/
│   ├── cn_mgt.py
│   ├── constants.py
│   ├── db.py
│   ├── singleton.py
│   └── exc/
│       ├── base.py
│       ├── cmn_exc.py
│       ├── codes.py
│       └── err_msg.py
├── README.md
└── LICENSE
```

## 📝 License

Licensed under the [Apache License 2.0](LICENSE).

---

**🚧 Work in progress.** Contributions and feedback are welcome! 🙌

## 👨‍💻 Author

- 🧑‍💻 Bhushan Borse
