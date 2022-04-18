import pygame

from random import randint
from typing import Optional

from settings import *
from logging import *

class Player:
    """ This class represents the player. """

    def __init__(
        self,
        name: str,
        health: float,
        chakra: float,
        maximumChakra: int,
        rechargeRate: float,
        primaryAffinity: str,
        secondaryAffinity: str
    ) -> object:
        # Set the unique player attributes
        self.name = name
        self.health = health
        self.chakra = chakra
        self.maximumChakra = maximumChakra
        self.rechargeRate = rechargeRate
        self.primaryAffinity = primaryAffinity
        self.secondaryAffinity = secondaryAffinity

        # Set the technical player attributes
        self.playerID = randint(0, PLAYER_ID_RANGE)
        self.x = randint(int(SCREEN_WIDTH * PLAYER_SPAWN_GAP),
                         int(SCREEN_WIDTH * (1 - PLAYER_SPAWN_GAP)))
        self.y = randint(int(SCREEN_HEIGHT * PLAYER_SPAWN_GAP),
                         int(SCREEN_HEIGHT * (1 - PLAYER_SPAWN_GAP)))
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.colour = (randint(0, 255), randint(0, 128), randint(0, 255)) # Using 128 on green ensures the colour chosen isn't grey
        self.step = PLAYER_SPEED # The amount of units to increase the x, y positions by per frame (speed)
        self.dead = False

        # Set the attributes needed to change the activated jutsu
        self.jutsuSequence = ""

    def checkForJutsu(self, jutsuIndex: dict) -> Optional[str]:
        # Ensure there is no extra whitespace around the jutsu sequence
        jutsuSequence = self.jutsuSequence.strip()

        # Reset the jutsu sequence since we may be launching a jutsu
        self.jutsuSequence = ""

        # Change the jutsu if the jutsu sequence is valid
        if jutsuSequence in jutsuIndex.keys():
            jutsuKey = jutsuIndex[jutsuSequence]
            infoMessage(f"Recognised jutsu - {jutsuKey.capitalize()}")
            return jutsuKey
        else:
            debugMessage(f"Jutsu not recognised - \'{jutsuSequence}\'", end="\n")

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the sprite onto the screen
        pygame.draw.rect(screen, self.colour, self.rect)

    def mould(self, event: pygame.event.Event, jutsuIndex: dict) -> Optional[str]:
        # Convert the keyboard key into unicode
        letter = event.unicode.lower()

        # Delete the most recently entered letter in the jutsu sequence
        if event.key == pygame.K_BACKSPACE:
            self.jutsuSequence = self.jutsuSequence[:-1]

        # Append to the jutsu sequence or complete it
        elif len(letter) != 0: # Ignore keyboard keys such as the shift button which have 0 characters
            if ord(letter) == 13: # ENTER
                return self.checkForJutsu(jutsuIndex)
            elif ord(letter) == 32: # SPACE
                self.jutsuSequence += letter
            elif 96 < ord(letter) and ord(letter) < 123: # Ensures a <= letter <= z
                self.jutsuSequence += letter
            else:
                pass # Ignore other irrelevant characters
        else:
            pass # Ignore other irrelevant characters

    def move(self) -> None:
        # Get a dictionary of what keys are pressed
        keysPressed = pygame.key.get_pressed()

        # Alter the position attributes of the character based on what values of the dictionary are True
        if keysPressed[pygame.K_UP]:
            self.y -= self.step
        if keysPressed[pygame.K_DOWN]:
            self.y += self.step
        if keysPressed[pygame.K_LEFT]:
            self.x -= self.step
        if keysPressed[pygame.K_RIGHT]:
            self.x += self.step

        self.updatePosition()

    def updatePosition(self) -> None:
        # Update the position attribute used to draw the sprite
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
