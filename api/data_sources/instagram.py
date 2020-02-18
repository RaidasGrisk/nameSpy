import requests
from bs4 import BeautifulSoup
import json


def get_basic_info(user_name):

    output = {}

    instagram_page = requests.get('https://www.instagram.com/' + user_name)
    soup = BeautifulSoup(instagram_page.text, 'html.parser')

    # TODO: private public?
    # TODO: description
    for item in soup.findAll('meta', attrs={'name': 'description', 'content': True}):
        content = item.get('content')
        if 'Followers' in content:
            words = content.split()
            output['followers_count'] = int(words[0].replace('k', '00').replace(',', '').replace('.', ''))
            output['following_count'] = int(words[2].replace('k', '000').replace(',', '').replace('.', ''))
            output['posts_count'] = int(words[4].replace('k', '000').replace(',', '').replace('.', ''))
            break

    # if nothing was found then profile is set to private and html is structured differently
    if not output:
        js_items = soup.findAll('script', attrs={'type': 'text/javascript'})
        for item in js_items:
            if 'edge_followed_by' in item.text:
                js_json = json.loads(item.text.replace('window._sharedData = ', '')[:-1])
                # js_json['country_code']
                output['followers_count'] = int(js_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count'])
                output['following_count'] = int(js_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count'])
                output['posts_count'] = int(js_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count'])

    return output


def instagram_users(input):

    # user search endpoint
    input = input.replace(' ', '+')
    endpoint = 'https://www.instagram.com/web/search/topsearch/?context=blended&query={}'.format(input)
    response = requests.get(endpoint)
    search_output = response.json()

    users = []
    for user in search_output['users'][:5]:
        basic_info = get_basic_info(user['user']['username'])
        user_info = {'username': user['user']['username']}
        user_info.update(basic_info)
        users.append(user_info)

    output = {}
    output['num_users'] = len(response.json()['users'])
    output['users'] = users

    return output
