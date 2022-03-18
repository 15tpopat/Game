import pygame
import sys

from json import dump as jDump, load as jLoad
from os import listdir
from random import randint

from settings import *
from libraries.network import Network
from libraries.player import Player
from libraries.jutsu import *

class Crosshair:
    """ This class represents the crosshair. """

    def __init__(self) -> object:
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.rect = pygame.Rect(self.x, self.y, CROSSHAIR_WIDTH, CROSSHAIR_HEIGHT)

    def update(self) -> None:
        # Retrieve the position of the mouse
        xPosition, yPosition = pygame.mouse.get_pos()

        # Set the position of the crosshair to the mouse
        self.rect.x = xPosition - (CROSSHAIR_WIDTH // 2)
        self.rect.y = yPosition - (CROSSHAIR_HEIGHT // 2)

def loadImage(name: str) -> pygame.Surface:
    """ Load the image and convert it into the same pixel format as the one used
        by pygame so that it can be drawn faster. """

    image = pygame.image.load(f"{IMAGES_PATH}/{name}.png").convert_alpha()
    image.set_colorkey((0, 0, 0))
    return image

def scale(image: pygame.Surface, size: tuple) -> pygame.Surface:
    """ Scale the image given to the desired resolution specified. """

    image = pygame.transform.scale(image, size)
    return image

def takeScreenshot(screen: pygame.Surface) -> None:
    """ This function will take a screenshot of the game every time the function
        is called and will be used to help track the development of the game. """

    # Create an anonymous function to stop hidden files being counted
    discardHiddenFiles = lambda files : [file for file in files if not file.startswith(".")]

    # Get the number to name the screenshot by adding 1 to the number of existing screenshots
    screenshotNumber = len(discardHiddenFiles(listdir(SCREENSHOT_PATH))) + 1

    # Save a snapshot of the screen to the screenshot directory
    pygame.image.save(screen, f"{SCREENSHOT_PATH}/screenshot #{screenshotNumber}.jpg")

def updateScreen(crosshair: Crosshair, player: Player, playerList: dict, jutsuList: list) -> None:
    """ This function updates the screen by clearing the screen and drawing the
        sprites every time the function is called. """

    # Set the background image
    screen.blit(images["background"], screenRect)

    # Draw the crosshair on the screen
    screen.blit(images["crosshair"], crosshair.rect)

    # Draw the players and jutsu on the screen
    player.draw(screen)
    for playerObject in playerList.values():
        playerObject.draw(screen)
    for jutsuObject in jutsuList.values():
        jutsuObject.draw(screen)

    pygame.display.update()

def main(crosshair: Crosshair, activatedJutsu: str, playerList: dict, jutsuList: list, jutsuIndex: dict) -> None:
    """ This function contains the main game loop. """

    # Start game loop
    while True:
        # Event processing
        for event in pygame.event.get():
            # If they click the exit button, quit pygame and exit python
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # On key up...
            elif event.type == pygame.KEYUP:
                # Take a screenshot every time the equals button is pressed
                if event.key == pygame.K_EQUALS:
                    takeScreenshot(screen)

                # Allow the player to mould the chakra into a jutsu
                jutsuKey = player.mould(event, jutsuIndex)

                # If the player has finished moulding...
                if jutsuKey is not None:
                    # Change the jutsu
                    activatedJutsu = jutsuKey

            # Launch a jutsu when the left mouse button is pressed down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    jutsuID = randint(0, JUTSU_ID_RANGE)

                    jutsu = Jutsu(player.rect, 10, 10, jutsuID, event.pos)
                    if activatedJutsu == "fireball_jutsu":
                        jutsu = FireballJutsu(player.rect, 10, 10, jutsuID, event.pos)
                    elif activatedJutsu == "mud_wall":
                        jutsu = MudWall(player.rect, 10, 10, jutsuID, event.pos)
                    elif activatedJutsu == "gale_palm":
                        jutsu = GalePalm(player.rect, 10, 10, jutsuID, event.pos)
                    elif activatedJutsu == "mist_barrier":
                        jutsu = MistBarrier(player.rect, 10, 10, jutsuID, event.pos)
                    elif activatedJutsu == "limelight_minor":
                        jutsu = Limelight(player.rect, 10, 10, jutsuID, event.pos)
                    else:
                        pass

                    jutsuList[jutsuID] = jutsu

        # Send the state of the player
        data = network.send({ "player": player, "jutsu": jutsuList })

        # If we receive data back...
        if data:
            playerList, jutsuList = data

        # Update the states of the player, crosshair and jutsu objects
        player.move()
        crosshair.update()

        for jutsuObject in jutsuList.values():
            # Remove the jutsu if it goes off the screen
            if (jutsuObject.rect.x < -screenWidthBorder or jutsuObject.rect.x > SCREEN_WIDTH + screenWidthBorder) or \
               (jutsuObject.rect.y < -screenHeightBorder or jutsuObject.rect.y > SCREEN_HEIGHT + screenHeightBorder):
                jutsuObject.remove = True
            else:
                jutsuObject.update()

        # Update the screen
        updateScreen(crosshair, player, playerList, jutsuList)

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

    # Ensure that the mouse is invisible whilst still moving the crosshair
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    # Initiate the connection to the server and retrieve the player
    network = Network()
    player = network.player

    # Setup necessary files, images, objects and variables
    with open(DATABASE_PATH, "r") as file:
        db = jLoad(file)

    backgroundImage = scale(loadImage("background"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    crosshairImage = scale(loadImage("crosshair"), (CROSSHAIR_WIDTH, CROSSHAIR_HEIGHT))

    crosshair = Crosshair()

    activatedJutsu = DEFAULT_ACTIVATED_JUTSU
    playerList = {}
    jutsuList = {}
    images = {
        "background": backgroundImage,
        "crosshair": crosshairImage
    }

    # At what point beyond the border should the jutsu be deleted
    screenWidthBorder = SCREEN_WIDTH * SCREEN_BORDER_MULTIPLIER
    screenHeightBorder = SCREEN_HEIGHT * SCREEN_BORDER_MULTIPLIER

    # Allows for quicker and easier retrieval of jutsu for the keyboard input method
    jutsuIndex = {}
    for jutsu in db["jutsu"]:
        for text in db["jutsu"][jutsu]["texts"]:
            jutsuIndex[text] = jutsu

    # Run the main loop
    main(crosshair, activatedJutsu, playerList, jutsuList, jutsuIndex)
