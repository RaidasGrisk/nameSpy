from data_sources.google import google_search, google_search_scrape, get_google_data_analytics
from data_sources.instagram import instagram_users

from helpers import get_entities, process_entities
from globals import nlp_models


# combine the output
def get_api_data(input):
    entities = get_entities(input, nlp_models)
    person_name = process_entities(entities)
    google_data = google_search_scrape(person_name)
    google_analytics = get_google_data_analytics(google_data, nlp_models)
    instagram_data = instagram_users(person_name)

    # making final output
    output = dict()
    output['input_raw'] = input
    output['input_entities'] = entities

    output['google'] = {'items': google_data['totalResults'], 'analysis': google_analytics}
    print('IG')
    output['instagram'] = instagram_data
    print('done')

    return output
