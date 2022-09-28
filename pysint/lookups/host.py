import aiohttp
from bs4 import BeautifulSoup
from colorama import Fore as color

class Host:
    def __init__(self) -> None:
        self.apikey = "WnZCo3GwKoia2iaWMJFq"
        self.headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.126 Safari/537.36"}

    async def get_ip(self, query: str) -> str:
        """Get IP information from the specified query

        Args:
            query (str): The IP address you wish to search for

        Returns:
            str: Information regarding the IP address
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://extreme-ip-lookup.com/json/{query}?key={self.apikey}") as resp:
                geo = await resp.json()
                msg = ""
                for key, value in geo.items():
                    msg += f"{color.RED}{key}:  {color.YELLOW}{value}\n"
            return msg

    async def host_whois(self, query: str) -> str:

        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://www.ipvoid.com/whois/", headers=self.headers, data={"host": query}) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    soup = BeautifulSoup(text, "html.parser")
                    data = soup.find("textarea")

                    return f"{color.YELLOW}{data.text}{color.RESET}"


            #form-control textarea


