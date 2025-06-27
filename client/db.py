import socket


class PyDBClient:

    def __init__(self, host="127.0.0.1", port=9000):
        self.__connection = None

        self.host = host
        self.port = port

    def create(self, data, many=False):
        pass

    def find(self, query):
        pass

    def find_many(self, query):
        pass

    def update(self, query):
        pass

    def delete(self, query):
        pass

    def _recv_data(self, size=1024):
        connection = self.get_connection()
        while True:
            data = connection.recv(size)
            if not data:
                break

            return data.decode()

    def _send_data(self, data: str):

        connection = self.get_connection()
        connection.sendall(data.encode())

        return True

    def ping(self):

        self._send_data("PING")
        data = self._recv_data()
        print(data)

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
