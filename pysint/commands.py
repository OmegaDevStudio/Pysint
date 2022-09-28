import asyncio
from colorama import Fore as color
from aioconsole import aprint, ainput
import os
from .lookups import *
from .browsers import *
from .socials import *
from .lookups import *


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
        await aprint(f"{color.YELLOW}=================================================================={color.RESET}")
        for command in self.user_show:
            await aprint(f"{color.RED}{command['name']}:  {color.YELLOW}{command['description']}{color.RESET}")
        await aprint(f"{color.YELLOW}=================================================================={color.RESET}")

    async def error(self, *args, **kwargs):
        """Message displayed if something errors
        """
        await aprint(f"{color.RED}Error: You are fail - command does not exist{color.RESET}")

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

            func = self.all_commands.get(input.lower(), self.error)
            if len(func.__code__.co_varnames) > 1:
                args = []
                for item in func.__code__.co_varnames:
                    if item == "query":
                        query = await ainput(f"{color.GREEN}Query required {color.LIGHTBLUE_EX}[{color.YELLOW}>{color.LIGHTBLUE_EX}]{color.RESET} ")
                        args.append(query)
                    if item == "amount":
                        amount = await ainput(f"{color.GREEN}Amount of searches required {color.LIGHTBLUE_EX}[{color.YELLOW}>{color.LIGHTBLUE_EX}]{color.RESET} ")
                        args.append(int(amount))
                    if item == "path":
                        path = await ainput(f"{color.GREEN}Path to image required {color.LIGHTBLUE_EX}[{color.YELLOW}>{color.LIGHTBLUE_EX}]{color.RESET} ")
                        args.append(path)
                try:
                    await self.all_commands.get(input, self.error)(*args)
                except Exception as e:
                    await aprint(f"{color.RED}Error: {e}{color.RESET}")
            else:
                await self.all_commands.get(input, self.error)()




Pysint = Pysint()

@Pysint.command(description="Displays all commands available to the user")
async def help():
    await Pysint.show()

@Pysint.command(description="Shows very cool ascii")
async def ascii():
    os.system('cls' if os.name == 'nt' else 'clear')
    await Pysint.ascii()

@Pysint.command(description="<query> <amount> - Searches google for specified query")
async def google(query: str, amount: int = 4):
    google = Google()
    resp = await google.search(query, int(amount))
    for url in resp:
        await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {url}")

@Pysint.command(description="<query> <amount> - Searches yandex for specified query")
async def yandex(query: str, amount: int = 4):
    yandex = Yandex()
    resp = await yandex.search(query, amount)
    for url in resp:
        await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {url}")

@Pysint.command(description="<path> - Searches yandex with image search")
async def imagesearch(path: str):
    yandex = Yandex()
    resp = await yandex.image_search(path)
    for url in resp:
        await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {url}")

@Pysint.command(description="<query> <amount> - Searches duckduckgo for specified query")
async def duck(query: str, amount: int = 4):
    duck = DuckDuckGo()
    resp = await duck.search(query, amount)
    for url in resp:
        await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {url}")

@Pysint.command(description="<query> - Searches shodan for specified query")
async def shodan(query: str):
    shodan = Shodan()
    resp = await shodan.search(query)
    for url in resp:
        await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {url}")

@Pysint.command(description="<query> - Gives in depth shodan report for specified search")
async def shodanreport(query: str):
    shodan = Shodan()
    resp = await shodan.report(query)
    await aprint(resp)


@Pysint.command(description="<query> <amount> - Searches Instagram using dorking methods")
async def instagram(query: str, amount: int = 4):
    google = Google()
    yandex = Yandex()
    duck = DuckDuckGo()

    gathered = await asyncio.gather(google.search(f"site:'https://instagram.com' intitle:'{query}'", amount), yandex.search(f"site:'https://instagram.com' intitle:'{query}'", amount), duck.search(f"site:'https://instagram.com' intitle:'{query}'", amount) )
    for searches in gathered:
        for url in searches:
            await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {url}")

@Pysint.command(description="<query> <amount> - Searches Facebook using dorking methods")
async def facebook(query: str, amount: int = 4):
    google = Google()
    yandex = Yandex()
    duck = DuckDuckGo()
    gathered = await asyncio.gather(google.search(f"site:'https://facebook.com' intitle:'{query}'", amount), yandex.search(f"site:'https://facebook.com' intitle:'{query}'", amount), duck.search(f"site:'https://facebook.com' intitle:'{query}'", amount))
    for searches in gathered:
        for url in searches:
            await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {url}")

@Pysint.command(description="<query> - Searches Facebook using API")
async def facebookapi(query: str):
    facebook = Facebook()
    resp = await facebook.search(query)
    for url in resp:
        await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {url}")



@Pysint.command(description="<query> - Searches Twitter using dorking methods")
async def twitter(query: str, amount: int =4):
    google = Google()
    yandex = Yandex()
    duck = DuckDuckGo()
    gathered = await asyncio.gather(google.search(f"site:'https://twitter.com' intitle:'{query}'", amount), yandex.search(f"site:'https://twitter.com' intitle:'{query}'", amount), duck.search(f"site:'https://twitter.com' intitle:'{query}'", amount))
    for searches in gathered:
        for url in searches:
            await aprint(f"{color.LIGHTYELLOW_EX}LINK FOUND -> {url}")

@Pysint.command(description="<query> - Gathers information regarding an IP address from public sources")
async def geoip(query:str):
    geoip = Host()
    resp = await geoip.get_ip(query)
    await aprint(resp)

@Pysint.command(description="<query> - Attempts to get a domains IP address")
async def domainip(query: str):
    host = Host()
    resp = await host.domain_ip(query)
    await aprint(resp)

@Pysint.command(description="<query> - Gathers information regarding a host from public sources")
async def whois(query: str):
    host = Host()
    resp = await host.host_whois(query)
    await aprint(resp)


