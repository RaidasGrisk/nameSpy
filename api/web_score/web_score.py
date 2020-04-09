import random

# ----------- #
# fetch a sample of random people
names_file_path = 'web_score/data/facebook-names-unique.txt'
num_lines = sum(1 for line in open(names_file_path))
random_names = random.choices(range(num_lines), k=500)

name_nr = 0
with open(names_file_path) as f:
    for line in f:
        if name_nr in random_names:
            print(line)
        name_nr += 1

# ----------- #
# call APIs to collect data
import aiohttp
import asyncio


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    urls = [
            'http://python.org',
            'https://google.com',
            'http://yifei.me'
        ]
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        for html in htmls:
            print(html[:100])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


# -------- #
# make stats distributions

from statsmodels.distributions.empirical_distribution import ECDF
# https://www.statsmodels.org/stable/generated/statsmodels.distributions.empirical_distribution.ECDF.html