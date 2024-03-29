from googletrans import Translator
from data_sources.requests_utils import requests_retry_session
import re
from log_config import logger
from functools import wraps


# this works on the premise that the fn will be ran
# again if it returns False, else the loop will stop
# https://towardsdatascience.com/are-you-using-python-with-apis-learn-how-to-use-a-retry-decorator-27b6734c3e6
# https://blog.miguelgrinberg.com/post/the-ultimate-guide-to-python-decorators-part-iii-decorators-with-arguments
def retry_if_fn_returned_false(max_tries=5):
    def inner(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for i in range(max_tries):
                logger.info(f'Trying {fn.__name__} {i}')
                output = fn(*args, **kwargs)
                if output:
                    return output
        return wrapper
    return inner


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
    # Translator creates its own requests session, so lets
    # modify it to retry on fail connection / other errors
    # else, the code will fail at this point with broken conn
    translator = Translator(proxies=proxies, timeout=5)

    # the following would overwrite a couple of things
    # also would force token acquisition to be done via proxy
    # none of this is good, so lets not do this and use the default session
    # translator.session = requests_retry_session(retries=0, timeout=5)

    # temp fix: https://github.com/ssut/py-googletrans/issues/234
    # from the looks of it, it seems the issue will be soon fixed
    # also this is good for cases when proxy connection fails
    for _ in range(5):
        try:
            translated = [item.text for item in translator.translate(text_to_translate, dest='en')]
            logger.info('Successfully google translated text')
            break
        except Exception as e:
            logger.info(f'google translate error {_}')
            translator = Translator(proxies=proxies, timeout=5)

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
from fake_useragent.fake import UserAgent


@retry_if_fn_returned_false(max_tries=5)
def get_google_search_response(person_name, exact_match, proxies, country_code):

    # set params
    params = {
        'as_epq' if exact_match else 'q': person_name.encode('utf8')
    }

    # make sure to set google search country code because
    # when using proxies the google results will depend on
    # the random country the proxy is located at and
    # the results will differ with every random proxy call

    # also keep in mind that including this parameter (as well as others, likely)
    # will increase the prob of triggering bot detection
    # so using this without a proxy will quickly result
    # in google banning the ip address and asking for recaptcha

    # set lr and cr params, maybe both of the will result
    # in actually simulating a search from specified country
    # source: https://github.com/MarioVilas/googlesearch/blob/master/googlesearch/__init__.py

    # as of 2021 the request triggers some kind of google protection
    # by not rendering the full page in html. Depending on the exact params set
    # in the html returned it says "Jei per kelias sekundes nebūsite nukreipti, <...>"
    # or just returns a different html structure that does not include div slim_appbar.
    # div slim_appbar contains the number of total results and we want to parse it.
    #
    # For future reference, the following does not help:
    # following the url provided together with "if you are not redirected within a few".
    # fixing proxy location (in private.py) e.g. US only.
    # do not setting cr lr params.
    if proxies:
        pass
        # params['cr'] = 'us'
        # params['lr'] = 'lang_' + 'us'
    if country_code:
        pass
        # params['cr'] = country_code
        # params['lr'] = 'lang_' + country_code

    # set headers - this is important!!!
    # if headers are not set google does not return
    # the number of search results and none of the divs
    # responsible for storing number of results are there.
    # Basically, the structure of html is totally different.
    # IMPORTANT: the above holds for requests sent directly
    # IMPORTANT: and for requests send through a proxy.

    # UserAgent() is a heroku app that sometimes fails
    # lets save a list of browsers for headers locally,
    # so that we don't have to call the heroku app
    # again and again every time.
    # Randomising from locally stored browsers does
    # increase the rate of captcha and invalid responses
    # For now lets fall back to UserAgent and investigate
    # the reasons later on.
    headers = {'User-Agent': UserAgent().random}
    # headers = {'User-Agent': random.choice(browsers)}

    # make the request
    url = 'https://www.google.com/search'
    response = requests_retry_session().get(url,
                                            params=params,
                                            headers=headers,
                                            proxies=proxies)

    # if recaptcha in the response, the client that sent the request
    # is blacklisted so lets return False
    if 'https://www.google.com/recaptcha/api.js' in response.text:
        logger.info('Received Captcha request (google search)')
        return False

    logger.info('Received a valid response (google search)')
    return response


@retry_if_fn_returned_false(max_tries=2)
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
        # TODO: this part has problems.
        #  recently it started to fail to parse snippets.
        #  Quick fix: s -> IsZvec and st -> aCOpRe
        #  These classes might be temporary
        #  but for now range across many countries.
        sdiv = li.find('div', attrs={'class': 'IsZvec'})  # s / IsZvec
        if sdiv:
            stspan = sdiv.find('span', attrs={'class': 'aCOpRe'})  # st / aCOpRe
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
