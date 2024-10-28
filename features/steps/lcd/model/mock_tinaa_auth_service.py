import time
import json
import requests
import os

class MockTinaaAuthService:
    MAX_CONNECTION_TIME=10
    TINAA_ACCESS_TOKEN = 'tinaa-access-token'

    def __init__(self, auth_config):
        pass     
    
    def connect(self):
        pass

    def update_headers(self, session: requests.Session):
        self.renew_if_needed()
        session.headers[self.TINAA_ACCESS_TOKEN] = "fake-access-token"

    def renew_if_needed(self):
        pass

