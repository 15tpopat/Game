import pygame

from math import atan2, pi

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
        self.jutsuPosition = pygame.math.Vector2(playerRect.center)
        distance = mousePosition - self.jutsuPosition
        self.velocity = distance.normalize() * JUTSU_SPEED

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the sprite onto the screen
        pygame.draw.rect(screen, self.colour, self.rect)

    def update(self) -> None:
        # Update the position attributes used to draw the sprite
        self.jutsuPosition += self.velocity

        # As center is a tuple, complete reassignment of attribute is required
        self.rect.center = self.jutsuPosition.x, self.jutsuPosition.y

class FireballJutsu(Jutsu):
    """ This class represents the fire-natured fireball jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        db: dict,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(
            playerRect,
            db["technical"]["width"],
            db["technical"]["height"],
            jutsuID,
            mousePosition)

        # Override inherited attributes
        self.colour = db["technical"]["colour"]

class MudWall(Jutsu):
    """ This class represents the earth-natured mud wall jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        db: dict,
        timePassed: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(
            playerRect,
            db["technical"]["width"],
            db["technical"]["height"],
            jutsuID,
            mousePosition)

        # Override inherited attributes and add new ones
        self.colour = db["technical"]["colour"]
        self.rect.center = mousePosition
        self.thickness = db["technical"]["thickness"]

        # Despawn after X amount of time
        self.lifetime = (db["characteristics"]["lifetime"] * 1000) + timePassed

        # Calculate the angle of the jutsu
        dy = mousePosition[1] - playerRect.center[1]
        dx = mousePosition[0] - playerRect.center[0]
        self.angle = atan2(-dy, dx) % (2 * pi)

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the sprite onto the screen
        pygame.draw.arc(screen,
            self.colour,
            self.rect,
            self.angle - (pi / 4),
            self.angle + (pi / 4),
            width=self.thickness)

    def update(self) -> None:
        # Overrides the inherited update method to stop the jutsu from moving
        pass

class GalePalm(Jutsu):
    """ This class represents the wind-natured gale palm jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        width: int,
        height: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(playerRect, width, height, jutsuID, mousePosition)

class MistBarrier(Jutsu):
    """ This class represents the water-natured crimson mist barrier jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        width: int,
        height: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(playerRect, width, height, jutsuID, mousePosition)

class Limelight(Jutsu):
    """ This class represents the lightning-natured limelight minor jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        width: int,
        height: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(playerRect, width, height, jutsuID, mousePosition)
