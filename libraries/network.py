import socket
from pickle import dumps as pDumps, loads as pLoads

from settings import *
from player import Player

class Network:
    """ This class represents the the client interface to the server. """
    def __init__(self) -> object:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.addr = (self.host, self.port)
        self.player = self.connect()

    def connect(self) -> Player:
        try:
            self.socket.connect(self.addr)
            return pLoads(self.socket.recv(DATA_SIZE))
        except socket.error as e:
            print("[NETWORK ERROR] An error occurred whilst trying to connect to the server: \n\t", e)
            print("[NETWORK INFO] The server is most likely not started")

    def send(self, data: dict) -> dict:
        self.socket.send(pDumps(data))
        return pLoads(self.socket.recv(DATA_SIZE))
