import aiohttp
from bs4 import BeautifulSoup

class Shodan:
    def __init__(self) -> None:
        self.headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}


    async def search(self, query: str) -> list[str]:
        """Searches Shodan for the specified query

        Args:
            query (str): The query to search Shodan for.

        Returns:
            list[str]: The urls returned from the search
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.shodan.io/search?query={query}", headers=self.headers) as resp:
                text = await resp.text()
                soup = BeautifulSoup(text, "html.parser")
                urls = []
                for url in soup.find_all('a', class_='title text-dark', href=True):
                    link = f"https://shodan.io{url.attrs['href']}"
                    urls.append(link)
        return urls

    async def report(self, query: str) -> str:
        """An in depth report for the specified query

        Args:
            query (str): The query to generate a report for

        Returns:
            str: The entire report generated
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.shodan.io/search/report?query={query}", headers=self.headers) as resp:
                text = await resp.text()
                soup = BeautifulSoup(text, "html.parser")
                title = query
                li_tags = soup.find_all('a', class_="text-dark")
                data = {}
                data['countries'] = []
                data['ports'] = []
                data['orgs'] = []
                data['vulns'] = []
                data['products'] = []
                data['tags'] = []
                data['os'] = []
                data['protocol_versions'] = []
                data['tls_version'] = []
                for item in li_tags:
                    if "country" in item.attrs['href']:
                        data['countries'].append(item.text)
                    elif "port" in item.attrs['href']:
                        data['ports'].append(item.text)
                    elif "org" in item.attrs['href']:
                        data['orgs'].append(item.text)
                    elif "vuln" in item.attrs['href']:
                        data['vulns'].append(item.text)
                    elif "product" in item.attrs['href']:
                        data['products'].append(item.text)
                    elif "tag" in item.attrs['href']:
                        data['tags'].append(item.text)
                    elif "os" in item.attrs['href']:
                        data['os'].append(item.text)
                    elif "ssl.alpn" in item.attrs['href']:
                        data['protocol_versions'].append(item.text)
                    elif "ssl.version" in item.attrs['href']:
                        data['tls_version'].append(item.text)
                return f"COUNTRIES: {data['countries']}\nPORTS: {data['ports']}\nORGANIZATIONS: {data['orgs']}\nVULNERABILITIES: {data['vulns']}\nPRODUCTS: {data['products']}\nTAGS: {data['tags']}\nOPERATING SYSTEMS: {data['os']}\nPROTOCOL VERSIONS: {data['protocol_versions']}\nTLS/SSL VERSIONS: {data['tls_version']}\nDISCLAIMER: These results listed are most popular results, not all results."

                # This is still ugly