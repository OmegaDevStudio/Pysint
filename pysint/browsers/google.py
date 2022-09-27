import aiohttp
from bs4 import BeautifulSoup
from .errors import *

class Google:
    """Helper class designed for google search related functions for optimal scraping.
    """
    def __init__(self):
        self.headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

    async def search(self, query: str, amount: int = 4 ) -> list[str]:
        """Searches google for the specified query, with option for multiple searches (defaults to 4).

        Args:
            query (str): The query to search google for.
            amount (int, optional): The amount of searches you want to do. Defaults to 4.

        Returns:
            list[str]: The links found from the searches.
        """

        async with aiohttp.ClientSession() as session:
            texts = []
            links = []
            start= 0
            for i in range(amount):
                async with session.get(f"https://www.google.com/search?q={query}&start={start}",headers=self.headers) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        texts.append(text)
                        start += 10
                    else:
                        raise HTTPException("Failed to get HTTP Response", resp)
            for text in texts:
                soup = BeautifulSoup(text, "html.parser")
                a_tags = soup.find_all('div', class_='yuRUbf')
                for link in a_tags:
                    links.append(link.find('a', href=True)['href'])

            return links


