import aiohttp
from bs4 import BeautifulSoup
from .errors import *

class DuckDuckGo:
    """Helper class for duckduckgo search related functions.
    """
    def __init__(self) -> None:

        self.headers={
            'accept': '*/*',
            'origin': 'https://lite.duckduckgo.com',
            'referer': 'https://lite.duckduckgo.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.124 Safari/537.36'
        }

    async def search(self, query: str, amount: int = 4 ) -> list[str]:
        """Searches duckduckgo for the specified query, with option for multiple searches (defaults to 4).

        Args:
            query (str): The query to search duckduckgo for.
            amount (int, optional): The amount of searches you want to do. Defaults to 4.

        Returns:
            list[str]: The links found from the searches.
        """
        texts = []
        links = []
        s = 0
        start = 0
        async with aiohttp.ClientSession() as session:

            async with session.post(f"https://lite.duckduckgo.com/lite/", headers=self.headers, data={'q': query,'kl': None, 'dt': None }) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    texts.append(text)
                else:
                    raise HTTPException("Failed to get HTTP Response", resp)
            async with session.post(f"https://lite.duckduckgo.com/lite/", headers=self.headers, data={'q': query,'s': s+30, 'o':'json', 'dc':start+16, 'api':'d.js', 'kl':'wt-wt' }) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    texts.append(text)
                else:
                    raise HTTPException("Failed to get HTTP Response", resp)

            for i in range(amount-2):
                async with session.post(f"https://lite.duckduckgo.com/lite/", headers=self.headers, data={'q': query,'s': s+50, 'o':'json', 'dc':start+50, 'api':'d.js', 'kl':'wt-wt' }) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        texts.append(text)
                    else:
                        raise HTTPException("Failed to get HTTP Response", resp)

            for text in texts:
                soup = BeautifulSoup(text, "html.parser")
                for link in soup.find_all('a', rel='nofollow', href=True):
                    links.append(link.attrs['href'])
            return links




