import time
import json
import requests
import os
import logging

from features.steps.lcd.tinaa_config import TinaaAuthServiceConfig


class TinaaAuthService:
    MAX_CONNECTION_TIME = 10
    TINAA_ACCESS_TOKEN = 'tinaa-access-token'

    def __init__(self, auth_config: TinaaAuthServiceConfig):
        self.auth_config = auth_config
        self.auth_info = {}

        self.config_ssl()

    def config_ssl(self):
        self.cert = None
        self.verify = False
        if self.auth_config.USE_CERTS:
            # self.verify = self.auth_config.CERTS_PATH + '/nso_laird.pem'
            # self.cert = self.auth_config.CERTS_PATH + '/Laird-public-key.txt'
            # self.cert = self.auth_config.CERTS_PATH + '/client_certificate.pem' #, self.auth_config.CERTS_PATH + '/client_key.pem')
            self.verify = self.auth_config.CERTS_PATH + '/ca_certificate.pem'

    def connect(self):
        data = {
            'client_id': self.auth_config.CLIENT_ID,
            'client_secret': self.auth_config.CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }
        url = self.auth_config.GENERATOR_URL
        headers = { "Content-Type": "application/x-www-form-urlencoded", 'Connection':'close' }

        response = requests.request('POST', url, data=data, cert=self.cert, verify=self.verify, headers=headers)

        if response.status_code != 200:
            raise ValueError(f"Tinaa Authentication failed {response.status_code} {response.text}")

        self.response_dict = json.loads(response.text)
        self.auth_info = self.response_dict
        self.auth_info['lastrenewed'] = time.time()

        # self.access_token = response_dict['access_token']
        # self.expires_in = response_dict['expires_in'],
        # self.refresh_expires_in = response_dict['refresh_expires_in']
        # self.refresh_token = response_dict['refersh_token']

    def update_headers(self, session: requests.Session):
        self.renew_if_needed()
        session.headers[self.TINAA_ACCESS_TOKEN] = self.auth_info['access_token']

    def renew_if_needed(self):
        now = time.time()
        expires_in = int(self.auth_info['expires_in'])
        time_since_renewal = now - int(self.auth_info['lastrenewed'])

        logging.debug("Checking if a reauthentication is needed...")
        if  time_since_renewal < expires_in - self.auth_config.GUARDING_TIME:
            logging.debug("No need for reauthentication")
            return

        if time_since_renewal < int(self.response_dict['refresh_expires_in']) - self.MAX_CONNECTION_TIME:
            #TODO: Current TINAA OAuth documentation doesn't include renewal
            logging.debug("Would have refreshed if Tinaa supported refresh")
            logging.debug("Time since renewal", time_since_renewal)
            logging.debug("Refresh Expires in", self.response_dict['refresh_expires_in'])
            logging.debug("Max connection time", self.MAX_CONNECTION_TIME)
            pass

        
        if time_since_renewal < int(self.response_dict['expires_in']) - self.MAX_CONNECTION_TIME:
            logging.info("Reauthenticating because we're close to expiry...")
            logging.debug("Expires in", (int(self.response_dict['expires_in'])-time_since_renewal))
            self.connect()
            return

        logging.info("Reauthenticating...")
        # If all fail, reconnect
        self.connect()

    def _renew(self):
        raise NotImplementedError()

