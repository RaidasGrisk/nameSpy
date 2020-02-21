from data_sources.google_scrape import get_google_search_scrape
from googleapiclient.discovery import build
from collections import Counter, OrderedDict
from private import GOOGLE_KEYS

from googletrans import Translator


def google_search_scrape(person_name, exact_match, pages=1):

    def reorganize_data(search_results):
        data = {'items': [], 'totalResults': search_results[0].number_of_results}
        for item in search_results:

            # little trick to fix bug inside name
            # it parses the text above the title containing a link
            # lets remove this as this is not what we want
            # point_of_remove = [i for i in item.link.split('/') if len(i) > 1][-1]
            # item.name = item.name.split(point_of_remove)[-1]

            data['items'].append({'displayLink': item.link,
                                  'snippet': item.description,
                                  'title': item.name})
        return data

    search_results = get_google_search_scrape(person_name, exact_match)
    search_results = reorganize_data(search_results)

    return search_results


def google_translate(search_results):
    # https://github.com/ssut/py-googletrans
    # TODO: do in one batch by giving an array

    # collect items to translate
    snippets = [item['snippet'] for item in search_results['items']]
    titles = [item['title'] for item in search_results['items']]
    text_to_translate = snippets + titles

    # translate
    translator = Translator()
    translated = [item.text for item in translator.translate(text_to_translate, dest='en')]

    # ungroup
    snippets_translated = translated[:len(snippets)]
    titles_translated = translated[len(snippets):]

    # assign
    for item, snippet, title in zip(search_results['items'], snippets_translated, titles_translated):
        item['snippet'] = snippet
        item['title'] = title

    return search_results


def google_search(person_name, num_pages=5):
    my_api_key = GOOGLE_KEYS['my_api_key']
    my_cse_id = GOOGLE_KEYS['my_cse_id']
    service = build("customsearch", "v1", developerKey=my_api_key)

    search_results = service.cse().list(q=person_name, cx=my_cse_id).execute()

    def process_google_response(google_response):
        output = {'totalResults': google_response['queries']['request'][0]['totalResults']}
        fields_to_parse_from_items = ['title',
                                      'displayLink',
                                      'snippet']
        parsed_items = []
        for item in google_response['items']:
            parsed_item_fields = {}
            for data_field in fields_to_parse_from_items:
                # print(data_field, item[data_field])
                parsed_item_fields[data_field] = item[data_field]
            parsed_items.append(parsed_item_fields)

        output['items'] = parsed_items

        return output

    search_results = process_google_response(search_results)

    return search_results


def get_google_data_analytics(search_results, nlp_models, person_name, ingore_name):

    def clean_text(text, nlp_models, person_name, ingore_name=True):
        import re
        import unicodedata

        output = text.replace('\n', ' ')
        output = re.sub(r'([^\s\w]|_)+', ' ', output).lower()  # remove non alphanum chars
        output = re.sub(r'[0-9]', ' ', output)  # remove numbers
        output = ''.join((c for c in unicodedata.normalize('NFD', output) if unicodedata.category(c) != 'Mn'))  # weird chars to latin
        output = output.replace('  ', ' ')  # replace double spaces with space
        output = re.sub(r'\b[a-z]{1,2}\b', ' ', output)  # remove words that are 2 or less chars

        # remove stop words
        nlp = nlp_models['EN']
        output = ' '.join(token.lemma_ for token in nlp(output) if not token.is_stop)

        # remove name and surename
        # TODO:  liet raides ir lot, etc, previous cleaning should apply to this
        if ingore_name:
            for name_part in person_name.split():
                name_part = name_part.lower()
                output = output.replace(name_part, '')

        return output

    # combine into one string
    text_items_combined = ' '.join([item['snippet'] + ' ' + item['title'] for item in search_results['items']])

    # extract entities
    # from helpers import get_entities
    # nlp = nlp_models['EN']
    # entities = get_entities(text_items_combined, {'EN': nlp})

    # count words
    text_items_cleaned = clean_text(text_items_combined, nlp_models, person_name, ingore_name)
    frequent_words = OrderedDict(Counter(text_items_cleaned.split()).most_common()[:25])

    return {'frequent_words': frequent_words}


# ------ #
import requests
from bs4 import BeautifulSoup
import unidecode
import re


def get_google_search_num_items(person_name):

    USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    params = {'q': person_name}
    response = requests.get('https://www.google.com/search', params=params, headers=USER_AGENT)

    soup = BeautifulSoup(response.text, "html.parser")
    results_div = soup.find("div", attrs={"id": ["resultStats", 'slim_appbar']})

    def _get_number_of_results(results_div):
        """Return the total number of results of the google search.
        Note that the returned value will be the same for all the GoogleResult
        objects from a specific query."""
        try:
            results_div_text = results_div.get_text()
            results_div_text = unidecode.unidecode(results_div_text)
            results_div_text = results_div_text.replace(' ', '').replace(',', '').replace('.', '')
            if results_div_text:
                regex = r"[\d\s]+(?:\.(?:\s*\d){2,4})?"
                m = re.findall(regex, results_div_text)

                # Clean up the number
                num = m[0]

                results = int(num)
                return results
        except Exception as e:
            print(e)
            return 0

    output = _get_number_of_results(results_div)
    print(output)
    return output