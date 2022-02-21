import pygame
import sys

from os import listdir

from settings import *
from player import Player
from libraries.network import Network

class Jutsu:
    """ This class represents the jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        width: int,
        height: int,
        mousePosition: tuple
    ) -> object:
        # Set the technical jutsu attributes
        self.x = playerRect.center[0]
        self.y = playerRect.center[1]
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.colour = JUTSU_COLOUR

        # Calculate the trajectory of the jutsu
        self.playerPosition = pygame.math.Vector2(player.rect.center) # duplicate # start position in start of canon
        distance = mousePosition - self.playerPosition
        self.velocity = distance.normalize() * JUTSU_SPEED

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the sprite onto the screen
        pygame.draw.rect(screen, self.colour, self.rect)

    def update(self) -> None:
        # Update the position attributes used to draw the sprite
        self.playerPosition += self.velocity
        self.rect.x = self.playerPosition.x
        self.rect.y = self.playerPosition.y

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
    for player in playerList.values():
        player.draw(screen)
    for jutsu in jutsuList:
        jutsu.draw(screen)

    pygame.display.update()

def main(crosshair: Crosshair, playerList: dict, jutsuList: list) -> None:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    jutsu = Jutsu(player.rect, 10, 10, event.pos)
                    jutsuList.append(jutsu)

        # Send the state of the player
        data = network.send({ "player": player })

        # If we receive data back...
        if data:
            playerList = data

        # Update the states of the player, crosshair and jutsu objects
        player.move()
        crosshair.update()

        for jutsu in jutsuList:
            # Remove the jutsu if it goes off the screen
            if (jutsu.rect.x < 0 or jutsu.rect.x > SCREEN_WIDTH) or \
               (jutsu.rect.y < 0 or jutsu.rect.y > SCREEN_HEIGHT):
                jutsuList.remove(jutsu)
            else:
                jutsu.update()

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

    # Setup necessary images, objects and variables
    backgroundImage = scale(loadImage("background"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    crosshairImage = scale(loadImage("crosshair"), (CROSSHAIR_WIDTH, CROSSHAIR_HEIGHT))

    crosshair = Crosshair()

    playerList = {}
    jutsuList = []
    images = {
        "background": backgroundImage,
        "crosshair": crosshairImage
    }

    # Run the main loop
    main(crosshair, playerList, jutsuList)
