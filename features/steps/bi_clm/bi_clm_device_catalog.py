import requests
import urllib3

from behave import *
from urllib3.exceptions import InsecureRequestWarning
from common.util.api_test import ApiTest
from features.steps.globalVar import GlobalVar
from common.util.payloadGenerator import *

"""Declared variables"""
response_json = None


@step("I read test data for Device catalog testcases")
def step_impl(context):
    try:
        testCase = context.scenario.name.split(':')[0]
        GlobalVar.testParams = context.csvReadAPI[int(testCase.split('_')[1]) - 1]
    except:
        raise Exception(f'There might be missing entries in the test data sheet')


@step('I set endpoint for "{param}" requests')
def step_impl(context, param):
    if param == "deviceCatalog":
        GlobalVar.requestType = GlobalVar.testParams.get('RequestType')
        endpoint = GlobalVar.testParams.get('EndPoint')

        GlobalVar.api_dict[f'{GlobalVar.requestType}_URL'] = ''.join([GlobalVar.api_url, endpoint])
        print(">>>>")
        print(GlobalVar.api_dict[f'{GlobalVar.requestType}_URL'])


@step('I set request body for "{param}" APIs')
def step_impl(context, param):
    if param == "deviceCatalog":
        filename = GlobalVar.testParams.get('RequestBody')
        GlobalVar.api_dict['payload'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0],
                                                                              filename)
        print(json.dumps(GlobalVar.api_dict['payload'], indent=4))


@step('I Set query parameters for Device catalog requests')
def set_query_params_device_catalog(context):
    queryParamsFile = GlobalVar.testParams.get('QueryParams')
    if not bool(queryParamsFile):
        GlobalVar.api_dict['request_params'] = None
    else:
        GlobalVar.api_dict['request_params'] = payloadGenerator.load_payload_message(context,
                                                                                     GlobalVar.testComponent[0],
                                                                                     queryParamsFile)
        print(">>>>>>>>")
        print(GlobalVar.api_dict['request_params'])


@step('I Send HTTP request for "{component}" APIs')
def step_impl(context, component):
    if component == "device-catalog":
        global response_json
        urllib3.disable_warnings(InsecureRequestWarning)

    try:
        response = requests.get(GlobalVar.api_dict[f'{GlobalVar.requestType}_URL'],
                                headers=GlobalVar.api_dict['request_header'],
                                params=GlobalVar.api_dict['request_params'], verify=False)
        GlobalVar.response_codes = response.status_code
        print(response.json())
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


@step('Ensure that the HTTP response code is "{status_code}"')
def step_impl(context, status_code):
    assert str(GlobalVar.response_codes) == str(status_code)
