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

import json
from data_sources.async_utils import make_async_requests
from data_sources.requests_utils import requests_retry_session
from log_config import logger


def parse_json_to_user_info(user_info):
    output = {
        'followers_count': user_info.get('data').get('user').get('edge_followed_by').get('count')
    }
    return output


def get_instagram_users(input, proxies):

    # user search endpoint
    # get usernames associated with name surname
    url = 'https://www.instagram.com/web/search/topsearch'
    params = {'query': input.replace(' ', '+'), 'context': 'blended'}

    # since ~2020-12-12 the request must contain user-agent header
    # else will return an html everytime
    # <!DOCTYPE html>\n<html lang="en" class="no-js not-logged-in client-root">
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.116 Safari/537.36',
    }

    # sometimes instead of json it returns html
    # <!DOCTYPE html>\n<html lang="en" class="no-js not-logged-in client-root">
    # try again if such case occur
    for i in range(5):
        try:
            logger.info(f'Sending a user search request to instagram {i}')
            response = requests_retry_session().get(url, params=params, headers=headers, proxies=proxies)
            search_output = response.json()
            logger.info(f'Sending a user search request to instagram: received a valid response')
            break
        except json.decoder.JSONDecodeError as e:
            logger.info(f'user search request to instagram exception: {repr(e)}')
            continue

    # get info of users
    # make async calls to save some time

    # as of 2021-05-01 many requests are failing.
    # looks like it wont fail if cookie is included
    # in header. Don't think this is a long term solution
    # will probably be banned or something. Don't see other
    # solutions though. Cookies taken from chrome browser.
    headers_ = {
        "cookie":
            "ig_did=9D06479D-FAB2-4F3B-A77E-2C3D7410AAC1; "
            "mid=XuzOYgAEAAFhdMSCcYcQ6kuygMhy; "
            "fbm_124024574287414=base_domain=.instagram.com; "
            "csrftoken=D6TGF4d2TA5pe7KrHGBjhtTUzY7DLuk1; "
            "sessionid=4791334445%3ArcqL1iuBGrw1JZ%3A7; "
            "ds_user_id=4791334445; s"
            "hbid=2755; "
            "shbts=1620822813.0845783; "
            "rur=FTW"
    }

    user_names = [i['user']['username'] for i in search_output['users'][:5]]
    user_ids = [i['user']['pk'] for i in search_output['users'][:5]]
    url = 'https://www.instagram.com/graphql/query/' \
          '?query_hash=c76146de99bb02f6415203be841dd25a&' \
          'variables={{"id":{},"include_reel":false,"fetch_mutual":false,"first":0}}'
    user_urls = [url.format(id) for id in user_ids]
    user_data = make_async_requests(user_urls, headers={**headers, **headers_}, proxies=proxies)
    user_data = [json.loads(i) for i in user_data]

    # parse info
    users = []
    for data, name in zip(user_data, user_names):
        user_info = {'username': name}
        user_info.update(parse_json_to_user_info(data))
        users.append(user_info)

    output = {
        'num_users': len(response.json()['users']),
        'users': users
    }

    return output


# # The following func is not longer used as there is a better solution!
# # TODO: hard to replicate but sometimes this parse does not do the job
# #  guess is that the response html structure depends on the caller location
# #  when doing this through proxy the response structure is not parsed sometimes
# #  maybe fix the proxy location?
# #  another solution would be to work with async calls and set single proxy for whole batch
# def parse_html_to_user_info(html):
#     """
#     Parses data from 'https://www.instagram.com/{username}/?__a=1'
#     """
#
#     output = {}
#     soup = BeautifulSoup(html, 'html.parser')
#
#     # TODO: private public?
#     # TODO: description
#     for item in soup.findAll('meta', attrs={'name': 'description', 'content': True}):
#         content = item.get('content')
#         if 'Followers' in content:
#             words = content.split()
#             # TODO: this does not work all the time
#             try:
#                 output['followers_count'] = int(words[0].replace('k', '00').replace(',', '').replace('.', ''))
#                 output['following_count'] = int(words[2].replace('k', '000').replace(',', '').replace('.', ''))
#                 output['posts_count'] = int(words[4].replace('k', '000').replace(',', '').replace('.', ''))
#             except:
#                 print('Failed to parse IG user info, now trying another html structure')
#                 continue
#             break
#
#     # if nothing was found then profile is set to private and html is structured differently
#     if not output:
#         js_items = soup.findAll('script', attrs={'type': 'text/javascript'})
#         for item in js_items:
#             # TODO: somehow the following line only works with beautifulsoup4==4.8.2
#             if 'edge_followed_by' in item.text:
#                 js_json = json.loads(item.text.replace('window._sharedData = ', '')[:-1])
#                 output['followers_count'] = int(js_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count'])
#                 output['following_count'] = int(js_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count'])
#                 output['posts_count'] = int(js_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count'])
#     return output