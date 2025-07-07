"""
This module provides the PyDBClient class, which acts as a client interface
for interacting with a custom-built Python-based database over a socket connection.

Supported operations include:
- Table creation and deletion
- Row creation, querying, updating, and deletion
- Authentication and session handling
"""

import json

from .utils import get_uuid
from .exc import PYDBException
from .cn_mgt import DBConnection
from .constants import ActionEnum


class PyDBClient:
    """
    Client interface for communicating with the custom Python database server.

    Handles authentication, command construction, and transmission of data
    over a socket connection.
    """

    def __init__(
        self,
        host="127.0.0.1",
        port=9000,
        database="py_db",
        username="root",
        password="root@123",
    ):
        """
        Initialize the PyDBClient with connection details and credentials.

        Args:
            host (str): Host address of the DB server.
            port (int): Port number of the DB server.
            database (str): Database name to connect to.
            username (str): Username for authentication.
            password (str): Password for authentication.
        """
        self.database = database
        self.username = username
        self.password = password

        self.auth_token = None

        self.__connection = DBConnection(
            host=host,
            port=port,
        )

    def create(self, table, data):
        """
        Insert a new row into a given table.

        Args:
            table (str): Table name.
            data (dict): Row data to insert.

        Returns:
            dict: Payload returned by the server.
        """
        if not "pk" in data:
            data["pk"] = get_uuid()

        req_payload = self._construct_payload(
            table=table,
            payload=data,
            action=ActionEnum.CREATE,
        )

        self._send(req_payload)

        return self._recv_data()["payload"]

    def create_table(self, table, schema):
        """
        Create a new table with the provided schema.

        Args:
            table (str): Table name.
            schema (dict): Schema definition for the table.

        Returns:
            dict: Payload returned by the server.
        """
        req_payload = self._construct_payload(
            table=table,
            payload=schema,
            action=ActionEnum.CREATE_TABLE,
        )

        self._send(req_payload)

        return self._recv_data()["payload"]

    def find(self, query, table):
        """
        Query data from a table based on the given filter.

        Args:
            query (dict): Query filters.
            table (str): Table name.

        Returns:
            dict: Response data from the server.
        """
        req_payload = self._construct_payload(
            ActionEnum.SELECT, query=query, table=table
        )

        self._send(req_payload)

        return self._recv_data()

    def update(self, query, data, table):
        """
        Update rows in a table that match the query.

        Args:
            query (dict): Query filters.
            data (dict): Data to update.
            table (str): Table name.

        Returns:
            dict: Response data from the server.
        """
        req_payload = self._construct_payload(
            ActionEnum.UPDATE,
            query=query,
            payload=data,
            table=table,
        )
        self._send(req_payload)

        return self._recv_data()

    def delete(self, query, table):
        """
        Delete rows from a table based on the query.

        Args:
            query (dict): Query filters.
            table (str): Table name.

        Returns:
            dict: Response data from the server.
        """
        req_payload = self._construct_payload(
            ActionEnum.DELETE,
            query=query,
            table=table,
        )
        self._send(req_payload)
        return self._recv_data()

    def _send(self, data: str):
        """
        Send a serialized request to the database server.

        Args:
            data (str): JSON-serialized request payload.
        """
        return self.get_connection().send(data)

    def _recv_data(self, handle_error=True):
        """
        Receive and deserialize response data from the server.

        Args:
            handle_error (bool): Whether to raise exceptions on error responses.

        Returns:
            dict: Parsed response data.
        """
        resp_data = json.loads(self.get_connection().recv_data())

        if resp_data["action_type"] == ActionEnum.ERROR and handle_error:
            self.handle_error(resp_data["payload"])

        return resp_data

    def ping(self):
        """
        Send a ping to verify the server is reachable.

        Returns:
            bool: True if successful.
        """
        self._send(self._construct_payload(ActionEnum.PING))

        data = self._recv_data()
        print(data["payload"]["message"])

        return True

    def _construct_payload(self, action, query=None, payload=None, table=None):
        """
        Construct a standardized payload for a database request.

        Args:
            action (str): Action type (e.g., SELECT, CREATE).
            query (dict, optional): Query filter.
            payload (dict, optional): Data payload.
            table (str, optional): Table name.

        Returns:
            str: JSON-encoded payload.
        """
        return json.dumps(
            {
                "table": table,
                "query": query,
                "action": action,
                "payload": payload,
                "auth": self.auth_token,
            }
        )

    def close(self):
        """
        Close the current connection to the database server.
        """
        self.get_connection().close()

    def get_connection(self):
        """
        Retrieve the underlying DB connection object.

        Returns:
            DBConnection: The connection instance.
        """
        return self.__connection

    def connect(self):
        """
        Establish connection and authenticate with the database server.

        Returns:
            bool: True if successful.
        """
        self.get_connection().connect()

        self._login()
        return True

    def handle_error(self, error_details):
        """
        Handle errors received from the server.

        Args:
            error_details (dict): Error response from the server.

        Raises:
            PYDBException: Custom exception with server-provided details.
        """
        self.close()
        raise PYDBException(**error_details)

    def _login(self):
        """
        Perform authentication using provided credentials.

        Returns:
            bool: True if login is successful.
        """
        payload = self._construct_payload(
            ActionEnum.LOGIN,
            payload={
                "user": self.username,
                "password": self.password,
                "database": self.database,
            },
        )

        self._send(payload)
        recv = self._recv_data()

        self.auth_token = recv["payload"]

        return True

    def drop_table(self, table):
        """
        Drop the specified table from the database.

        Args:
            table (str): Table name.

        Returns:
            dict: Server response after dropping the table.
        """
        payload = self._construct_payload(
            table=table,
            action=ActionEnum.DROP_TABLE,
        )

        self._send(payload)

        return self._recv_data()
