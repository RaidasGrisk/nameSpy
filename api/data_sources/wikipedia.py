import requests


def get_wiki_search(input, exact_match=True):

    # https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=albert einstein
    url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch='
    if exact_match:
        input = '"' + input + '"'
    page = requests.get(url + input)
    wiki_json = page.json()

    output = {'totalhits': wiki_json['query']['searchinfo']['totalhits'],
              'wordcount': sum([i['wordcount'] for i in wiki_json['query']['search']])}
    return output
