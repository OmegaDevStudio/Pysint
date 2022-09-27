import asyncio
from colorama import Fore as color
from aioconsole import aprint, ainput
from .browsers import *

class Pysint:
    """A class dedicated for all Pysint related commands
    """
    def __init__(self):
        self.all_commands = dict()
        self.user_show = list()


    def command(self, description: str):
        """A decorator to help add commands
        """
        def decorator(func):
            self.all_commands[func.__name__] = func
            self.user_show.append({"name": func.__name__, "description": description})
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator

    async def show(self):
        """Method to display all commands available to the user
        """
        for command in self.user_show:
            await aprint(f"{command['name']}:  {command['description']}")

    async def error(self, *args, **kwargs):
        """Message displayed if something errors
        """
        await aprint(f"{color.RED}YOU FAILURE{color.RESET}")

    async def ascii(self):
        """Method to display the very cool ascii
        """
        await aprint(f"""{color.RED}
█▀█ █▄█ █▀ █ █▄░█ ▀█▀
█▀▀ ░█░ ▄█ █ █░▀█ ░█░
{color.YELLOW}
Type help below to display all the commands available to you. Parameters for a particular command are encapsulated with <paramater>.
        {color.RESET}""")

    async def command_input(self):
        while True:
            input = await ainput(f"""
{color.LIGHTBLUE_EX}╔═══ {color.RED}╬ OmegaDev [Ω] ╬
{color.LIGHTBLUE_EX}║
{color.LIGHTBLUE_EX}╚══[{color.YELLOW}>{color.LIGHTBLUE_EX}] {color.RESET}""")

            func = self.all_commands.get(input, self.error)
            if len(func.__code__.co_varnames) > 1:
                args = []
                for item in func.__code__.co_varnames:
                    if item == "query":
                        query = await ainput(f"{color.GREEN}Query required {color.LIGHTBLUE_EX}[{color.YELLOW}>{color.LIGHTBLUE_EX}]{color.RESET} ")
                        args.append(query)
                    if item == "amount":
                        amount = await ainput(f"{color.GREEN}Amount required {color.LIGHTBLUE_EX}[{color.YELLOW}>{color.LIGHTBLUE_EX}]{color.RESET} ")
                        args.append(amount)

                await self.all_commands.get(input, self.error)(*args)
            else:
                await self.all_commands.get(input, self.error)()


Pysint = Pysint()

@Pysint.command(description="Displays all commands available to the user")
async def help():
    await Pysint.show()

@Pysint.command(description="<query> <amount> - Searches google for specified query")
async def google(query: str, amount: int = 4):
    google = Google()
    resp = await google.search(query, int(amount))
    for item in resp:
        await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {item}")

