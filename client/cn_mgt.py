import socket

from .singleton import SingletonMeta


class DBConnection(metaclass=SingletonMeta):

    def __init__(self, host="127.0.0.1", port=9000):
        self.__connection = None

        self.host = host
        self.port = port

    def recv_data(self):
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
                    # self.send("Invalid QUERY_LENGTH header")
                    return
                break

        if query_length is None:
            raise ValueError("QUERY_LENGTH header missing")
            return

        # Read the rest of the body if not fully received
        while len(body) < query_length:
            chunk = connection.recv(1024)
            if not chunk:
                break
            body += chunk

        # Now body contains the full data of length query_length
        query_data = body[:query_length]

        # Example: echo back the received data length
        query_data = query_data.decode()

        print("query_data >>> ", query_data, type(query_data))
        return query_data

    def send(self, data: str):

        connection = self.get_connection()

        header = f"QUERY_LENGTH: {len(data)}\r\n\r\n"
        connection.sendall((header + data).encode())

        return True

    def close(self):
        self.get_connection().close()

    def connect(self):

        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection.connect((self.host, self.port))

        return self

    def get_connection(self):

        if self.__connection is None:
            raise ConnectionError("Connection not established. Call connect() first.")
        return self.__connection
