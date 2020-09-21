from endpoint_get_job_title import app as job_title_app
from endpoint_get_social_score import app as social_score_app
import urllib
import json

# -------- #
with job_title_app.test_client() as c:

    inputs = [
        {'input': 'carl hust',
         'ner_threshold': 0.90,
         'country_code': 'gb',
         'debug': 1},

        {'input': 'melissa respondek',
         'ner_threshold': 0.90,
         'country_code': 'lt',
         'debug': 1},

        {'input': 'egle tauraite',
         'ner_threshold': 0.95,
         'country_code': 'lt',
         'use_proxy': 0,
         'debug': 1},

        {'input': 'John Lee',
         'ner_threshold': 0.95,
         'country_code': 'lt',
         'use_proxy': 1,
         'debug': 1},

        {'input': 'Bart Simpson',
         'country_code': 'us',
         'debug': 1},

        {'input': 'Jurgita Antuchevičienė',
         'country_code': 'lt',
         'use_proxy': 1,
         'debug': 1}
    ]

    for input in inputs:
        resp = c.get('api/job_title?{}'.format(urllib.parse.urlencode(input)))
        print(json.dumps(json.loads(resp.data), indent=4))
        print('\n\n')

# ---------- #
with social_score_app.test_client() as c:

    inputs = [
        {'input': 'carl hust',
         'ner_threshold': 0.90,
         'country_code': 'gb',
         'debug': 1},

        {'input': 'melissa respondek',
         'ner_threshold': 0.90,
         'country_code': 'lt',
         'debug': 1},

        {'input': 'egle tauraite',
         'ner_threshold': 0.95,
         'country_code': 'lt',
         'use_proxy': 1,
         'debug': 1},

        {'input': 'John Lee',
         'ner_threshold': 0.95,
         'country_code': 'lt',
         'use_proxy': 1,
         'debug': 1},

        {'input': 'Bart Simpson',
         'country_code': 'us',
         'use_proxy': 1,
         'collected_data': 0,
         'debug': 1},

        {'input': 'lady gaga',
         'country_code': 'us',
         'use_proxy': 1,
         'collected_data': 0,
         'debug': 1}
    ]

    for input in inputs:
        resp = c.get('api/social_score?{}'.format(urllib.parse.urlencode(input)))
        print(json.dumps(json.loads(resp.data), indent=4))
        print('\n\n')
