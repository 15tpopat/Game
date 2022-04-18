import pygame
import pygame_menu as pyMenu

from settings import *

class Menu:
    """ This class represents the menu. """

    def __init__(self, screen: pygame.Surface) -> object:
        # Set the necessary attributes
        self.screen = screen
        self.vars = {
            "username": None,
            "music": True,
            "sound_effects": True,
            "fullscreen": False,
            "cross_input_matches": False
        }

        # Create the main menu
        self.mainMenu = pyMenu.Menu(
            "Main Menu",
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            theme=pyMenu.themes.THEME_DARK,
            enabled=True)

        # Create the multiplayer menu
        self.multiplayerMenu = pyMenu.Menu(
            "Multiplayer Menu",
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            theme=pyMenu.themes.THEME_DARK,
            enabled=True)

        # Create the settings menu
        self.settingsMenu = pyMenu.Menu(
            "Settings Menu",
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            theme=pyMenu.themes.THEME_DARK,
            enabled=False)

        # Add the widgets to the menus
        self.createMainMenu()
        self.createSettingsMenu()
        self.createMultiplayerMenu()

        # Enable the main menu and make it visible
        self.mainMenu.mainloop(self.screen, fps_limit=FPS)

    def createMainMenu(self) -> None:
        # Create the multiplayer button
        self.mainMenu.add.button(
            "Multiplayer",
            self.multiplayerMenu,
            selection_color="#FFFFFF")

        # Create the training button
        self.mainMenu.add.button(
            "Training",
            self.startTraining,
            selection_color="#FFFFFF")

        # Create the guide button
        self.mainMenu.add.button(
            "Guide",
            self.startGuide,
            selection_color="#FFFFFF")

        # Create the settings button
        self.mainMenu.add.button(
            "Settings",
            self.settingsMenu,
            selection_color="#FFFFFF")

        # Create the quit button
        self.mainMenu.add.button(
            "Quit",
            pyMenu.events.EXIT,
            selection_color="#FFFFFF")

    def createMultiplayerMenu(self) -> None:
        # Create the username input button
        self.multiplayerMenu.add.text_input(
            "Name: ",
            default="",
            onchange=self.changeUsername,
            selection_color="#FFFFFF")

        # Create the start button
        self.multiplayerMenu.add.button(
            "Start",
            self.startMultiplayer,
            selection_color="#FFFFFF")

        # Create the back button
        self.multiplayerMenu.add.button(
            "Back",
            pyMenu.events.BACK,
            selection_color="#FFFFFF")

    def createSettingsMenu(self) -> None:
        # Create the music button
        self.settingsMenu.add.toggle_switch(
            "Music",
            self.vars["music"],
            onchange=self.toggleMusic,
            selection_color="#FFFFFF")

        # Create the sound effects button
        self.settingsMenu.add.toggle_switch(
            "Sound Effects",
            self.vars["sound_effects"],
            onchange=self.toggleSoundEffects,
            selection_color="#FFFFFF")

        # Create the fullscreen button
        self.settingsMenu.add.toggle_switch(
            "Fullscreen",
            self.vars["fullscreen"],
            onchange=self.toggleFullscreen,
            selection_color="#FFFFFF")

        # Create the cross input matches button
        self.settingsMenu.add.toggle_switch(
            "Cross Input Matches",
            self.vars["cross_input_matches"],
            onchange=self.toggleCrossInputMatches,
            selection_color="#FFFFFF")

        # Create the back button
        self.settingsMenu.add.button(
            "Back",
            pyMenu.events.BACK,
            selection_color="#FFFFFF")

    def startTraining(self) -> None:
        pass

    def startGuide(self) -> None:
        pass

    def changeUsername(self, value) -> None:
        self.vars["username"] = value

    def startMultiplayer(self) -> None:
        self.multiplayerMenu.disable()

    def toggleMusic(self, value) -> None:
        if value:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        self.vars["music"] = value

    def toggleSoundEffects(self, value) -> None:
        self.vars["sound_effects"] = value

    def toggleFullscreen(self, value) -> None:
        if value:
            infoObject = pygame.display.Info()
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.mainMenu.resize(infoObject.current_w, infoObject.current_h)
            self.settingsMenu.resize(infoObject.current_w, infoObject.current_h)
            self.multiplayerMenu.resize(infoObject.current_w, infoObject.current_h)
        else:
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.mainMenu.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.settingsMenu.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.multiplayerMenu.resize(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.vars["fullscreen"] = value

    def toggleCrossInputMatches(self, value) -> None:
        self.vars["cross_input_matches"] = value
