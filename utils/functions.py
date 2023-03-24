import os

from typing import AnyStr
from sys import executable, argv

from numerize import numerize
#from discord.ext import commands


""" def commands_cooldown():
    _cooldown = commands.CooldownMapping.from_cooldown(
        4.0, 15.0, commands.BucketType.user) """


def clear_console() -> None:
    """ clears the console """
    os.system("cls" if os.name == "nt" else "clear")


def restart_bot() -> None:
    """ restarts the bot """
    os.execv(executable, ['python'] + argv)


def better_numbers(number: int) -> str:
    """
    returns a neater number format, useful for big numbers

    Parameters
    ----------
    `number`: int
     the number to format

    Returns
    -------
    `str`
     the formatted number
    """

    return numerize.numerize(number).lower()


def read_file(filepath: str, *args, **kwargs) -> AnyStr:
    """
    reads a file and returns the content

    Parameters
    ----------
    `filepath`: str
     The path to the file to read

    Returns
    -------
    `AnyStr`
     the content of the file
    """

    with open(filepath, *args, **kwargs, encoding='utf-8') as f:
        return f.read()


def line_count() -> int:
    """
    counts the lines of code in the current dir 

    Returns
    -------
    `int`
     the number of lines of code
    """

    total_lines = 0

    for root, subdirs, files in os.walk(os.getcwd()):
        for filename in files:

            if filename.endswith('.py'):
                file = os.path.join(root, filename)

                with open (file, mode='r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    total_lines += len(all_lines)
    return total_lines

