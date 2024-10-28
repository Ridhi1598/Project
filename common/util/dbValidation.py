import sys
import requests
import json
import os
import jsonschema as jsonschema
from jsonschema import validate
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from requests import HTTPError


class ES:
    def __init__(self, method, baseUrl, endpoint, payloadFileName, component):
        self.response = None
        self.component = component

        # set endpoint
        self.requestEndpoint = ''.join([baseUrl, endpoint])

        # set payload
        if payloadFileName is not None:
            self.filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + \
                            f'/resources/payload/{sys.argv[1]}/{component.lower()}/{payloadFileName}'
            with open(self.filePath) as messageFile:
                self.requestPayload = json.load(messageFile)

            if method.upper() == "POST":
                pass

        else:
            self.requestPayload = None

        # set header
        self.headers = {
            'Authorization': 'Basic ZWxhc3RpYzplbGFzdGlj',
            'Content-Type': 'application/json'
        }

    def send_db_req(self, requestMethod):
        try:
            urllib3.disable_warnings(InsecureRequestWarning)
            self.response = requests.request(method=requestMethod, url=self.requestEndpoint, json=self.requestPayload,
                                             headers=self.headers, verify=False)

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def validate_response_code(self, expectedStatusCode):
        actualStatusCode = self.response.status_code
        if int(actualStatusCode) == int(expectedStatusCode):
            return True

    def validate_response_schema(self, schemaFileName):
        if not type(self.response) is dict:
            response_json = self.response.json()
        else:
            response_json = self.response

        if schemaFileName is not None:
            filePath = os.path.abspath(
                os.path.join(os.path.dirname(__file__),
                             "../..")) + f'/resources/schema/{sys.argv[1]}/{self.component.lower()}/{schemaFileName}'
            with open(filePath) as schemaFile:
                schema = json.load(schemaFile)
        try:
            validate(instance=response_json, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            print(err)
            return False
