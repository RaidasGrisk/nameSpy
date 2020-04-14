from endpoint_get_job_title import app as job_title_app
from endpoint_get_social_score import app as social_score_app
import urllib
import json

# -------- #
with job_title_app.test_client() as c:

    inputs = [
        {'input': 'carl hust',
         'ner_threshold': 0.90,
         'google_search_loc': 'gb'},

        {'input': 'melissa respondek',
         'ner_threshold': 0.90,
         'google_search_loc': 'lt'},

        {'input': 'egle tauraite',
         'ner_threshold': 0.95,
         'google_search_loc': 'lt'},

        {'input': 'John Lee',
         'ner_threshold': 0.95,
         'google_search_loc': 'lt'},

        {'input': 'Bart Simpson',
         'google_search_loc': 'us'},

        {'input': 'Jurgita Antuchevičienė',
         'google_search_loc': 'lt'}
    ]

    for input in inputs:
        resp = c.get('api/job_title?{}'.format(urllib.parse.urlencode(input)))
        print(json.loads(resp.data))
        print('\n\n')

# ---------- #
with social_score_app.test_client() as c:

    inputs = [
        {'input': 'carl hust',
         'ner_threshold': 0.90,
         'google_search_loc': 'gb'},

        {'input': 'melissa respondek',
         'ner_threshold': 0.90,
         'google_search_loc': 'lt'},

        {'input': 'egle tauraite',
         'ner_threshold': 0.95,
         'google_search_loc': 'lt'},

        {'input': 'John Lee',
         'ner_threshold': 0.95,
         'google_search_loc': 'lt'},

        {'input': 'Bart Simpson',
         'google_search_loc': 'us'}
    ]

    for input in inputs:
        resp = c.get('api/social_score?{}'.format(urllib.parse.urlencode(input)))
        print(json.loads(resp.data))
        print('\n\n')
