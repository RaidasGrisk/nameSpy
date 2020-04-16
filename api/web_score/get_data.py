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
import os
from endpoint_get_social_score import app as social_score_app

random_names = [line.strip() for line in open('web_score/data/random_names.txt')]
finished_names = [i.replace('.txt', '') for i in os.listdir('web_score/data/resp')]
random_names = [i for i in random_names if i not in finished_names]
localhost = True
for name in random_names:

    if localhost:
        with social_score_app.test_client() as c:
            response = c.get('api/social_score?input={}&filter_input=0'.format(name))
            response_json = json.loads(response.data)

    else:
        url = 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score?input={}&filter_input=0'.format(name)
        response = requests.get(url)
        response_json = json.loads(response.text)

    print(response_json)

    with open('web_score/data/resp/{}.txt'.format(name), 'w') as outfile:
        json.dump(response_json, outfile)


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


