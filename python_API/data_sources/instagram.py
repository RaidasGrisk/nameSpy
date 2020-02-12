import requests
from bs4 import BeautifulSoup


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
            output['Followers'] = words[0].replace('k', '00').replace(',', '').replace('.', '')
            output['Following'] = words[2].replace('k', '000').replace(',', '').replace('.', '')
            output['Posts'] = words[4].replace('k', '000').replace(',', '').replace('.', '')
            break

    return output


def instagram_users(input):

    # user search endpoint
    input = input.replace(' ', '+')
    endpoint = 'https://www.instagram.com/web/search/topsearch/?context=blended&query={}'.format(input)
    response = requests.get(endpoint)
    search_output = response.json()

    # remove some fields
    for user in search_output['users']:
        del user['user']['profile_pic_url']

    # limit number of users to go on with
    # TODO: dicts are unordered!
    search_output['users'] = search_output['users'][:5]
    search_output['hashtags'] = search_output['hashtags'][:5]

    for user in search_output['users']:
        basic_info = get_basic_info(user['user']['username'])
        user['basic_info'] = basic_info

    output = {}
    output['num_users'] = len(response.json()['users'])
    output['data'] = search_output

    return output
