import pygame
import sys

from settings import *

def main() -> None:
    # Start game loop
    while True:
        # Event processing
        for event in pygame.event.get():
            # If they click the exit button, quit pygame and exit python
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update the screen
        pygame.display.update()

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

    # Run the main loop
    main()
