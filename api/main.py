from data_sources.google import google_search, get_google_data_analytics, google_search_scrape
# from data_sources.google_scrape import google_search_scrape
from data_sources.instagram import instagram_users

from helpers import get_entities, process_entities
from globals import nlp_models


# combine the output
def get_api_data(input):

    print('Starting')
    entities = get_entities(input, nlp_models)
    print(entities)
    person_name = process_entities(entities)

    print('Google search')
    google_data = google_search_scrape(person_name, exact_match=True, pages=1)
    print('Google analytics')
    google_analytics = get_google_data_analytics(google_data, nlp_models, person_name, ingore_name=True)
    print('Instagram')
    instagram_data = instagram_users(person_name)

    # making final output
    output = dict()
    output['input_raw'] = input
    output['input_entities'] = entities

    output['google'] = {'items': google_data['totalResults'], 'analysis': google_analytics}
    output['instagram'] = instagram_data

    return output
