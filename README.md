# 🗄️ Database Client

A Python client library for interacting with a custom TCP-based database server.
Provides a high-level API for table management, CRUD operations, authentication, and robust error handling over a socket connection.

---

## 📚 Overview

`database_client` is designed to connect to a custom database server using a custom protocol over TCP sockets.
It features singleton-based connection management, a clear and extensible API, and a modular codebase with custom exceptions and utilities.

---

## 🏗️ Architecture

- **Singleton Connection:** Ensures only one socket connection per client using a thread-safe singleton pattern.
- **Custom Protocol:** Communicates with the server using a protocol with headers (e.g., `QUERY_LENGTH`) and JSON payloads.
- **Authentication:** Handles login and session token management.
- **CRUD & Table Operations:** Supports creating, querying, updating, and deleting rows, as well as creating and dropping tables.
- **Custom Exceptions:** Provides a hierarchy of exceptions for robust error handling.
- **Utility Functions:** Includes helpers such as UUID generation for primary keys.

---

## 🗂️ Project Structure

```sh
database_client/
├── client/
│   ├── __init__.py
│   ├── cn_mgt.py         # DBConnection: manages TCP socket connection
│   ├── constants.py      # ActionEnum: protocol action constants
│   ├── db.py             # PyDBClient: main client API
│   ├── singleton.py      # SingletonMeta: thread-safe singleton metaclass
│   ├── exc/
│   │   ├── __init__.py
│   │   ├── base.py       # BaseExc: base exception class
│   │   ├── cmn_exc.py    # PYDBException: common exception
│   │   ├── codes.py      # Error code constants
│   │   └── err_msg.py    # Error message constants
│   └── utils/
│       ├── __init__.py
│       └── cmn_fun.py    # get_uuid: UUID generator
```

---

## 📝 Key Components

### `PyDBClient` ([client/db.py](client/db.py))

A high-level client for interacting with the database server.
Handles authentication, command construction, sending/receiving data, and error handling.

**Main methods:**

- `connect()`: Establish connection and authenticate.
- `create(table, data)`: Insert a new row (auto-generates `pk` if missing).
- `find(query, table)`: Query rows.
- `update(query, data, table)`: Update rows matching query.
- `delete(query, table)`: Delete rows matching query.
- `create_table(table, schema)`: Create a new table.
- `drop_table(table)`: Drop a table.
- `ping()`: Check server connectivity.
- `close()`: Close the connection.

### `DBConnection` ([client/cn_mgt.py](client/cn_mgt.py))

Manages a singleton TCP socket connection to the server, handling the custom protocol for sending and receiving data.

### `SingletonMeta` ([client/singleton.py](client/singleton.py))

Thread-safe singleton metaclass to ensure only one instance of connection/client exists.

### `ActionEnum` ([client/constants.py](client/constants.py))

Enum-like class for all supported protocol actions (e.g., `PING`, `CREATE`, `SELECT`, `LOGIN`, etc.).

### Exception Handling ([client/exc/](client/exc/))

- `BaseExc`: Base exception class.
- `PYDBException`: Raised for server-side or protocol errors.
- Error codes and messages are centralized for consistency.

### Utilities ([client/utils/](client/utils/))

- `get_uuid()`: Generates a UUID string for use as a primary key.

---

## 🚀 Features

- Singleton-based, thread-safe connection management
- Custom protocol with headers and JSON payloads
- Table and row CRUD operations
- Authentication and session management
- Robust, extensible error handling
- Utility functions for common tasks

---

## 📦 Installation

Clone this repository:

```sh
git clone https://github.com/yourusername/database_client.git
cd database_client
```

---

## 🛠️ Usage

```python
from client.db import PyDBClient

# Instantiate the client
client = PyDBClient(
    host="127.0.0.1",
    port=9000,
    database="py_db",
    username="root",
    password="root@123"
)

# Connect and authenticate
client.connect()

# Ping the server
client.ping()

# Create a table
schema = {
    "fields": {
        "pk": "str",
        "name": "str",
        "age": "int"
    }
}
client.create_table("users", schema)

# Insert a row (pk auto-generated if not provided)
client.create("users", {"name": "Alice", "age": 30})

# Query rows
results = client.find({"name": "Alice"}, "users")

# Update rows
client.update({"name": "Alice"}, {"age": 31}, "users")

# Delete rows
client.delete({"name": "Alice"}, "users")

# Drop the table
client.drop_table("users")

# Close the connection
client.close()
```

---

## ⚙️ Configuration

You can customize the connection parameters when instantiating `PyDBClient`:

- `host`: Database server host (default: `"127.0.0.1"`)
- `port`: Database server port (default: `9000`)
- `database`: Database name (default: `"py_db"`)
- `username`: Username (default: `"root"`)
- `password`: Password (default: `"root@123"`)

---

## 📝 License

Licensed under the [Apache License 2.0](LICENSE).

---

## 👨‍💻 Author

- Bhushan Borse
