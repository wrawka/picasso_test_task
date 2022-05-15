import asyncio
import json

import aiohttp
from bs4 import BeautifulSoup


async def fetch_html(url: str, session: aiohttp.ClientSession, **kwargs) -> str:
    """Fetches html source from `url`."""
    response = await session.request(method="GET", url=url, **kwargs)
    html = await response.text()
    return html


def get_urls_from_html(raw_html):
    """Parses html code for the `<a href='url'></a>` tags and collects all `url`'s."""
    html_soup = BeautifulSoup(raw_html, "html.parser")
    urls = set(tag.get('href') for tag in html_soup.find_all('a', href=True))
    return urls


async def domains_search(url: str, session: aiohttp.ClientSession, **kwargs):
    """Polls some API for some data 🤷."""
    api_url = 'https://api.domainsdb.info/v1/domains/search?domain='
    response = await session.request(method="GET", url=api_url + url, **kwargs)
    found_data = json.loads(await response.text())
    return found_data


async def bulk_domains_search(urls: set, session: aiohttp.ClientSession, **kwargs):
    """Runs `domains_search` for `urls` collection."""
    tasks = []
    for url in urls:
        tasks.append(
            domains_search(url, session, **kwargs)
        )
    return await asyncio.gather(*tasks)
