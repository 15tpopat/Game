import socket

from pickle import dumps as pDumps, loads as pLoads
from threading import Thread

from settings import *
from logging import *
from libraries.player import Player
from libraries.jutsu import *

players = {}
jutsu = {}

class Server:
    """ This class represents the server. """

    def __init__(self) -> object:
        # Create an IPV4 TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the network attributes
        self.host = HOST
        self.port = PORT
        self.addr = (self.host, self.port)

        # Set the game tracking attributes
        self.playerIndex = 0

    def start(self) -> None:
        # Try to create a socket to an unbinded address
        # If the address is already binded, an error will occur
        try:
            self.socket.bind(self.addr)
        except Exception as e:
            errorMessage("Error trying to bind server", end=": ")
            errorMessage(str(e), prefix=False)

        # Only allow for a certain number of connections
        self.socket.listen(MAXIMUM_NUM_CONNECTIONS)
        infoMessage(f"Listening for connections on {self.port}")
        self.listenForConnections()

    def listenForConnections(self) -> None:
        while True:
            # Accept incoming connections and create a new thread for each connection
            conn, clientAddress = self.socket.accept()
            infoMessage(f"Connection from {clientAddress}")
            clientThread = Thread(target=self.clientThread, args=(conn, clientAddress, self.playerIndex))
            clientThread.start()

            # Increment the player ID
            self.playerIndex += 1

    def clientThread(self, conn: socket.socket, clientAddress: tuple, playerIndex: int) -> None:
        global jutsu

        # Create the player and add them to the list containing all players
        player = Player(
            "Sasuke",       # Name
            80.0,           # Health
            60.0,           # Chakra
            90,             # Maximum Chakra
            0.2,            # Recharge Rate
            "lightning",    # Primary Affinity
            "fire",         # Secondary Affinity
        )
        players[playerIndex] = player
        currentPlayer = players[playerIndex]

        # Send the initial player object to the newly connected client
        conn.send(pDumps(players[playerIndex]))
        infoMessage(f"Started thread with player index: {playerIndex}")

        # Whilst the player is connected...
        connected = True
        while connected:
            try:
                # Receive the updated state of the player
                data = pLoads(conn.recv(DATA_SIZE))
                players[playerIndex] = data["player"]

                # Reset the player list
                playerList = {}

                # If the player is connected...
                if data:
                    # Send the states of all the players bar the player who sent the data
                    for playerKey in players:
                        player = players[playerKey]
                        if player != currentPlayer:
                            playerList[playerKey] = player

                    # Send the states of all the jutsu
                    jutsuList = data["jutsu"]
                    for jutsuObject in jutsuList.values():
                        if jutsuObject.remove:
                            try:
                                del jutsu[jutsuObject.jutsuID]
                            except KeyError:
                                pass
                        else:
                            jutsu[jutsuObject.jutsuID] = jutsuObject
                else:
                    # If no data is received, the client has disconnected
                    infoMessage(f"{clientAddress} has disconnected", colour="yellow")
                    connected = False
                    conn.sendall(pDumps([None, None]))

                # Send the data back to the client
                conn.sendall(pDumps([playerList, jutsu]))

            except Exception as e:
                # If we can't send data to the client, the client has disconnected
                errorMessage(f"{clientAddress} has disconnected", end=": ")
                errorMessage(str(e), prefix=False)
                connected = False

        # Decrement the player ID and delete the respective player object
        infoMessage(f"Ended threaded tasks for client: {clientAddress}")
        self.playerIndex -= 1
        del players[playerIndex]
        conn.close()

def main() -> None:
    """ This function contains the server initialisation and start code. """

    server = Server()
    server.start()

if __name__ == "__main__":
    main()
