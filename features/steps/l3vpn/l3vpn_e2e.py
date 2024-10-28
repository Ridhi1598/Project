import json
import time
import os
import sys
import ssl

from netmiko import ConnectHandler
from os.path import dirname, abspath
import jsonschema as jsonschema
import requests
import re

import yaml
from behave import given, when, then, step
from jsonschema import validate
from netmiko import ConnectHandler
from requests import HTTPError

from common.util.baseReader import BaseReader
from common.util.config import ConfigReader
from common.util.payload_config_reader import PayloadConfigReader
from features.steps.globalVar import GlobalVar
from features.steps.bi.bi_restApis import *
from features.steps.api_steps_general import *
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from features.steps.globalVar import GlobalVar
from features.steps.l3vpn.regex_utils import RegexUtils
from features.steps.ui_steps_general import page_title_validation, change_currentPage
from selenium.webdriver.support.select import Select
from common.util.payloadGenerator import payloadGenerator
from features.steps.bi.bi_uiFunctional import *
from netmiko import ConnectHandler
import yaml
import logging as logger
from pathlib import Path


# declared variables
from features.steps.globalVar import GlobalVar

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
testParams = {}
executedTestCases = []
request_Id = {}
index = None
testCaseData = {}
loginStatus = None
requestState = None
device_handler = None
url = None
matches = None
count = 0
previous_config = None
counter = 5
conn = None
flag = False


@step('I generate access token for L3VPN')
def generate_access_token(context):
    global body
    global access_token
    set_endpoint(context)
    set_header_request(context, 'Content-Type', 'application/x-www-form-urlencoded')
    filepath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + \
               '/resources/payload/l3vpn/v1_service/accessToken.json'
    GlobalVar.api_dict['request_bodies'] = json.load(open(filepath))
    responseCode = post_request_authorization_l3vpn(context, GlobalVar.api_dict['request_bodies'])
    validate_response_code_l3vpn(context, int(responseCode), context.config.get('authorizationAPIResponse'))
    access_token = get_access_token_l3vpn(context)
    GlobalVar.access_token = access_token
    return access_token


@step('I read service id for test case sequence for L3VPN')
def read_service_id(context):
    global serviceId
    featureName = str(context.feature)
    featureNameList = featureName.split('"')
    featureTest = featureNameList[1].split(' ')
    GlobalVar.baseTest = featureTest[0].split('_')[1]
    serviceId = context.csvRead[int(GlobalVar.baseTest) - 1].get('telus-cust-service-id')
    GlobalVar.testParams['serviceId'] = serviceId

@step('Set request Body for L3VPN')
def set_request_body(context):
    global rootPath
    global requestType
    requestType = testParams.get('Request-Type')
    if requestType == 'DELETE':
        pass
    elif requestType == 'POST' or 'PUT':
        filename = testParams.get('Payload')
        if filename != 'None':
            payloadFile = context.csvRead[index].get('Payload')
            context.baseReader = PayloadConfigReader(payloadFile)

            payloadName = GlobalVar.testParams['payloadName']

            payload = context.baseReader.getValueByName("Payload", payloadName).get("value")
            GlobalVar.api_dict['payload'] = payload
        else:
            GlobalVar.api_dict['payload'] = None


@step('I set api endpoint for testcase "{testCase}" for l3vpn')
def set_API_endpoint(context, testCase):
    global testParams
    global index
    global testcase
    global api_endpoints

    index = int(testCase) - 1

    testParams = context.csvRead[index]
    GlobalVar.testParams = testParams

    serviceId = testParams.get('telus-cust-service-id')
    testcase = testParams.get('Testcase')

    requestType = testParams.get('Request-Type')
    endpoint = testParams.get('Endpoint')

    api_url = GlobalVar.api_url

    if endpoint == '/l3vpn/svc/v1/service' and sys.argv[2] == "dev":
        api_endpoints[requestType + '_URL'] = api_url + endpoint + "?user_id=x231081"

    if endpoint == '/l3vpn/svc/v1/service' and sys.argv[2] == "preprod":
        api_endpoints[requestType + '_URL'] = api_url + endpoint

    if endpoint == '/l3vpn/svc/v1/service/{service_id}' and sys.argv[2] == "dev":
        api_endpoints[requestType + '_URL'] = GlobalVar.api_url + endpoint.replace('{service_id}', serviceId) + "?user_id=x231081"

    if endpoint == '/l3vpn/svc/v1/service/{service_id}' and sys.argv[2] == "preprod":
        api_endpoints[requestType + '_URL'] = GlobalVar.api_url + endpoint.replace('{service_id}', serviceId)

    if endpoint == '/l3vpn/svc/v1/site' and sys.argv[2] == "dev":
        api_endpoints[requestType + '_URL'] = GlobalVar.api_url + endpoint.replace('{service_id}', serviceId) + "?user_id=x231081"

    if endpoint == '/l3vpn/svc/v1/service/{service_id}/site' and sys.argv[2] == "preprod":
        api_endpoints[requestType + '_URL'] = GlobalVar.api_url + endpoint.replace('{service_id}', serviceId)

    # print('api_endpoint_' + requestType + '_url')
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = api_endpoints[requestType + '_URL']
    print("Endpoint: ", GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])


