import json
import os
import sys
import jsonschema as jsonschema
from jsonschema import validate
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from features.steps.globalVar import GlobalVar
from requests.auth import HTTPBasicAuth
from requests import HTTPError



class ApiTest:
    def __init__(self):
        pass

    def setEndpoint(self, baseUrl, endpoint):
        requestEndpoint = ''.join([baseUrl, endpoint])
        return requestEndpoint

    def setHeader(self, headerType, headerValue, requestHeaders={}):
        if headerType or headerValue is not None: requestHeaders[headerType] = headerValue
        return requestHeaders

    def setParams(self, fileName, component):
        if fileName is not None:
            filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + \
                       f'/resources/payload/{sys.argv[1]}/{component.lower()}/{fileName}'
            with open(filePath) as messageFile:
                requestParams = json.load(messageFile)
        else: requestParams = None
        return requestParams

    def setBody(self, fileName, component):
        if fileName is not None:
            filePath = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../..")) + \
                       f'/resources/payload/{sys.argv[1]}/{component.lower()}/{fileName}'
            with open(filePath) as messageFile:
                requestPayload = json.load(messageFile)
        else: requestPayload = None
        return requestPayload

    def sendRequestData(self, requestMethod, requestEndpoint, requestHeaders, requestParams, requestPayload):
        try:
            urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.request(method=requestMethod, url=requestEndpoint, headers=requestHeaders,
                                        params=requestParams, data=requestPayload, verify=False)
            return response
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def sendRequestjson(self, requestMethod, requestEndpoint, requestHeaders, requestParams, requestPayload):
        try:
            urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.request(method=requestMethod, url=requestEndpoint, headers=requestHeaders,
                                        params=requestParams, json=requestPayload, verify=False)

            return response
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def sendRequestAuth(self, requestMethod, requestEndpoint, requestPayload, authUser, authPassword):
        try:
            urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.request(method=requestMethod, url=requestEndpoint,  json=requestPayload,
                                        auth=HTTPBasicAuth(authUser, authPassword), verify=False)

            return response
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def sendRequest(self, requestMethod, requestEndpoint, requestParams, requestHeaders):
        try:
            urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.request(method=requestMethod, url=requestEndpoint, headers=requestHeaders,
                                        params=requestParams, verify=False)
            return response
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def validateResponseCode(self, response, expectedStatusCode):
        actualStatusCode = response.status_code
        if int(actualStatusCode) == int(expectedStatusCode): return True
        else: return False

    def validateResponseSchema(self, response, schemaFileName, component):
        if not type(response) is dict: response_json = response.json()
        else: response_json = response

        if schemaFileName is not None:
            filePath = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../..")) + f'/resources/schema/{sys.argv[1]}/{component.lower()}/{schemaFileName}'
            with open(filePath) as schemaFile:
                schema = json.load(schemaFile)
        try:
            validate(instance=response_json, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            print(err)
            return False

    def updateBodyParams(self, body, params):
        body["serviceCharacteristic"][0]["value"]["site"]["telus-pe-ce-network-accesses"]["site-network-access"][
            "telus-pe-device-reference"] = params.get("deviceName")
        body["serviceCharacteristic"][0]["value"]["site"]["telus-pe-devices"]["pe-device"][0][
            "pe-device-id"] = params.get("deviceName")
        body["serviceCharacteristic"][0]["value"]["site"]["telus-pe-devices"]["pe-device"][0][
            "vendor"] = params.get("deviceVendor")
        body["serviceCharacteristic"][0]["value"]["site"]["telus-pe-devices"]["pe-device"][0][
            "model"] = params.get("deviceModel")
        body["serviceCharacteristic"][0]["value"]["site"]["telus-pe-ce-network-accesses"]["site-network-access"][
            "bearer"]["telus-pe-tp-info"]["port"] = params.get("port").strip()
        body["serviceCharacteristic"][0]["value"]["site"]["telus-pe-ce-network-accesses"]["site-network-access"][
            "bearer"]["telus-pe-tp-info"]["vlan-id"] = int(params.get("vlanId"))
        body["serviceCharacteristic"][0]["value"]["site"]["telus-cust-service-id"] = params.get("serviceId")
        return body

    def readVlan(self, body):
        vlanId = body["serviceCharacteristic"][0]["value"]["site"]["telus-pe-ce-network-accesses"]["site-network-access"][
            "bearer"]["telus-pe-tp-info"]["vlan-id"]
        return vlanId

