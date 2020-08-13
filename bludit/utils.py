from bs4 import BeautifulSoup

import logging


def get_bludit_key(response):
    cookie = response.headers['Set-Cookie']
    bludit_key = None
    if not cookie:
        logging.error('Cannot find cookie')
    else:
        cookie_values = cookie.split(';')
        bludit_key = next((x for x in cookie_values if x.startswith('BLUDIT-KEY')), None)
    return bludit_key.split('=')[1]


def get_csrf_token(response):
    html = BeautifulSoup(response.text, 'html.parser')
    input_fields = html.find_all('input')
    token = next((x for x in input_fields if x.get('name', None) == 'tokenCSRF'), None)
    return token.get('value', None)
