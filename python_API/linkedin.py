from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def linkedin_users(input):

    # TODO: this requeres name and surename
    # TODO: what if second name, two names, etc?
    input = 'Raidas Griskevicius'
    input = input.split()
    endpoint = 'https://www.linkedin.com/pub/dir?firstName={}&lastName={}'.format(input[0], input[1])

    # cannot do this simple, have to emulate webbrowser
    # TODO: have to load this once inside a class
    def create_browser(webdriver_path):
        # browser_options = Options()
        # browser_options.add_argument("--headless")
        # browser_options.add_argument('--no-sandbox')
        browser = webdriver.Chrome(webdriver_path)
        return browser

    browser = create_browser('other/chromedriver')
    browser.get(endpoint)

    # parse items
    output = {}
    html = browser.page_source.replace('\n', '').replace('  ', '')
    soup = BeautifulSoup(html, 'html.parser')

    # this element will be available if query returns multiple accounts
    # otherwise it will redirect to the user account page
    multiple_users = soup.find('div', attrs={'class': 'base-serp-page'})

    if multiple_users:
        nr_results = soup.find('header', attrs={'class': 'serp-page__results-heading'}).text
        output['num_users'] = nr_results.split('results')[0]

        def extract_user_info_many(item):
            output = {}
            try:
                output['username'] = item.find('h3', attrs={'class': 'base-search-card__title'}).text
            except:
                pass
            try:
                output['job_title'] = item.find('h4', attrs={'class': 'base-search-card__subtitle'}).text
            except:
                pass
            try:
                output['sumary'] = item.find('p', attrs={'class': 'people-search-card__summary'}).text
            except:
                pass
            return output

        users = []
        for item in soup.findAll('li', attrs={'class': 'pserp-layout__profile-result-list-item'}):
            user_info = extract_user_info_many(item)
            users.append(user_info)
        output['users'] = users
    else:

        def extract_user_info_single(soup):
            output = {}
            try:
                output['username'] = soup.find('h1', attrs={'class': 'top-card-layout__title'}).text
            except:
                pass
            try:
                output['job_title'] = soup.find('h2', attrs={'class': 'top-card-layout__headline'}).text
            except:
                pass
            try:
                output['summary'] = soup.find('section', attrs={'class': 'summary pp-section'}).find('p').text[:100]
            except:
                pass
            return output

        output['num_users'] = 1
        user_info = extract_user_info_single(soup)

        output['users'] = [user_info]





