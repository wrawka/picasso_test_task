import aiohttp

from django.shortcuts import render

from . import parser


HEADER = [
    "найденный url",
    "domain",
    "create_date",
    "update_date",
    "country",
    "isDead",
    "A",
    "NS",
    "CNAME",
    "MX",
    "TXT"
]


def index(requset):
    return render(requset, "input.html")


async def parse(request):
    target_url = request.POST.get('url')
    context = {'header': HEADER, 'rows': []}

    async with aiohttp.ClientSession() as session:
        raw_html = await parser.fetch_html(target_url, session)
        urls = parser.get_urls_from_html(raw_html)
        found_data = await parser.bulk_domains_search(urls, session)
        for url, data in zip(urls, found_data):
            context['rows'].append({'url': url, 'domains': data.get('domains')})
    return render(request, "parse.html", context=context)
