import requests
from bs4 import BeautifulSoup
import json
from data_sources.async_utils import make_async_requests
from data_sources.requests_utils import requests_retry_session

# TODO: hard to replicate but sometimes this parse does not do the job
# TODO: guess is that the response html structure depends on the caller location
# TODO: when doing this through proxy the response structure is not parsed sometimes
# TODO: maybe fix the proxy location?
# TODO: another solution would be to work with async calls and set single proxy for whole batch
def parse_html_to_user_info(html):

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


def get_instagram_users(input, proxies):

    # user search endpoint
    # get usernames associated with name surname
    url = 'https://www.instagram.com/web/search/topsearch'
    params = {'query': input.replace(' ', '+'), 'context': 'blended'}

    response = requests_retry_session().get(url, params=params, proxies=proxies)
    search_output = response.json()

    # get htmls of user pages
    # make async calls to save some time
    user_names = [i['user']['username'] for i in search_output['users'][:5]]
    user_pages = ['https://www.instagram.com/' + i for i in user_names]
    user_pages_html = make_async_requests(user_pages, proxies)

    # parse info from htmls
    users = []
    for user_html, username in zip(user_pages_html, user_names):
        basic_info = parse_html_to_user_info(user_html)
        user_info = {'username': username}
        user_info.update(basic_info)
        users.append(user_info)

    output = {}
    output['num_users'] = len(response.json()['users'])
    output['users'] = users

    return output

