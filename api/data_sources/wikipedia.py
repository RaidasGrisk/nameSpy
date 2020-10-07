import requests
from log_config import logger

def get_wiki_search(query, exact_match=True):

    # wikipedia has many websites for specific language
    # E. g. english wiki: https://en.wikipedia.org/w/api.php
    # the one used below is supposed to be international
    # and search the whole wiki, instead of wiki of specific country
    # also: Quotes around words mark an "exact phrase" search.
    # For parameters they are also needed to delimit multi-word input.
    # source: https://www.mediawiki.org/wiki/Help:CirrusSearch#Prefer_phrase_matches
    url = 'https://www.wikidata.org/w/api.php?'
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
