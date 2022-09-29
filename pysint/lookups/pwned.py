import aiohttp
from bs4 import BeautifulSoup
from aioconsole import aprint
from colorama import Fore as color



class Pwned:
    def __init__(self) -> None:
        self.headers = {"x-requested-with": "XMLHttprequest", "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.124 Safari/537.36"}



    async def check_email(self, query: str):
        """Checks if your email/query has been pwned

        Args:
            query (str): Your email/query
        """
        account = query.replace("@", "%40")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://haveibeenpwned.com/", headers=self.headers) as resp:
                cookie = resp.headers['set-cookie']
            x = await session.get(f"https://haveibeenpwned.com/unifiedsearch/{account}", headers={f"cookie":cookie, "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.124 Safari/537.36", "connection":"keep-alive", "Host":"haveibeenpwned.com", "referer":"https://haveibeenpwned.com"})
            if x.status == 404:
                await aprint(f"{color.RED}Email not in database{color.RESET}")
            if x.status == 200:
                z = await x.json()
                breaches = z['Breaches']
                msg = ""
                for breach in breaches:
                    name = breach['Name']
                    date = breach['BreachDate']
                    count = breach['PwnCount']
                    msg += f"{color.RED}NAME: {color.YELLOW}{name} --- {color.RED}DATE: {color.YELLOW}{date} --- {color.RED}COUNT: {color.YELLOW}{count}{color.RESET}\n"
                return msg



