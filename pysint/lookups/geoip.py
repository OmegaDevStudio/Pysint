import aiohttp
from bs4 import BeautifulSoup
from colorama import Fore as color
class GeoIp:
    def __init__(self) -> None:
        self.apikey = "WnZCo3GwKoia2iaWMJFq"

    async def get(self, query: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://extreme-ip-lookup.com/json/{query}?key={self.apikey}") as resp:
                geo = await resp.json()
                msg = ""
                for key, value in geo.items():
                    msg += f"{color.RED}{key}:  {color.YELLOW}{value}\n"
            return msg
