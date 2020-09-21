"""
# this url works fine
# will get blocked after a while if many requests are made > 150
# might work for longer if shuffling headers and user-agent
# still will have to use proxy
https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":2738070677,"include_reel":false,"fetch_mutual":false,"first":0}

# many different hashes
https://github.com/ping/instagram_private_api/blob/54427574583d33544c006c9f6a13cb6bc306a714/instagram_web_api/client.py#L387

# this contains all I need but does not work over proxy?
# works sometimes, prob due to random pc being logged into fb, else not
# prob due to headers and cookies or something else
# ok this requires login and redirects to /accounts/login if not logged in
'https://www.instagram.com/raidasgriskevicius/?__a=1'

"""

import requests
from bs4 import BeautifulSoup
import json
from data_sources.async_utils import make_async_requests
from data_sources.requests_utils import requests_retry_session
from log_cofig import logger

# The following func is not longer used as there is a better solution!
# TODO: hard to replicate but sometimes this parse does not do the job
#  guess is that the response html structure depends on the caller location
#  when doing this through proxy the response structure is not parsed sometimes
#  maybe fix the proxy location?
#  another solution would be to work with async calls and set single proxy for whole batch
def parse_html_to_user_info(html):
    """
    Parses data from 'https://www.instagram.com/{username}/?__a=1'
    """

    output = {}
    soup = BeautifulSoup(html, 'html.parser')

    # TODO: private public?
    # TODO: description
    for item in soup.findAll('meta', attrs={'name': 'description', 'content': True}):
        content = item.get('content')
        if 'Followers' in content:
            words = content.split()
            # TODO: this does not work all the time
            try:
                output['followers_count'] = int(words[0].replace('k', '00').replace(',', '').replace('.', ''))
                output['following_count'] = int(words[2].replace('k', '000').replace(',', '').replace('.', ''))
                output['posts_count'] = int(words[4].replace('k', '000').replace(',', '').replace('.', ''))
            except:
                print('Failed to parse IG user info, now trying another html structure')
                continue
            break

    # if nothing was found then profile is set to private and html is structured differently
    if not output:
        js_items = soup.findAll('script', attrs={'type': 'text/javascript'})
        for item in js_items:
            # TODO: somehow the following line only works with beautifulsoup4==4.8.2
            if 'edge_followed_by' in item.text:
                js_json = json.loads(item.text.replace('window._sharedData = ', '')[:-1])
                output['followers_count'] = int(js_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count'])
                output['following_count'] = int(js_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count'])
                output['posts_count'] = int(js_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count'])
    return output


def parse_json_to_user_info(user_info):
    output = {}
    output['followers_count'] = user_info.get('data').get('user').get('edge_followed_by').get('count')
    return output


def get_instagram_users(input, proxies):

    # user search endpoint
    # get usernames associated with name surname
    url = 'https://www.instagram.com/web/search/topsearch'
    params = {'query': input.replace(' ', '+'), 'context': 'blended'}

    logger.info('Sending a user search request to instagram')
    response = requests_retry_session().get(url, params=params, proxies=proxies)
    # TODO: sometimes receiving this error
    # raise JSONDecodeError(\"Expecting value\", s, err.value) from
    # None\njson.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n",
    search_output = response.json()

    # get info of users
    # make async calls to save some time
    user_names = [i['user']['username'] for i in search_output['users'][:5]]
    user_ids = [i['user']['pk'] for i in search_output['users'][:5]]
    url = 'https://www.instagram.com/graphql/query/' \
          '?query_hash=c76146de99bb02f6415203be841dd25a&' \
          'variables={{"id":{},"include_reel":false,"fetch_mutual":false,"first":0}}'
    user_urls = [url.format(id) for id in user_ids]
    user_data = make_async_requests(user_urls, proxies)
    # TODO: sometimes receiving this error
    # raise TypeError(f'the JSON object must be str, bytes or bytearray, '
    # \nTypeError: the JSON object must be str, bytes or bytearray, not JSONDecodeError\n"
    user_data = [json.loads(i) for i in user_data]

    # parse info
    users = []
    for data, name in zip(user_data, user_names):
        user_info = {'username': name}
        user_info.update(parse_json_to_user_info(data))
        users.append(user_info)

    output = {}
    output['num_users'] = len(response.json()['users'])
    output['users'] = users

    return output
