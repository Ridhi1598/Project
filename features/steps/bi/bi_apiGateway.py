from behave import *
import difflib
import json
import time
import os
import sys
import ssl
import pysftp
import gzip
import shutil
from os.path import dirname, abspath
import jsonschema as jsonschema
import requests
import datetime
from behave import given, when, then, step
from jsonschema import validate
from requests import HTTPError
from features.steps.globalVar import GlobalVar
from features.steps.bi.bi_restApis import *
from features.steps.api_steps_general import *
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from features.steps.globalVar import GlobalVar
from features.steps.ui_steps_general import page_title_validation, change_currentPage
from selenium.webdriver.support.select import Select
from common.util.payloadGenerator import payloadGenerator
from features.steps.globalVar import GlobalVar
from features.steps.l3vpn.l3vpn_restAPIs import *

# declared variables
api_endpoints = {}
request_headers = {}
response_codes = {}
response_texts = {}
response_json = {}
request_bodies = {}
api_url = None
responseVar = None
payload = {}
access_token = None
body = {}
request_Id = {}
# end of declared variables


@step('I Set "{requestType}" api endpoint for "{endpoint}" for BI')
def set_endpoint_for_BI(context, requestType, endpoint):
    print(GlobalVar.api_url)
    print(endpoint)
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = GlobalVar.api_url + endpoint
    return GlobalVar.api_dict['api_endpoint_' + requestType + '_url']


@step('Send "{requestType}" HTTP request')
def send_HTTP_request(context, requestType):
    # sending get request and saving response as response object
    global response_texts, response, response_json
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    if requestType == 'POST':
        response = requests.post(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                 headers=GlobalVar.api_dict.get("request_header"),
                                 data=GlobalVar.api_dict.get("payload"),
                                 verify=False)

    if requestType == 'GET':
        response = requests.get(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                headers=GlobalVar.api_dict.get("request_header"),
                                params=GlobalVar.api_dict.get('request_params'),
                                verify=False)
    print(response.text)
    # extracting response status_code
    response_codes[requestType] = response.status_code
    GlobalVar.response_codes = response_codes
    if scenarioVal == 'Health API':
        response_texts[requestType] = response.text
        pass
    else:
        response_json[requestType] = response.json()


@step('I validate the response value for "{scenario}"')
def validate_response(context, scenario):
    if scenario == 'Health API':
        responseVal = (GlobalVar.testParams.get("Response Assertion-1")).split('"')
        assert responseVal[1] in response_texts['GET']


@step('I validate the response value for expected message')
def validate_error_message(context):
    for key in response_json:
        if key == 'POST':
            if scenarioVal == 'Routing service validation-1':
                value = response_json[key]['reason'][0]
                assert value in GlobalVar.testParams.get("Response Assertion-1")

            elif scenarioVal == 'Keycloack certificate validation':
                try:
                    value = response_json[key]['reason']
                    assert value in GlobalVar.testParams.get("Response Assertion-1")

                except:
                    value = response_json[key]['reason'][0]
                    assert value in GlobalVar.testParams.get("Response Assertion-2")

            else:
                value = response_json[key]['reason']
                assert value in GlobalVar.testParams.get("Response Assertion-1")


@step('I Set "{requestType}" api endpoint for "{endpoint}"')
def set_API_endpoint(context, requestType, endpoint):
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = GlobalVar.api_url + endpoint


@step('I Set query parameters for request')
def set_query_params(context):
    filepath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + \
               '/resources/payload/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() + '/queryParams_userId.json'
    GlobalVar.api_dict['request_params'] = json.load(open(filepath))


@step('I Set HEADER param request "{header}" for "{scenario}"')
def set_token_value(context, header, scenario):
    global request_headers
    auth = GlobalVar.testParams.get(header)
    if auth == 'Bearer Token':
        access_token = generate_access_token(context)
        request_headers[header] = 'Bearer ' + access_token
    else:
        request_headers[header] = auth
    GlobalVar.api_dict['request_header'] = request_headers


@step('I set data values against scenario "{scenario}"')
def set_params(context, scenario):
    global scenarioVal

    for index in range(0, 7):
        GlobalVar.testParams = context.csvReadAPI[index]
        scenarioVal = GlobalVar.testParams.get("Scenario")
        if scenarioVal == scenario:
            break


@step(u'Set request Body for "{endpoint}" API of BI')
def step_impl(context, endpoint):
    global payload
    GlobalVar.api_dict['payload'] = GlobalVar.testParams.get("Request Body")