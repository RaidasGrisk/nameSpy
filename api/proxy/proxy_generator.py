
"""
# https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b
# https://stackoverflow.com/questions/48117693/python-stemrequests-not-switching-circut-changing-ip-address-when-using-a-sess

The password and ControlPort must be set inside /etc/tor/torrc. Here's an excerpt form dockerfile
RUN echo HashedControlPassword $(tor --hash-password "abs123" | tail -n 1) >> /etc/tor/torrc
RUN echo "ControlPort 9051" >> /etc/tor/torrc

"""


from stem import Signal
from stem.control import Controller
import requests
from datetime import datetime

from googletrans import Translator


class ProxyChanger:

    def __init__(self, tor_password):
        self.last_change = datetime.now()
        self.tor_password = tor_password

    def get_new_proxy(self, minutes_between_changes, connection_check, total_retries=5):

        """
        :param minutes_between_changes:
        :param connection_check: test function returning True (if proxy is good) or False (proxy is bad)
        :return:
        """

        if (datetime.now() - self.last_change).total_seconds() > 60 * minutes_between_changes:
            # print((datetime.now() - self.last_change).total_seconds() > 60 * minutes_between_changes)

            with Controller.from_port(port=9051) as controller:
                controller.authenticate(self.tor_password)
                controller.signal(Signal.NEWNYM)
                controller.get_newnym_wait()

            if connection_check() and total_retries > 0:
                pass
            else:
                print('retrying due to connection_check returning False')
                self.get_new_proxy(minutes_between_changes, connection_check, total_retries=total_retries-1)

            self.last_change = datetime.now()
            print(self.last_change, self.what_is_my_ip())

    def what_is_my_ip(self):
        proxies = {
            'http': 'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050'
        }
        return requests.get('http://icanhazip.com/', proxies=proxies).text.strip()


def check_if_can_connect_to_google_translate():
    translator = Translator()
    try:
        response = [item.text for item in translator.translate(['apple'], dest='en')][0]
        if response == 'apple':
            return True
    except:
        return False

# proxy_changer = ProxyChanger(tor_password='123')
# proxy_changer.get_new_proxy(minutes_between_changes=5)
