"""
Data source, look for facebook lists: https://wiki.skullsecurity.org/Passwords
"""

# ----------- #
# fetch a sample of random people
import random


names_file_path = 'web_score/data/facebook-names-unique.txt'
num_lines = 100128460 # total number of lines in name_file_path
random_idx = set(random.choices(range(num_lines), k=500))
random_names = [x.rstrip() for i, x in enumerate(open(names_file_path)) if i in random_idx]

with open('web_score/data/random_names.txt', 'w') as outfile:
    outfile.write("\n".join(random_names))

# ----------- #
# call the api and save
import json
import os

import aiohttp
import asyncio


async def fetch(session, url):
    timeout = aiohttp.ClientTimeout(total=2*60)
    async with session.get(url, timeout=timeout) as response:
        return await response.text()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

# init
random_names = [line.strip() for line in open('web_score/data/random_names.txt')]
finished_names = [i.replace('.txt', '') for i in os.listdir('web_score/data/resp')]
random_names = [i for i in random_names if i not in finished_names]
localhost = True

# collect data
n = 10  # number of async requests at once
name_batches = [random_names[i:i+max(1, n)] for i in range(0, len(random_names), max(1, n))]

for batch in name_batches:

    url = 'https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/web_score?input={}&filter_input=1&api_key=54321'
    urls = [url.format(i) for i in batch]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(fetch_all(urls, loop))

    for response, name in zip(responses, batch):
        if not isinstance(response, Exception):
            response_json = json.loads(response)
            print(response_json)

            if 'input' in response_json.keys():  # check if proper response
                with open('web_score/data/resp/{}.txt'.format(name), 'w') as outfile:
                    json.dump(response_json, outfile)
            else:
                print(name)
