from google import google
from googleapiclient.discovery import build
from collections import Counter, OrderedDict
from private import GOOGLE_KEYS

from googletrans import Translator


def google_search_scrape(person_name, num_pages=1):

    def reorganize_data(search_results):
        data = {'items': [], 'totalResults': search_results[0].number_of_results}
        for item in search_results:

            # little trick to fix bug inside name
            # it parses the text above the title containing a link
            # lets remove this as this is not what we want
            point_of_remove = [i for i in item.link.split('/') if len(i) > 1][-1]
            item.name = item.name.split(point_of_remove)[-1]

            data['items'].append({'displayLink': item.link,
                                  'snippet': item.description,
                                  'title': item.name})
        return data

    search_results = google.search(person_name, num_pages)
    search_results = reorganize_data(search_results)

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


def google_translate(search_results):
    # https://github.com/ssut/py-googletrans
    # TODO: do in one batch by giving an array
    translator = Translator()
    for item in search_results['items']:
        item['snippet'] = translator.translate(item['snippet'], dest='en').text
        item['title'] = translator.translate(item['title'], dest='en').text
    return search_results


def get_google_data_analytics(search_results, nlp_models):

    def clean_text(input):
        import re
        import unicodedata

        output = input.replace('\n', ' ')
        output = re.sub(r'([^\s\w]|_)+', ' ', output).lower()  # remove non alphanum chars
        output = re.sub(r'[0-9]', ' ', output)  # remove numbers
        output = ''.join((c for c in unicodedata.normalize('NFD', output) if unicodedata.category(c) != 'Mn'))  # weird chars to latin
        output = output.replace('  ', ' ')  # replace double spaces with space
        output = re.sub(r'\b[a-z]{1,2}\b', '', output)  # remove words that are 2 or less chars

        # remove stop words
        # TODO: this is slow, have to load and reuse
        import spacy
        nlp = spacy.load('en_core_web_sm', parser=False, entity=False)
        output = ' '.join(token.lemma_ for token in nlp(output) if not token.is_stop)

        return output

    # translate
    search_results = google_translate(search_results)

    # combine into one string
    text_items_combined = ' '.join([item['snippet'] + ' ' + item['title'] for item in search_results['items']])
    text_items_cleaned = clean_text(text_items_combined)
    frequent_words = OrderedDict(Counter(text_items_cleaned.split()).most_common()[:25])

    return {'entities': [], 'frequent_words': frequent_words}

# from other.main import pretty_print_json
# pretty_print_json(search_results)
