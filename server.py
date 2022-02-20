import socket

from pickle import dumps as pDumps, loads as pLoads
from threading import Thread

from settings import *
from logging import *
from player import Player

players = {}

class Server:
    """ This class represents the server. """

    def __init__(self) -> object:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.addr = (self.host, self.port)
        self.playerIndex = 0

    def start(self) -> None:
        try:
            self.socket.bind(self.addr)
        except Exception as e:
            errorMessage("Error trying to bind server")
            errorMessage(str(e))

        self.socket.listen(MAXIMUM_NUM_CONNECTIONS)
        infoMessage(f"Listening for connections on {self.port}")
        self.listenForConnections()

    def listenForConnections(self) -> None:
        while True:
            conn, clientAddress = self.socket.accept()
            infoMessage(f"Connection from {clientAddress}")
            clientThread = Thread(target=self.clientThread, args=(conn, clientAddress, self.playerIndex))
            clientThread.start()
            self.playerIndex += 1

    def clientThread(self, conn: socket.socket, clientAddress: tuple, playerIndex: int) -> None:
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

                playerList = {}

                # If the player is connected...
                if data:
                    # Send the states of all the players bar the player who sent the data
                    for player_idx in players:
                        player = players[player_idx]
                        if player != currentPlayer:
                            playerList[player_idx] = player
                else:
                    infoMessage(f"{clientAddress} has disconnected", colour="yellow")
                    connected = False
                    conn.sendall(pDumps([None]))

                conn.sendall(pDumps(playerList))

            except Exception as e:
                infoMessage(f"{clientAddress} has disconnected", colour="yellow")
                connected = False

        infoMessage(f"Ended threaded tasks for client: {clientAddress}")
        self.playerIndex -= 1
        del players[playerIndex]
        conn.close()

def main() -> None:
    server = Server()
    server.start()

if __name__ == "__main__":
    main()
