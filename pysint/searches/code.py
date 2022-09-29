import aiohttp
from bs4 import BeautifulSoup

class CodeSearch:
    def __init__(self) -> None:
        self.headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

    async def search(self, query: str, amount: int = 4 ) -> list[str]:
        """Searches searchcode for the specified query, with option for multiple searches (defaults to 4).

        Args:
            query (str): The query to search codesearch for.
            amount (int, optional): The amount of searches you want to do. Defaults to 4.

        Returns:
            list[str]: The links found from the searches.
        """
        async with aiohttp.ClientSession() as session:
            links = []
            for i in range(amount):
                async with session.get(f"https://searchcode.com/?q={query}&p={i}", headers=self.headers) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        soup = BeautifulSoup(text, "html.parser")
                        divs = soup.find("div", style="width:100%;")

                        for url in divs.find_all("a", href=True,  recursive=False):

                            links.append(f"https://searchcode.com{url['href']}")

            return links


