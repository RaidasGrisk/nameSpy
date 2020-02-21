from data_sources.google import google_search, get_google_data_analytics, google_search_scrape, google_translate
# from data_sources.google_scrape import google_search_scrape
from data_sources.instagram import instagram_users
from data_sources.wikipedia import get_wiki_search
from data_sources.twitter import get_twitter_users
from data_sources.google_scrape import get_google_search_scrape

from job_titles.find_job_titles import get_job_titles as get_job_titles_1
from job_titles.core_nlp_ner import get_job_titles as get_job_titles_2

from helpers import get_entities, process_entities
from globals import nlp_models


def get_job_title(input):

    entities = get_entities(input, nlp_models)
    print(entities)
    person_name = process_entities(entities)

    print('Google search')
    google_data = google_search_scrape(person_name, exact_match=True, pages=1)
    print('Google translate')
    google_data = google_translate(google_data)

    print('Job titles')
    job_titles_1 = get_job_titles_1(google_data)
    job_titles_2 = get_job_titles_2(google_data)
    job_titles = {'py': job_titles_1, 'stanfordNLP': job_titles_2}

    # making final output
    output = dict()
    output['input_raw'] = input
    output['input_entities'] = entities

    output['google_data'] = {'job_title': job_titles}

    return output


# combine the output
def get_social_score(input):

    entities = get_entities(input, nlp_models)
    print(entities)
    person_name = process_entities(entities)

    print('Google counts')
    google_counts = get_google_search_scrape(person_name, exact_match=True, pages=1, number_of_results_only=True)
    print('Wikipedia')
    wiki_data = get_wiki_search(person_name)
    print('Instagram')
    instagram_data = instagram_users(person_name)
    print(instagram_data)
    print('Twitter')
    twitter_data = get_twitter_users(person_name)

    # making final output
    output = dict()
    output['input_raw'] = input
    output['input_entities'] = entities

    output['google'] = google_counts
    output['wikipedia'] = wiki_data
    output['twitter'] = twitter_data
    output['instagram'] = instagram_data

    return output
