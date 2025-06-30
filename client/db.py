import json

from .constants import ActionEnum
from .singleton import SingletonMeta

from .cn_mgt import DBConnection


class PyDBClient(metaclass=SingletonMeta):

    def __init__(self, host="127.0.0.1", port=9000):
        self.__connection = DBConnection(host=host, port=port)

    def create(self, data):

        req_payload = self._construct_payload(ActionEnum.CREATE, payload=data)

        self._send(req_payload)

        return self._recv_data()

    def find(self, query):

        req_payload = self._construct_payload(ActionEnum.SELECT, query=query)

        self._send(req_payload)

        return self._recv_data()

    def update(self, query, data):

        req_payload = self._construct_payload(
            ActionEnum.UPDATE, query=query, payload=data
        )
        self._send(req_payload)

        return self._recv_data()

    def delete(self, query):
        req_payload = self._construct_payload(ActionEnum.DELETE, query=query)
        self._send(req_payload)
        return self._recv_data()

    def _send(self, data: str):
        return self.get_connection().send(data)

    def _recv_data(self):
        return json.loads(self.get_connection().recv_data())

    def ping(self):

        self._send(self._construct_payload(ActionEnum.PING))

        data = self._recv_data()

        print(data["payload"]["message"])

        return True

    @staticmethod
    def _construct_payload(action, query=None, payload=None):
        return json.dumps({"query": query, "action": action, "payload": payload})

    def close(self):
        self.get_connection().close()

    def get_connection(self):
        return self.__connection

    def connect(self):
        self.get_connection().connect()
        return True
