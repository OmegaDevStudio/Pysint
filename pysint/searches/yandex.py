from bs4 import BeautifulSoup
import aiohttp
from .errors import *

class Yandex:
    """Helper class for yandex search related functions.
    """
    def __init__(self):
        self.headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'host': 'yandex.com',
            'referer': 'https://yandex.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.124 Safari/537.36'
        }

    async def search(self, query: str, amount: int = 4 ) -> list[str]:
        """Searches yandex for the specified query, with option for multiple searches (defaults to 4).

        Args:
            query (str): The query to search yandex for.
            amount (int, optional): The amount of searches you want to do. Defaults to 4.

        Returns:
            list[str]: The links found from the searches.
        """
        texts = []
        links = []
        async with aiohttp.ClientSession() as session:
            for i in range(amount):
                async with session.get(f"https://yandex.com/search/?text={query}&p={i}", headers=self.headers) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        texts.append(text)
                    else:
                        raise HTTPException("Failed to get HTTP Response", resp.status)

            for text in texts:
                soup = BeautifulSoup(text, "html.parser")
                a_tags = soup.find_all('a', class_='Link Link_theme_normal OrganicTitle-Link organic__url link', href=True)
                for link in a_tags:
                    links.append(link.attrs['href'])
            return links

    async def image_search(self, path: str) -> list[str]:
        """Searches yandex image search for the specified image.

        Args:
            path (str): The path to the image.

        Returns:
            list[str]: The links found from the searches
        """
        try:
            path = path.replace("'", "")
        except:
            pass

        async with aiohttp.ClientSession() as session:
            with open(path, 'rb')as f:
                image = f.read()
            async with session.post("https://yandex.com/images-apphost/image-download?cbird=37&images_avatars_size=preview&images_avatars_namespace=images-cbir", headers=self.headers, data=image)as resp:
                if resp.status == 200:
                    k = await resp.json()
                    url = k['url']
                    shard = k['image_shard']
                    id = k['image_id']
                else:
                    raise HTTPException("Failed to get HTTP Response", resp.status)

                url = url.replace('preview', 'orig')
                async with session.get(f"https://yandex.com/images/search?rpt=imageview&url={url}&cbir_id={shard}/{id}", headers=self.headers) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        soup = BeautifulSoup(text, "html.parser")
                        info = [link.attrs['href'] for link in soup.find_all('a', class_='Link Link_view_default', href=True)]
                        return info
                    else:
                        raise HTTPException("Failed to get HTTP Response", resp.status)


