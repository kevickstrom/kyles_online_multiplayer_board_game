# network for online monopoly

import socket
import pickle
from game import Game


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.0.0.88"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        """
        Initial connection
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data: str) -> Game:
        """
        Used to send string data over socket
        Don't think this will be used anymore
        :param data: string message
        :return: Game object
        """
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)

    def update(self, data: object) -> Game:
        """
        Used to send object data over socket
        :param data: Player object
        :return: Game object
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            print(e)
