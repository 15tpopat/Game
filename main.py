import pygame
import sys

from os import listdir

from settings import *
from player import Player
from libraries.network import Network

def takeScreenshot(screen: pygame.Surface) -> None:
    """ This function will take a screenshot of the game every time the function
        is called and will be used to help track the development of the game. """

    # Get the number to name the screenshot by adding 1 to the number of existing screenshots
    screenshotNumber = len(listdir(SCREENSHOT_PATH)) + 1

    # Save a snapshot of the screen to the screenshot directory
    pygame.image.save(screen, f"{SCREENSHOT_PATH}/screenshot #{screenshotNumber}.jpg")

def updateScreen(player: Player, playerList: dict) -> None:
    """ This function updates the screen by clearing the screen and drawing the
        sprites every time the function is called. """

    # Set the background colour
    screen.fill(BACKGROUND_COLOUR)

    # Draw the players on the screen
    player.draw(screen)
    for player in playerList.values():
        player.draw(screen)

    pygame.display.update()

def main(playerList: dict) -> None:
    """ This function contains the main game loop. """
    # Start game loop
    while True:
        # Event processing
        for event in pygame.event.get():
            # If they click the exit button, quit pygame and exit python
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Take a screenshot every time the equals button is pressed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_EQUALS:
                    takeScreenshot(screen)

        # Send the state of the player
        data = network.send({ "player": player })

        # If we receive data back...
        if data:
            playerList = data

        # Check if the player wants to move and move it
        player.move()

        # Update the screen
        updateScreen(player, playerList)

        # Limit the screen updates to FPS frames per second
        clock.tick(FPS)

if __name__ == "__main__":
    # Initialise pygame
    pygame.init()
    pygame.display.set_caption(CAPTION)

    # Manage how often the screen updates
    clock = pygame.time.Clock()

    # Initiate the screen with the given width and height
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screenRect = screen.get_rect()

    # Initiate the connection to the server and retrieve the player
    network = Network()
    player = network.player

    # Setup necessary variables
    playerList = {}

    # Run the main loop
    main(playerList)
