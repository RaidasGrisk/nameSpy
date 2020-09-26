from googletrans import Translator
from data_sources.requests_utils import requests_retry_session
from log_config import logger

# this works on the premise that the fn will be ran
# again if it returns False, else the loop will stop
def retry_if_fn_returned_false(fn, max_tries=5):
    def wrapper(*args, **kwargs):
        for i in range(max_tries):
            logger.info(f'Trying {fn.__name__} {i}')
            output = fn(*args, **kwargs)
            if not output:
                continue
            return output
    return wrapper


def google_translate(google_data, proxies):
    # https://github.com/ssut/py-googletrans
    # TODO: do in one batch by giving an array

    # collect items to translate
    snippets = [item['snippet'] for item in google_data['items']]
    titles = [item['title'] for item in google_data['items']]

    # okay, this is pretty ugly but here is the idea:
    # I want to combine whole text into one string to send only one request to google translate
    # due to this snippets and titles are combined with special separator *||* (with hope that it will not break)
    # later on all is reorganized back to snippets and titles
    # text_to_translate = titles + snippets
    text_to_translate = [' ||| '.join([title + ' ||| ' + snippet for title, snippet in zip(titles, snippets)])]

    # clear non alpha num
    # e.g ☀ throws error in translator
    # re is fastest
    # https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
    # keep . and , and add else if needed
    text_to_translate = [re.sub(r"[^\w.,|']", ' ', text) for text in text_to_translate]

    # translate
    # TODO: Translator creates its own requests session, so I
    #  should find a way to make it repeat the call to the server
    #  if proxy fails and throws connection timeout error
    translator = Translator(proxies=proxies)
    translated = [item.text for item in translator.translate(text_to_translate, dest='en')]
    logger.info('Successfully google translated text')

    # ungroup and split back to snippets and titles
    titles_translated = translated[0].split('|||')[0::2]
    snippets_translated = translated[0].split('|||')[1::2]

    # assign
    for item, snippet, title in zip(google_data['items'], snippets_translated, titles_translated):
        item['snippet'] = snippet
        item['title'] = title

    return google_data


# ------ #
from bs4 import BeautifulSoup
import unidecode
import re
from fake_useragent.fake import UserAgent


@retry_if_fn_returned_false
def get_google_search_response(person_name, exact_match, proxies, country_code):

    # set params
    params = {
        'as_epq' if exact_match else 'q': person_name.encode('utf8')
    }

    # make sure to set google search country code because
    # when using proxies the google results will depend on
    # the random country the proxy is located at and
    # the results will differ with every random proxy call
    #
    # also keep in mind that including this parameter (as well as others, likely)
    # will increase the prob of triggering bot detection
    # so using this without a proxy will quickly result
    # in google banning the ip address and asking for recaptcha
    # TODO: even though the parameter is set, the search results
    #  differ when returned from different proxy/client
    #  maybe this is fine as this returns different search results
    #  implying that it is actually working in terms of loc spec
    #  it might vary just because it varies by default in the loc
    if proxies:
        params['gl'] = 'us'
    if country_code:
        params['gl'] = country_code

    # set headers - this is important!!!
    # if headers are not set google does not return
    # the number of search results and none of the divs
    # responsible for storing number of results are there.
    # Basically, the structure of html is totally different.
    # TODO: not sure if need to use UserAgent() as sometimes it
    #  fails, maybe just pick from a random of 10 headers
    #  stored locally? Not sure if this is good long term solution
    headers = {'User-Agent': UserAgent().random}

    # make the request
    url = 'https://www.google.com/search'
    response = requests_retry_session().get(url,
                                            params=params,
                                            headers=headers,
                                            proxies=proxies)

    # if recaptcha in the response, the client that sent the request
    # is blacklisted so lets return False
    if 'https://www.google.com/recaptcha/api.js' in response.text:
        logger.info('Received Captcha request')
        return False

    logger.info('Received a valid response')
    return response


@retry_if_fn_returned_false
def get_google_search_result_count(person_name, exact_match, proxies, country_code):

    """
    Returns either bool False or int as number of search results found.
    False will trigger the decorator to run this exact function again
    with a hope to get the function to return an int.

    Major problem with it is that the results are chaotic and not
    reproducible because google returns different structures depending
    on the random proxy though which the requests is being sent.
    """

    response = get_google_search_response(person_name, exact_match, proxies, country_code)

    # parse the results and extract the part of html
    # which contains the number of search results found
    soup = BeautifulSoup(response.text, 'html.parser')
    results_div = soup.find('div', attrs={'id': ['resultStats', 'slim_appbar']})

    # TODO: what if the results are in fact 0? e.g. sosicc cequel tycoonkingz
    #  have to find a way to separate this case from other cases where we return False.
    #  It should look something like this: if X (no results found) is in soup: return 0
    if not results_div or not results_div.__getattribute__('text'):
        logger.info('Google search does not contain the search results div / or there are 0 results')
        return False

    def _parse_number_of_results(results_div_text):
        """
        parse total number of search results given the text
        inside the div that should hold the number.

        Basically the function finds numbers in the string and
        returns the first number found as int
        """

        # clean the string by removing space and commas
        # what we want is glued string from which we can
        # easily extract the first number found
        results_div_text = unidecode.unidecode(results_div_text)
        results_div_text = ''.join([i for i in results_div_text if i.isalpha() or i.isnumeric()])

        # first number is the one we are looking for
        # the second number should be the time it took
        # for google to return the search results
        # e.g Apie 54 500 000 rezult. (0,67 sek.)
        regex = r"[\d\s]+(?:\.(?:\s*\d){2,4})?"
        m = re.search(regex, results_div_text)
        results = int(m.group())

        return results

    number_of_results = _parse_number_of_results(results_div.__getattribute__('text'))
    return number_of_results


def get_google_search_result_items(person_name, exact_match, proxies, country_code):
    """
    Parse google search response html into a list where each list item is 
    a dict containing single search result item
    e.g. [{'title': 'a', 'snippet': 'a', 'url': 'a'}, ...]
    """
    
    response = get_google_search_response(person_name,
                                          exact_match,
                                          proxies,
                                          country_code)

    soup = BeautifulSoup(response.text, 'html.parser')
    items_found = soup.findAll('div', attrs={'class': 'g'})

    def _get_title(item):
        a = item.find('h3')
        if a is not None:
            return a.text.strip()
        return None

    def _get_snippet(li):
        sdiv = li.find('div', attrs={'class': 's'})
        if sdiv:
            stspan = sdiv.find('span', attrs={'class': 'st'})
            if stspan is not None:
                return stspan.text.strip()
        else:
            return None

    def _get_url(li):
        try:
            a = li.find('a')
            link = a['href']
        except Exception:
            return None
        return link

    search_result_items = []
    for item in items_found:

        search_result_ = {
            'title': _get_title(item),
            'snippet': _get_snippet(item),
            'url': _get_url(item)
        }

        # sometimes some other items make it into the items_found list
        # an example: "John Lee" -> {title': 'x', 'snippet': None}
        # so remove items where titles or snippets are None
        if search_result_['title'] and search_result_['snippet']:
            search_result_items.append(search_result_)

    # make sure the output is clean and can be used easily in the next steps

    return {'items': search_result_items}
