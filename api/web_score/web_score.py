"""
Data source, look for facebook lists: https://wiki.skullsecurity.org/Passwords

"""

# ----------- #
# fetch a sample of random people
import random
import os

names_file_path = 'web_score/data/facebook-names-unique.txt'
num_lines = int(os.popen('wc -l < ' + names_file_path).read().rstrip())  # 100128460
random_idx = set(random.choices(range(num_lines), k=500))
random_names = [x.rstrip() for i, x in enumerate(open(names_file_path)) if i in random_idx]

with open('web_score/data/random_names.txt', 'w') as outfile:
    outfile.write("\n".join(random_names))

# ----------- #
# call the api and save
import requests
import json

for name in random_names:
    url = 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score?input={}&filter_input=0'.format(name)
    response = requests.get(url)
    print(response.text)

    with open('web_score/data/resp/{}.txt'.format(name), 'w') as outfile:
        json.dump(response.json(), outfile)

# ----------- #
# load and structure
with open('data.txt') as json_file:
    data = json.load(json_file)


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