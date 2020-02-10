import requests

input = 'Raidas Griskevicius'
endpoint = 'https://api.twitter.com/1.1/users/lookup.json?screen_name={}'.format(input)
oauth_consumer_key = 'PrstHGkvSNyYHDYchun8vxiPiNtP3fLQgBXiKpktDz1n8IU5tU'
response = requests.get('https://website.com/id', headers={'Authorization': 'OAuth oauth_consumer_key="{}"'.format(oauth_consumer_key)})



import base64
#Define your keys from the developer portal
client_key = 'mPgpDSjjToaPbqGnLk3JnxSzG'
client_secret = 'PrstHGkvSNyYHDYchun8vxiPiNtP3fLQgBXiKpktDz1n8IU5tU'
#Reformat the keys and encode them
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

# Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)
#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')


import requests
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

access_token = auth_resp.json()['access_token']


search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

search_params = {
    'screen_name': 'Karolis matuliauskas',
    'user_id': '',
    'include_entities': False,
    'tweet_mode': False
}
search_url = '{}1.1/users/lookup.json'.format(base_url)
search_resp = requests.get(search_url, headers=search_headers, params=search_params)
print(search_resp.text)