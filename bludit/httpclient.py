from http import HTTPStatus
import requests
import validators
from validators import ValidationFailure

from bludit.utils import get_bludit_key, get_csrf_token

import logging


class IPAddressBlockedError(Exception):
    pass


class BluditHttpClient:

    def __init__(self, bludit_credentials_factory):
        self.bludit_credentials_factory = bludit_credentials_factory
        self.admin_panel_url = None
        self.is_connected = False
        self.csrf_token = None
        self.cookies = None

    def connect(self, admin_panel_url):
        self.admin_panel_url = admin_panel_url
        self.reconnect()

    def reconnect(self):
        if not self.is_admin_panel_url_valid():
            return
        self.is_connected = False
        response = requests.get(self.admin_panel_url)
        if response.status_code == HTTPStatus.OK:
            bludit_key = get_bludit_key(response)
            self.csrf_token = get_csrf_token(response)

            self.cookies = {'BLUDIT-KEY': bludit_key}

            self.bludit_credentials_factory.use_csrf_token(self.csrf_token)

            self.is_connected = True
        return self.is_connected

    def is_admin_panel_url_valid(self):
        is_valid = True
        try:
            validators.url(self.admin_panel_url)
        except ValidationFailure:
            is_valid = False
            logging.getLogger().error("Admin panel URL is not valid")
        return is_valid

    def try_authenticate(self, username, password):
        credentials = self.bludit_credentials_factory.create_credentials(username, password)
        authenticate_response = requests.post(self.admin_panel_url, cookies=self.cookies, data=credentials)
        if 'IP address has been blocked' in authenticate_response.text:
            raise IPAddressBlockedError
        return 'HTML_PATH_ADMIN_ROOT' in authenticate_response.text
