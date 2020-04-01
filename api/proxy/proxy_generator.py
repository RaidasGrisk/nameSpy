
"""
# https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b
# https://stackoverflow.com/questions/48117693/python-stemrequests-not-switching-circut-changing-ip-address-when-using-a-sess

The password and ControlPort must be set inside /etc/tor/torrc. Here's an excerpt form dockerfile
RUN echo HashedControlPassword $(tor --hash-password "kjhadfjkasf12a32sf456" | tail -n 1) >> /etc/tor/torrc
RUN echo "ControlPort 9051" >> /etc/tor/torrc

"""


from stem import Signal
from stem.control import Controller
import requests
from datetime import datetime


class ProxyChanger:
    def __init__(self, tor_password):
        self.last_change = datetime.now()
        self.tor_password = tor_password
        self.get_new_proxy(minutes_between_changes=0)

    def get_new_proxy(self, minutes_between_changes):

        if (datetime.now() - self.last_change).total_seconds() > 60 * minutes_between_changes:
            # print((datetime.now() - self.last_change).total_seconds() > 60 * minutes_between_changes)

            with Controller.from_port(port=9051) as controller:
                controller.authenticate(self.tor_password)
                controller.signal(Signal.NEWNYM)
                controller.get_newnym_wait()

            self.last_change = datetime.now()
            print(self.last_change, self.what_is_my_ip())

    def what_is_my_ip(self):
        proxies = {
            'http': 'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050'
        }
        return requests.get('http://icanhazip.com/', proxies=proxies).text.strip()


# proxy_changer = ProxyChanger(tor_password='123')
# proxy_changer.get_new_proxy(minutes_between_changes=5)
