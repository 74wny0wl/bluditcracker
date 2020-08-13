import itertools
import os
import logging


class BluditCredentialsFactory:

    def __init__(self):
        self.csrf_token = None

    def use_csrf_token(self, csrf_token):
        self.csrf_token = csrf_token

    def create_credentials(self, username, password):
        credentials = {'tokenCSRF': self.csrf_token, 'username': username, 'password': password, 'save': ''}
        return credentials


def __load_file_lines__(filename):
    lines = []
    if not os.path.isfile(filename):
        logging.getLogger().error('File path {} does not exist'.format(filename))
    else:
        with open(filename, 'r') as f:
            lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def load_usernames(filename):
    return __load_file_lines__(filename)


def load_passwords(filename):
    return __load_file_lines__(filename)


def build_credentials_wordlist(usernames, passwords):
    return list(itertools.product(usernames, passwords))
