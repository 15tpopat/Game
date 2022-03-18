from colorama import Fore
from inspect import getframeinfo, stack, Traceback
from os import getcwd

ROOT_FOLDER = getcwd().split("/")[-1] # Get the tail folder of the working directory
ROOT_FOLDER = "/" + ROOT_FOLDER + "/" # (The parent folder of the server.py and main.py files)

def getFilename(caller: Traceback) -> str:
    if ROOT_FOLDER in caller.filename:
        filename = caller.filename[caller.filename.rindex(ROOT_FOLDER) + len(ROOT_FOLDER):]
    else:
        filename = caller.filename

    return filename

def colourPrint(text: str, colour: str = "reset", end: str = "\n"):
    if colour is None:
        raise TypeError("'colour' parameter cannot be NoneType.")

    print(eval("Fore.{}".format(colour.upper())) + text, end=end)
    print("\033[39m", end="")

def infoMessage(text: str, start: str = "", colour: str = "blue", end: str = ".\n"):
    caller = getframeinfo(stack()[1][0])
    filename = getFilename(caller)
    colourPrint("{start}{filename}:{lineNumber}\t\t{text}".format(
                start=start,
                filename=filename,
                lineNumber=f"{caller.lineno:03d}", # Ensures the line number has the same number of digits
                text=text),
                colour=colour,
                end=end)

def debugMessage(text: str, start: str = "", colour: str = "magenta", end: str = "...\n"):
    caller = getframeinfo(stack()[1][0])
    filename = getFilename(caller)
    colourPrint("{start}{filename}:{lineNumber}\t\t{text}".format(
                start=start,
                filename=filename,
                lineNumber=f"{caller.lineno:03d}", # Ensures the line number has the same number of digits
                text=text),
                colour=colour,
                end=end)

def errorMessage(text: str, colour: str = "red", prefix: bool = True, end: str = "!\n"):
    caller = getframeinfo(stack()[1][0])
    filename = getFilename(caller)
    if prefix:
        colourPrint("{filename}:{lineNumber}\t\t{text}".format(
                    filename=filename,
                    lineNumber=f"{caller.lineno:03d}", # Ensures the line number has the same number of digits
                    text=text),
                    colour=colour,
                    end=end)
    else:
        colourPrint(text,
                    colour=colour,
                    end=end)
