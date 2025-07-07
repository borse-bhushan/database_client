"""
Defines the ActionEnum class which contains constants representing various actions
that can be performed by the PyDBClient when communicating with the database server.
These are used to build and interpret requests and responses.
"""


class ActionEnum:
    """
    Enum-like class for supported database actions used in request/response payloads.
    Each attribute corresponds to a specific command or operation in the protocol.
    """

    PING = "PING"  # Health check operation
    CREATE = "CREATE"  # Insert a new row
    UPDATE = "UPDATE"  # Update existing rows
    DELETE = "DELETE"  # Delete rows
    SELECT = "SELECT"  # Query rows

    CREATE_TABLE = "CREATE_TABLE"  # Define and create a new table
    DROP_TABLE = "DROP_TABLE"  # Remove a table definition

    LOGIN = "LOGIN"  # Authenticate the client

    ERROR = "ERROR"  # Error response type
