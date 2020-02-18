from find_job_titles import Finder
from helpers import get_domain_from_url


def get_job_titles(google_data):

    titles_parsed = []
    finder = Finder()
    for item in google_data['items']:
        title_parsed = {}
        try:
            job_titles = finder.findall(item['title'] + '. ' + item['snippet'])
            job_titles = [title.match for title in job_titles]
            source = get_domain_from_url(item['displayLink'])
            title_parsed[source] = list(set(job_titles))
            titles_parsed.append(title_parsed)
        except RuntimeError:
            continue

    return titles_parsed