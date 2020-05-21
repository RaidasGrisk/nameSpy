from data_sources.google_scrape import get_google_search_scrape
from googletrans import Translator


def retry_if_google_search_fail(fn, max_tries=5):
    def wrapper(*args, **kwargs):
        for i in range(max_tries):
            output = fn(*args, **kwargs)
            if len(output['items']) == 0:
                print('Google returned 0 items, trying again {}'.format(i))
                continue
            return output
    return wrapper

def retry_if_google_numresults_fail(fn, max_tries=5):
    def wrapper(*args, **kwargs):
        for i in range(max_tries):
            output = fn(*args, **kwargs)
            if output == 0:
                print('Google did not return the number of results, trying again')
                continue
            return output
    return wrapper


@retry_if_google_search_fail
def google_search_scrape(person_name, exact_match, proxies, loc):

    def reorganize_data(search_results):
        data = {'items': []}
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

    search_results = get_google_search_scrape(person_name, exact_match, proxies, loc=loc)
    search_results = reorganize_data(search_results)

    return search_results


def google_translate(google_data, proxies):
    # https://github.com/ssut/py-googletrans
    # TODO: do in one batch by giving an array

    # collect items to translate
    snippets = [item['snippet'] for item in google_data['items']]
    titles = [item['title'] for item in google_data['items']]

    # okay, this is pretty ugly but here is what is being done:
    # I want to combine whole text into one string to send only one request to google translate
    # due to this snippets and titles are combined with special separator *||* (with hope that it will not break)
    # later on all is reorganized back to spippets and titles
    # text_to_translate = titles + snippets
    text_to_translate = [' ||| '.join([title + ' ||| ' + snippet for title, snippet in zip(titles, snippets)])]

    # clear non alpha num
    # e.g ☀ throws error in translator
    # re is fastest
    # https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
    # keep . and , and add else if needed
    text_to_translate = [re.sub(r"[^\w.,|']", ' ', text) for text in text_to_translate]

    # translate
    translator = Translator(proxies=proxies)
    translated = [item.text for item in translator.translate(text_to_translate, dest='en')]

    # ungroup
    # snippets_translated = translated[:len(snippets)]
    # titles_translated = translated[len(snippets):]
    titles_translated = translated[0].split('|||')[0::2]
    snippets_translated = translated[0].split('|||')[1::2]

    # assign
    for item, snippet, title in zip(google_data['items'], snippets_translated, titles_translated):
        item['snippet'] = snippet
        item['title'] = title

    return google_data


# ------ #
import requests
from bs4 import BeautifulSoup
import unidecode
import re
from fake_useragent.fake import UserAgent
import time

# TODO: this needs to be refactored and fixed, now its a mess
# TODO: generally, this must be combined with google_scrape and functions inside
# TODO: e.g. wrapper to try again, get_url etc.
@retry_if_google_numresults_fail
def get_google_search_num_items(person_name, proxies, exact_match=True):

    ua = UserAgent()
    USER_AGENT = {'User-Agent': ua.random}

    params = {}
    if exact_match:
        params['as_epq'] = person_name.encode('utf8')
    else:
        params['q'] = person_name.encode('utf8')

    https_bool = int(time.time()) % 2 == 0
    url = 'https://www.google.com/search' if https_bool else 'http://www.google.com/search'

    # make sure to set google search country code when using proxies
    # otherwise the results will differ with every proxy call
    # TODO: this should be the same country that no proxy search would return
    if proxies:
        params['gl'] = 'us'

    response = requests.get(url, params=params, headers=USER_AGENT, proxies=proxies)

    if 'https://www.google.com/recaptcha/api.js' in response.text:
        print('Google search returned captcha')
        return 0

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
