import urllib3
import time
import json
import requests
import os
import sys
from json import JSONDecodeError
import logging

from features.steps.lcd.model.tinaa_auth_service import TinaaAuthService
from features.steps.lcd.tinaa_config import TinaaAuthServiceConfig
from features.steps.lcd.functional_rule_test_config import FunctionalRuleTestConfig


class MediationLayerSession:
    def __init__(self):
        self.verify = True
        self.headers = {}
        self.cookies = {}
        
    def get(self, url, headers={}):
        headers2 = {}
        headers2.update(self.headers)
        headers2.update(headers)
        
        response = requests.get(url, verify=self.verify, headers=headers2, cookies=self.cookies)
        self.cookies.update(response.cookies)
        
        return response
    
    def post(self, url, data=None, headers={}):
        headers2 = {}
        headers2.update(self.headers)
        headers2.update(headers)
        
        response = requests.post(url, data=data, verify=self.verify, headers=headers2, cookies=self.cookies)
        self.cookies.update(response.cookies)
        
        return response
    
class MediationLayerNSOContext:
    def __init__(self, config: FunctionalRuleTestConfig, auth_service: TinaaAuthService):
        self.config = config
        self.MEDIATION_HOST = config.FUNCTIONAL_TESTING_MEDIATION_HOSTNAME
        self.LOGIN_URL = self.MEDIATION_HOST + '/api/login/'
        self.NSO_REQUEST_URL = self.MEDIATION_HOST + '/api/nso_request'
        self.auth_service = auth_service

        self.current_session = None
        self.id = -1
        self.th = -1
        self.session_pair = None
        self.test_timeout = 290
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def open(self):
        self._initialize_session()
        self._login()
        self._start_trans()
        return self

    def close(self):
        self._close_trans()
        self._logout()
        self._destroy_session()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _logout(self):
        #TODO:
        pass

    def _destroy_session(self):
        #TODO:
        self.current_session = None
        pass

    def _initialize_session(self):
        self.current_session: MediationLayerSession = MediationLayerSession()
        if self.config.USE_CERTS:
            # self.current_session.cert = (self.config.MEDIATION_CLIENT_CERTIFICATE, self.config.MEDIATION_CLIENT_KEY)
            self.current_session.verify = self.config.MEDIATION_CA_CERTIFICATE
        else:
            self.current_session.verify = False
        self.current_session.headers.update({'Content-type': 'application/json', 'Connection':'close'})
        self.auth_service.connect()

    def _login(self):
        self.auth_service.update_headers(self.current_session)

        response = self.current_session.get(self.LOGIN_URL)
        logging.debug("Get " + self.LOGIN_URL)
        logging.debug("Response " + str(response))

        if not response.text.startswith("sessionid_"):
            raise ValueError("Mediation Layer Issue", response.text)

        self.session_pair = response.text

    def request_body(self, subpath, request):
        self.auth_service.update_headers(self.current_session)
        return self._request(self.id, self.th, subpath, request)

    def _start_trans(self):
        self.id = 1
        self.th = self._request_start_trans(self.id)

    def _close_trans(self):
        print("Closing Transaction...")
        body = {}
        body['session'] = self.session_pair
        body['path'] = 'run_action'
        body['request'] = {
            "jsonrpc":"2.0",
            "id": str(id),
            "method":"delete_trans",
            "params": {
                'th': self.th,
            }
        }

        response = self.current_session.post(self.NSO_REQUEST_URL, data=json.dumps(body, indent=4))
        response_dict = json.loads(response.text)

        if response_dict['result'] != {}:
            raise RuntimeError("Closing transaction issue " + json.dumps(response_dict, indent=4))

    def _request_start_trans(self, id) -> int:
        body = {}
        body['session'] = self.session_pair
        body['path'] = 'run_action'
        body['request'] = {"jsonrpc":"2.0", "id": str(id), "method":"new_trans"}

        logging.debug("request to = " + self.NSO_REQUEST_URL)
        logging.debug("body = " + json.dumps(body, indent=4))
        request = self.current_session.post(self.NSO_REQUEST_URL, data=json.dumps(body, indent=4))
        logging.debug("request.text = " + request.text)
        th = json.loads(request.text)['result']['th']
        return th

    def _request(self, id, th, subpath, request):
        body = {}
        body['session'] = self.session_pair
        body['path'] = subpath
        body['request'] = request

        request['jsonrpc'] = '2.0'
        if id:
            request['id'] = id
        request['params']['format'] = 'json'
        if self.th:
            request['params']['th'] = self.th

        tojson = json.dumps(body, indent=4)
        response = self.current_session.post(self.NSO_REQUEST_URL, data=tojson)


        if (response.status_code != 200) and (response.status_code != 201):
            raise ValueError(f"Unexpected value: {response.status_code} {response.text}")

        try:
            content = json.loads(response.text)
        except JSONDecodeError as e:
            print("Improperly formatted response:\n", response.text, file=sys.stderr)
            raise ValueError(f"Text not properly formatted as JSON\n")
        logging.debug("request = " + tojson)
        logging.debug("response = " + json.dumps(content, indent=4))
        if "error" in content:
            print("body = ", tojson, file=sys.stderr)
            raise ValueError(f"Unexpected error: {content['error']}")

        return content['result']


class NSOAction:
    def __init__(self, context: MediationLayerNSOContext):
        self.context = context

    def request(self, params):
        params['method'] = 'run_action'
        return self.context.request_body("run_action", params)

