import pygame

from random import randint

from settings import *

class Jutsu:
    """ This class represents the jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        width: int,
        height: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Set the technical jutsu attributes
        self.x = playerRect.center[0]
        self.y = playerRect.center[1]
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.colour = JUTSU_COLOUR

        # Set the network jutsu attributes
        self.jutsuID = jutsuID
        self.remove = False

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