@step('Send Http request for L3VPN')
def send_Http_request(context):
    global serviceState
    global request_Id
    global testScenario

    response = None
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        if requestType == 'POST':
            print("Sending POST request:-")
            response = requests.post(
                url=GlobalVar.api_dict.get("api_endpoint_" + testParams['Request-Type'] + "_url"),
                headers=GlobalVar.api_dict.get("request_header"),
                json=GlobalVar.api_dict.get("payload"),
                verify=False)

        if requestType == 'PUT':
            print("Sending PUT request:-")
            response = requests.put(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                    headers=GlobalVar.api_dict.get("request_header"),
                                    json=GlobalVar.api_dict.get("payload"),
                                    verify=False)

        if requestType == 'DELETE':
            print(GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"))
            print(GlobalVar.api_dict.get("request_header"))
            response = requests.delete(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                       headers=GlobalVar.api_dict.get("request_header"),
                                       verify=False)

        if requestType == 'GET':
            response = requests.get(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                    headers=GlobalVar.api_dict.get("request_header"),
                                    params=GlobalVar.api_dict['request_params'],
                                    verify=False)

        print("Request response text: {}".format(response.text))
        response_codes[requestType] = response.status_code
        response_json[requestType] = response.json()

        responseCodeVar = 'l3vpn_' + requestType + '_Response'
        validate_response_code(context, int(response_codes[requestType]), context.config.get(responseCodeVar))

        # extract request id for asynchronous response tracking
        request_Id = {baseTest: {testcase: response_json[requestType]['requestId']}}
        print("Request Id for testcase-{} : {}".format(testcase, request_Id[baseTest][testcase]))
        # request_Id['rollback'] = request_Id[baseTest][testcase]

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step(u'Send POST HTTP request for authorization for l3vpn')
def post_request_authorization_l3vpn(context, body):
    global access_token
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=GlobalVar.api_dict.get("api_endpoint_post_url"), data=body, verify=False)
        response_texts['POST'] = response.text
        statuscode = response.status_code
        response_codes['POST'] = statuscode
        response_json['POST'] = response.json()
        return response_codes['POST']

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I receive valid HTTP response code "{actual_response_code}" as "{expected_response_code}" for l3vpn')
def validate_response_code_l3vpn(context, actual_response_code, expected_response_code):
    time.sleep(3)
    assert actual_response_code == expected_response_code


@step('I extract response value of access_token for l3vpn')
def get_access_token_l3vpn(context):
    global access_token
    for key in response_json:
        if key == 'POST':
            for key_nested in response_json[key]:
                if key_nested == 'access_token':
                    access_token = response_json[key][key_nested]
                    return access_token
        else:
            print("Access Token Not Found")


