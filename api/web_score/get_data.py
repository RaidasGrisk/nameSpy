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
from endpoint_get_web_score import app as social_score_app

random_names = [line.strip() for line in open('web_score/data/random_names.txt')]
finished_names = [i.replace('.txt', '') for i in os.listdir('web_score/data/resp')]
random_names = [i for i in random_names if i not in finished_names]
localhost = True

# sync
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

# async
from data_sources.async_utils import make_async_requests

n = 10
name_batches = [random_names[i:i+max(1, n)] for i in range(0, len(random_names), max(1, n))]

for batch in name_batches:

    # url = 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score?input={}&filter_input=0&use_proxy=1'
    url = 'http://localhost:8080/api/social_score?input={}&filter_input=0&use_proxy=1'
    urls = [url.format(i) for i in batch]
    responses = make_async_requests(urls)

    for response, name in zip(responses, batch):
        response_json = json.loads(response)
        print(response_json)

        # check for errors
        if 'input' in response_json.keys():
            with open('web_score/data/resp/{}.txt'.format(name), 'w') as outfile:
                json.dump(response_json, outfile)
        else:
            print(response_json)
            print(name)

