# data
# http://www.varduzinynas.lt/moteru-vardai?page=40
# http://lkiis.lki.lt/pavardziu-duomenu-baze

import spacy
from googleapiclient.discovery import build
from collections import Counter, OrderedDict

from private import GOOGLE_KEYS

# separate endpoints
from instagram import instagram_users

# define models
nlp_models = {'LTU': spacy.load('lt_core_news_sm'),
              'EN': spacy.load('en_core_web_sm')}


def get_entities(input, nlp_models):

    # get all entities
    entities = {}
    for model_lang, nlp_model in nlp_models.items():
        doc = nlp_model(input)
        if doc.ents:
            for ent in doc.ents:
                ent_str = str(ent)
                print(model_lang, ent.text, ent.label_)
                if ent.label_ in entities.keys():
                    entities[ent.label_].add(ent_str)
                else:
                    entities[ent.label_] = set([ent_str])
        else:
            print(model_lang, '-')

    # convert to decent dict
    for key, value in entities.items():
        entities[key] = list(value)

    return entities


def process_entities(entities):

    # analyze and return
    if 'PERSON' in entities.keys():

        if len(entities['PERSON']) > 1:
            print(entities['PERSON'])
            return list(entities['PERSON'])[0]
        else:
            return list(entities['PERSON'])[0]
    else:
        print('No manes here')
        return None


def google_search(person_name, num_pages=5):
    my_api_key = GOOGLE_KEYS['my_api_key']
    my_cse_id = GOOGLE_KEYS['my_cse_id']
    service = build("customsearch", "v1", developerKey=my_api_key)

    res = service.cse().list(q=person_name, cx=my_cse_id).execute()
    if num_pages > 1:
        for start in range(1, num_pages):
            start *= 10
            start += 1
            next_page = service.cse().list(q=person_name, cx=my_cse_id, start=start).execute()
            res['items'] = res['items'] + next_page['items']

    return res


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


def get_google_data_analytics(google_data):

    def clean_text(input):
        import re
        import unicodedata
        output = input.replace('\n', '')
        output = re.sub(r'([^\s\w]|_)+', '', output).lower()
        output = ''.join((c for c in unicodedata.normalize('NFD', output) if unicodedata.category(c) != 'Mn'))
        return output

    text_items_combined = ' '.join([item['snippet'] + ' ' + item['title'] for item in google_data['items']])
    text_items_cleaned = clean_text(text_items_combined)
    frequent_words = OrderedDict(Counter(text_items_cleaned.split()).most_common()[:25])

    return frequent_words

# tests
# input = 'Povilas Dargis'
# entities = get_entities(input, nlp_models)
# person_name = process_entities(entities)
# google_response = google_search(person_name)
# google_data = process_google_response(google_response)
# google_analytics = get_google_data_analytics(google_data)

# output = {}
# output['input_raw'] = input
# output['input_entities'] = entities
# output['google'] = {'items': google_data['totalResults'], 'freq_words': google_analytics}
# print(json.dumps(output, indent=4, sort_keys=False))


# combine the output
def get_api_data(input):
    entities = get_entities(input, nlp_models)
    person_name = process_entities(entities)
    google_response = google_search(person_name)
    google_data = process_google_response(google_response)
    google_analytics = get_google_data_analytics(google_data)
    instagram_data = instagram_users(person_name)

    # making final output
    output = dict()
    output['input_raw'] = input
    output['input_entities'] = entities

    output['google'] = {'items': google_data['totalResults'], 'freq_words': google_analytics}
    print('IG')
    output['instagram'] = instagram_data
    print('done')

    return output
