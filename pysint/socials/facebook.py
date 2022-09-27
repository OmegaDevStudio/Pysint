import aiohttp
from bs4 import BeautifulSoup
import asyncio

class Facebook:
    """Facebook related utilities
	"""


    async def search(self, query: str):
        """Uses facebooks own API to search

		Args:
			query (str): The query which you wish to search for
		"""

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.facebook.com/public/{query}?_fb_noscript=1") as resp:
                text = await resp.text()
                soup = BeautifulSoup(text, "html.parser")
        return [url.attrs['href'] for url in soup.find_all('a', class_="_32mo", href=True)]