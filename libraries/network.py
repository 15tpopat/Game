import socket
import sys

from pickle import dumps as pDumps, loads as pLoads

from settings import *
from logging import *

class Network:
    """ This class represents the client interface to the server. """

    def __init__(self) -> object:
        # Create an IPV4 TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the network attributes
        self.host = HOST
        self.port = PORT
        self.addr = (self.host, self.port)

        # Connect to the server and receive the initial player object
        self.player = self.connect()

    def connect(self) -> object:
        try:
            # Try and connect to the server
            self.socket.connect(self.addr)

            # Receive the initial player object
            return pLoads(self.socket.recv(DATA_SIZE))
        except socket.error as e:
            # If an error occurs, it likely means that the server is not listening for connections
            errorMessage("An error occurred whilst trying to connect to the server", end=": ")
            errorMessage(str(e), prefix=False)
            infoMessage("The server is most likely not started")
            sys.exit()

    def send(self, data: dict) -> dict:
        # Send the data to the server and receive data back
        self.socket.send(pDumps(data))
        return pLoads(self.socket.recv(DATA_SIZE))
