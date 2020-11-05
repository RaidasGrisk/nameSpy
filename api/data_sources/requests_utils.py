import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from log_config import logger

# create a session with:
# 1 .retries
# 2. timeouts
# 3. logging
# the code is overcomplicated for such a simple task
# but there seems to be no better solution..?


# https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 5
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
            del kwargs['timeout']
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get('timeout')
        if timeout is None:
            kwargs['timeout'] = self.timeout
        return super().send(request, **kwargs)


# https://stackoverflow.com/questions/51188661/adding-callback-function-on-each-retry-attempt-using-requests-urllib3
class RetryWithCallback(Retry):

    # use this method, to log error info on every new retry call
    def new(self, **kw):
        # kw = {'total': int, ..., 'history': tuple}
        last_error = kw['history'][-1].error
        if last_error:
            error_name = last_error.__class__.__name__
            # try get the url of the error else just include the whole error
            url = getattr(getattr(last_error, 'pool', None), 'host', None) or last_error
            logger.info(f'Request session: {url} {error_name}')
        return super(RetryWithCallback, self).new(**kw)


def requests_retry_session(retries=5, timeout=5):
    session = requests.Session()
    retry = RetryWithCallback(
        total=retries,
        read=retries,
        connect=retries,
    )
    adapter = TimeoutHTTPAdapter(timeout=timeout, max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


# test with localhost
# from log_config import handler as log_handler
#
# log_handler.flush()
# session = requests_retry_session(timeout=1, retries=2)
# r = session.get('http://localhost:1234', proxies={})
#
# [print(i) for i in log_handler.log]

"""
from flask import Flask
import time
app = Flask(__name__)


@app.route('/')
def hello():
    time.sleep(1)
    return 'Hi'

if __name__ == '__main__':
    app.run(port=1234)
"""