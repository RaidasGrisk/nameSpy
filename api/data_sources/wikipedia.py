import requests
from log_cofig import logger

def get_wiki_search(query, exact_match=True):

    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': '"' + query + '"' if exact_match else query
    }
    logger.info('Sending a request to wikipedia')
    wiki_json = requests.get(url, params=params).json()

    output = {'items': wiki_json['query']['searchinfo']['totalhits'],
              'wordcount': sum([i['wordcount'] for i in wiki_json['query']['search']])}

    return output
