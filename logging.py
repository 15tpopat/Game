from colorama import Fore
from inspect import getframeinfo, stack
from os import getcwd
from typing import Optional

ROOT_FOLDER = getcwd().split("/")[-1] # Get the tail folder of the working directory
ROOT_FOLDER = "/" + ROOT_FOLDER + "/" # (The parent folder of the server.py and main.py files)

def colourPrint(text: str, colour: Optional[str] = None, end: str = "\n"):
    if colour is None:
        raise TypeError("'colour' parameter cannot be NoneType.")

    print(eval("Fore.{}".format(colour.upper())) + text, end=end)
    print("\033[39m", end="")

def message(*text: str):
    text = " ".join(text)
    colourPrint(text + ".", colour="cyan")

def infoMessage(*text: str, start: str = ""):
    text = " ".join(text)
    caller = getframeinfo(stack()[1][0])
    fileName = caller.filename[caller.filename.rindex(ROOT_FOLDER):]
    colourPrint("{start}{filename}:{lineNumber}\t\t{text}".format(
                start=start,
                filename=fileName,
                lineNumber=caller.lineno,
                text=text + "."),
                colour="cyan")

def debugMessage(*text: str, start: str = ""):
    text = " ".join(text)
    caller = getframeinfo(stack()[1][0])
    fileName = caller.filename[caller.filename.rindex(ROOT_FOLDER):]
    colourPrint("{start}{filename}:{lineNumber}\t\t{text}".format(
                start=start,
                filename=fileName,
                lineNumber=caller.lineno,
                text=text + "..."),
                colour="magenta")

def errorMessage(*text: str):
    text = " ".join(text)
    caller = getframeinfo(stack()[1][0])
    fileName = caller.filename[caller.filename.rindex(ROOT_FOLDER):]
    colourPrint("{filename}:{lineNumber}\t\t{text}".format(
                filename=fileName,
                lineNumber=caller.lineno,
                text=text + "!"),
                colour="red")
