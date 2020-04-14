import requests
import random
from bs4 import BeautifulSoup

# this is supposed to turn off info logging
# https://stackoverflow.com/questions/29651505/disable-info-logging-messages-in-ipython-notebook
# the issue is that tor constantly outputs the following:
# INFO:stem:Error while receiving a control message (SocketClosed): received exception "read of closed file"
# this eats up logging space in google cloud so lets try turning this off
import logging
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')

    proxies = set()
    for row in table.findAll('tr'):
        ip = row.findAll('td')[0].getText()
        port = row.findAll('td')[1].getText()
        scheme = ['https://' if row.findAll('td')[6].getText() == 'yes' else 'http://'][0]
        proxy = scheme + ip + ':' + port
        proxies.add(proxy)

    return proxies


proxies = get_proxies()
url = 'https://httpbin.org/ip'
for i in range(1, 100):
    proxy = random.sample(proxies, 1)[0]
    print(proxy)
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=1)
        print(response.json())
    except Exception as e:
        #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
        #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
        print(e)