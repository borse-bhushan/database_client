"""
db_connection.py

This module provides the DBConnection class responsible for managing a singleton
TCP socket connection to the custom database server. It handles sending and
receiving data with a custom protocol that includes headers and body.
"""

import socket

from .singleton import SingletonMeta


class DBConnection(metaclass=SingletonMeta):
    """
    Manages a singleton socket connection to the database server using a custom protocol.

    Ensures only one connection instance exists using the SingletonMeta metaclass.
    """

    def __init__(self, host="127.0.0.1", port=9000):
        """
        Initialize the DBConnection with host and port details.

        Args:
            host (str): Hostname or IP of the server.
            port (int): Port number to connect to.
        """
        self.__connection = None

        self.host = host
        self.port = port

    def recv_data(self):
        """
        Receive and parse data from the socket connection using the custom protocol.

        Returns:
            str: The full decoded query data received from the server.

        Raises:
            ValueError: If QUERY_LENGTH header is missing or invalid.
        """
        connection = self.get_connection()

        buffer = b""
        # Read initial chunk
        chunk = connection.recv(1024)
        if not chunk:
            return

        buffer += chunk

        # Find the header delimiter
        delimiter = b"\r\n\r\n"
        header_end = buffer.find(delimiter)
        if header_end == -1:
            # Header not fully received yet, keep reading until we get it
            while header_end == -1:
                chunk = connection.recv(1024)
                if not chunk:
                    return
                buffer += chunk
                header_end = buffer.find(delimiter)

        # Extract header and body
        header = buffer[:header_end].decode()
        body = buffer[header_end + len(delimiter) :]

        # Parse query length from header
        query_length = None
        for line in header.splitlines():
            if line.startswith("QUERY_LENGTH"):
                try:
                    query_length = int(line.split(":")[1].strip())
                except (IndexError, ValueError):
                    raise ValueError("QUERY_LENGTH is not valid")
                break

        if query_length is None:
            raise ValueError("QUERY_LENGTH header missing")

        # Read the rest of the body if not fully received
        while len(body) < query_length:
            chunk = connection.recv(1024)
            if not chunk:
                break
            body += chunk

        # Now body contains the full data of length query_length
        query_data = body[:query_length]

        # Decode the received data
        query_data = query_data.decode()

        return query_data

    def send(self, data: str):
        """
        Send data to the server with the custom QUERY_LENGTH header.

        Args:
            data (str): The JSON string or command to send.

        Returns:
            bool: True if data is sent successfully.
        """
        connection = self.get_connection()

        header = f"QUERY_LENGTH: {len(data)}\r\n\r\n"
        connection.sendall((header + data).encode())

        return True

    def close(self):
        """
        Close the current socket connection.
        """
        self.get_connection().close()

    def connect(self):
        """
        Establish a new socket connection to the database server.

        Returns:
            DBConnection: The current instance for chaining.
        """
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection.connect((self.host, self.port))

        return self

    def get_connection(self):
        """
        Retrieve the active socket connection.

        Returns:
            socket.socket: The active socket object.

        Raises:
            ConnectionError: If the connection is not yet established.
        """
        if self.__connection is None:
            raise ConnectionError("Connection not established. Call connect() first.")
        return self.__connection
