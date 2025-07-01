import json


from .exc import PYDBException
from .cn_mgt import DBConnection
from .constants import ActionEnum
from .singleton import SingletonMeta


class PyDBClient(metaclass=SingletonMeta):

    def __init__(
        self,
        host="127.0.0.1",
        port=9000,
        database="py_db",
        username="root",
        password="root@123",
    ):
        self.database = database
        self.username = username
        self.password = password

        self.auth_token = None

        self.__connection = DBConnection(
            host=host,
            port=port,
        )

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

    def _recv_data(self, handle_error=True):
        resp_data = json.loads(self.get_connection().recv_data())

        if resp_data["action_type"] == ActionEnum.ERROR and handle_error:
            self.handle_error(resp_data["payload"])

        return resp_data

    def ping(self):

        self._send(self._construct_payload(ActionEnum.PING))

        data = self._recv_data()
        print(data["payload"]["message"])

        return True

    def _construct_payload(self, action, query=None, payload=None):
        return json.dumps(
            {
                "query": query,
                "action": action,
                "payload": payload,
                "auth": (
                    {
                        "token": self.auth_token,
                    }
                    if self.auth_token
                    else None
                ),
            }
        )

    def close(self):
        self.get_connection().close()

    def get_connection(self):
        return self.__connection

    def connect(self):
        self.get_connection().connect()

        self._login()
        return True

    def handle_error(self, error_details):
        raise PYDBException(**error_details)

    def _login(self):

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