@step('I validate the IE response as "{expectedValue}"')
def validate_IE_response(context, expectedValue):
    global requestState
    if request_Id[baseTest][testcase] is not None:
        waitTime = testParams.get('wait_time')
        print("Waiting for " + waitTime + " seconds...")
        time.sleep(int(waitTime))

        generate_access_token(context)

        url_monitor = 'monitorAPIURL_' + sys.argv[2]
        url = context.config.get(url_monitor) + request_Id[baseTest][testcase]

        print("Monitor API URL: ", url)
        set_header_request(context, 'Authorization', access_token)

        try:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(url=url, headers=GlobalVar.api_dict.get("request_header"), verify=False)
            response_codes['GET'] = response.status_code
            response_json['GET'] = response.json()
            validate_response_code(context, int(response_codes['GET']),
                                   context.config.get('monitorAPIResponse'))
            requestState = response_json['GET']['state']
            print('L3VPN Service Request State: ', requestState)

            if requestState == 'submitted':
                validate_IE_response(context, expectedValue)

            elif requestState == 'failed' or requestState == 'timeout':
                context.scenario.skip(reason='Reason: Service is failed or timeout')
                GlobalVar.scenarioStatus = "skipped"
            else:
                assert requestState == expectedValue

        except HTTPError as http_err:
            print(f'Failing test case at request completion: {str(testcase)}')
            print(f'HTTP error occurred: {http_err}')

        except Exception as err:
            print("Other error occured:", err)

    else:
        print("Request does not exist")

@step('I create SSH connection to the device "{user}"')
def create_SSH(context, user):
    global device_handler
    global counter
    global conn
    deviceType = testParams.get('Device-Type')
    connInfo = ConfigReader().configFileReader("SSH_Credentials_device_"+deviceType+".json")
    try:
        conn = ConnectHandler(**connInfo)
        prompt = conn.find_prompt()
        logger.info(f"SSH-Connection is successful. Prompt: {prompt}")
        conn.enable()
        print("Entered in enable mode!!")
        counter = 5
    except BaseException as ex:
        if counter >= 1:
            counter = counter - 1
            print("Create SSH-Connection attempted!!!")
            time.sleep(10)
            create_SSH(context, user)
        else:
            logger.error(ex)
            raise ex
    GlobalVar.sshInfo['Device_Handler'] = conn
    return conn


@step('I run "{value}" command and store the device config')
def run_command(context, value):
    device_handler = GlobalVar.sshInfo['Device_Handler']
    current_config = device_handler.send_command(value)
    GlobalVar.sshInfo['device_config'] = current_config
    # print("Command output : ")
    # print(current_config)


@step('I close the SSH connection')
def close_SSH_connection(context):
    device_handler = GlobalVar.sshInfo['Device_Handler']
    device_handler.exit_enable_mode()
    device_handler.disconnect()
    print("Device disconnected..")
    return True


@step('I query the content of section "{header}" at level "{level}"')
def query_content(context, header, level):
    global count
    global previous_config
    if count == 0:
        GlobalVar.current_config['base_config'] = GlobalVar.sshInfo['device_config']
        try:
            GlobalVar.vrf_section_content['header'], GlobalVar.vrf_section_content['body'], GlobalVar.vrf_section_content['footer'] =\
                RegexUtils.retrieve_section(GlobalVar.current_config['base_config'], header, level)
            GlobalVar.current_config[header] = GlobalVar.vrf_section_content['body']
            previous_config = header
            count=+1
        except:
            print(f"Could not retrive section starting with \"{header}\" at level {level}")
            print("data = ")
            raise

    elif count > 0:
        try:
            GlobalVar.vrf_section_content['header'], GlobalVar.vrf_section_content['body'], GlobalVar.vrf_section_content['footer'] =\
                RegexUtils.retrieve_section(GlobalVar.current_config[previous_config], header, level)

            GlobalVar.current_config[header] = GlobalVar.vrf_section_content['body']
            previous_config = header
        except:
            print(f"Could not retrive section starting with \"{header}\" at level {level}")
            print("data = ")
            raise


@step('I query the content of section "{header}" at "{level}" level')
def query_content(context, header, level):
    global previous_config
    GlobalVar.current_config['base_config'] = GlobalVar.sshInfo['device_config']
    try:
        GlobalVar.vrf_section_content['header'], GlobalVar.vrf_section_content['body'], GlobalVar.vrf_section_content['footer'] =\
            RegexUtils.retrieve_section(GlobalVar.current_config['base_config'], header, level)
        # print("#################QUERY OUTPUT- START ############")
        # print(GlobalVar.vrf_section_content['body'])
        # print("#################QUERY OUTPUT - END #############")
    except:
        print(f"Could not retrive section starting with \"{header}\" at level {level}")
        print("data = ")
        raise


