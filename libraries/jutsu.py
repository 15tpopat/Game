import pygame

from math import atan2, pi, sin, sqrt

from settings import *

class Jutsu:
    """ This class represents the jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        width: int,
        height: int,
        speed: int,
        playerID: int,
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
        self.playerID = playerID
        self.jutsuID = jutsuID
        self.remove = False

        # Calculate the trajectory of the jutsu
        self.jutsuPosition = pygame.math.Vector2(playerRect.center)
        self.distance = mousePosition - self.jutsuPosition
        self.velocity = self.distance.normalize() * speed

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
        playerID: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(
            playerRect,
            db["technical"]["width"],
            db["technical"]["height"],
            db["characteristics"]["speed"],
            playerID,
            jutsuID,
            mousePosition)

        # Override inherited attributes and add new ones
        self.colour = db["technical"]["colour"]
        self.damage = db["characteristics"]["damage"]

    def collide(self, player) -> int:
        # Reduce the health of the player when the jutsu collides with the player
        playerHealth = getattr(player, "health") - self.damage
        setattr(player, "health", playerHealth)

        # If the player has no health, kill the player
        if player.health <= 0:
            player.dead = True

class MudWall(Jutsu):
    """ This class represents the earth-natured mud wall jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        db: dict,
        timePassed: int,
        playerID: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(
            playerRect,
            db["technical"]["width"],
            db["technical"]["height"],
            0,
            playerID,
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
        db: dict,
        playerID: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(
            playerRect,
            db["technical"]["width"],
            db["technical"]["height"],
            db["characteristics"]["speed"],
            playerID,
            jutsuID,
            mousePosition)

        # Override inherited attributes and add new one
        self.colour = db["technical"]["colour"]

class MistBarrier(Jutsu):
    """ This class represents the water-natured crimson mist barrier jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        db: dict,
        timePassed: int,
        playerID: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(
            playerRect,
            1,
            1,
            0,
            playerID,
            jutsuID,
            mousePosition)

        # Override inherited attributes and add new ones
        self.colour = db["technical"]["colour"]
        self.radius = 1
        self.maximumRadius = db["technical"]["maximumRadius"]
        self.timePassed = 0

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the sprite onto the screen
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

    def update(self) -> None:
        # Overrides the inherited update method to increase and decrease the radius of the circle

        # The smaller the value, the slower the rate of change of size is
        self.timePassed += 0.005

        # This formula rapidly increases the radius of the circle and then slowly decreases it
        self.radius = self.maximumRadius * sin((self.timePassed - sqrt(pi)) ** 2)

        # If the radius is negative, delete the jutsu
        if self.radius <= 1:
            self.remove = True

class Chidori(Jutsu):
    """ This class represents the lightning-natured chidori jutsu. """

    def __init__(
        self,
        playerRect: pygame.Rect,
        db: dict,
        playerID: int,
        jutsuID: int,
        mousePosition: tuple
    ) -> object:
        # Initiate the jutsu super class
        super().__init__(
            playerRect,
            PLAYER_WIDTH * 1.5,
            PLAYER_HEIGHT * 1.5,
            db["characteristics"]["speed"],
            playerID,
            jutsuID,
            mousePosition)

        # Override inherited attributes and add new ones
        self.colour = db["technical"]["colour"]
        self.distanceMag = self.distance.magnitude()
        self.velocityMag = self.velocity.magnitude()

    def update(self) -> None:
        # Adds to the inherited update method to remove the jutsu at the mouse position
        super().update()

        # If the jutsu has travelled beyond the original mouse point, remove it
        self.distanceMag -= self.velocityMag
        if self.distanceMag < 0:
            self.remove = True