@step('I search for the pattern “{patternVal}”')
def search_pattern_val(context, patternVal):
    pattern = RegexUtils.findall_groupings(GlobalVar.vrf_section_content['body'], patternVal)
    GlobalVar.regex_pattern = pattern


@step('I validate the searched pattern “{output}”')
def device_config_output_assertion(context, output):
    expectedPattern = list(output)
    assert expectedPattern == GlobalVar.regex_pattern


@step('I validate the output of "{sectionType}" section')
def validate_query_section(context, sectionType):
    global matches
    # In this step, We are fetching the device assertions from YML file on the basis of parameters
    targetOutput = context.baseReader.getValueByName("Assertions", sectionType).get("value")

    elements = targetOutput.strip().split("\n")
    pattern_str = "(?:(.|\n)*)".join(map(
        lambda element: "^ *(" + re.escape(element) + ") *$",elements))
    pattern = re.compile("((?:.|\n)*)" + pattern_str + "((?:.|\n)*)", re.MULTILINE)

    if sectionType == "router_ospf" or sectionType == "router_ospfv3":
        data = GlobalVar.sshInfo['device_config']
        matches = re.findall(pattern, data)
    else:
        data = GlobalVar.vrf_section_content['body']
        #In this step, We are fetching actual configuration from device
        matches = re.findall(pattern, data)
    try:
        assert len(matches) >= 1
        print("Successfully Matched!!")
    except Exception as e:
        print("Expected Output to be matched:\n" + targetOutput)
        raise e

@step('I validate the output of "{sectionType}" section at "{level}"')
def validate_output_section_different_level(context, sectionType, level):
    global matches
    targetOutput = context.baseReader.getValueByName("Assertions", sectionType).get("value")
    elements = targetOutput.strip().split("\n")
    pattern_str = "(?:(.|\n)*)".join(map(
        lambda element: "^ *(" + re.escape(element) + ") *$",elements))
    pattern = re.compile("((?:.|\n)*)" + pattern_str + "((?:.|\n)*)", re.MULTILINE)

    if level == "default-level":
        data = GlobalVar.sshInfo['device_config']
        matches = re.findall(pattern, data)
    else:
        data = GlobalVar.vrf_section_content['body']
        #In this step, We are fetching actual configuration from device
        matches = re.findall(pattern, data)
    try:
        assert len(matches) >= 1
        print("Successfully Matched!!")
    except Exception as e:
        print("Expected Output to be matched:\n" + targetOutput)
        raise e


@step('I validate the show running config output by query "{sectionType}"')
def validate_query_section(context, sectionType):
    global matches
    targetOutput = context.baseReader.getValueByName("Assertions", sectionType).get("value")

    elements = targetOutput.strip().split("\n")
    pattern_str = "(?:(.|\n)*)".join(map(
        lambda element: "^ *(" + re.escape(element) + ") *$",elements))
    pattern = re.compile("((?:.|\n)*)" + pattern_str + "((?:.|\n)*)", re.MULTILINE)
    data = GlobalVar.sshInfo['device_config']
    matches = re.findall(pattern, data)
    try:
        assert len(matches) >= 1
        print("Successfully Matched!!")
    except Exception as e:
        print("Expected Output to be matched:\n"+ targetOutput)
        raise e


@step('I validate the value of "{value}" section')
def encapsulation_value(context, value):
    global flag
    if value == "description_bgp_desc":
        desc = context.baseReader.getValueByName("Assertions", value).get("value")
        data = GlobalVar.vrf_section_content['body']
        if desc in data:
            print("Successfully matched--")
            flag = True
        else:
            print("Expected Output to be matched:" + desc)
            assert flag == True

    else:
        full_en_value = context.baseReader.getValueByName("Assertions", value).get("value")
        full_en_value = full_en_value.strip()
        targetOutput = "," + full_en_value.split(value + " ")[1]
        targetOutput = targetOutput.strip()
        data = GlobalVar.vrf_section_content['body']

        for line in data.splitlines():
            if (line.strip()).__contains__(value):
                # print(full_en_value in line)
                # print(targetOutput+"," in line)
                # print(targetOutput in line)
                if full_en_value in line or targetOutput + "," in line or targetOutput in line:
                    print("Successfully matched--")
                    flag = True
                    break
                else:
                    print("Expected Output to be matched:" + targetOutput)
        assert flag == True