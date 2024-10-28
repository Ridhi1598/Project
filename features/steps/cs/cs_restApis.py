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

from features.steps.bi.bi_apiGateway import set_endpoint_for_BI
from features.steps.globalVar import GlobalVar
from features.steps.bi.bi_uiFunctional import *
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
from common.util.fileCompare import FileCompare
from common.util.stc import STC

# declared variables

# end of declared variables


@step('I send request to create new session')
def create_Session(context):
    server = GlobalVar.testParams.get('server')
    port = GlobalVar.testParams.get('port')
    userName = GlobalVar.testParams.get('userName')
    sessionName = GlobalVar.testParams.get('sessionName')
    STC.create_session(context, server, port, userName, sessionName)


@step('I send request to create "{projectCommand}" and "{portCommand}"')
def create_project(context, projectCommand, portCommand):
    chassis_ip = GlobalVar.testParams.get('chassis_ip')
    chassis_port = GlobalVar.testParams.get('chassis_port')
    GlobalVar.testParams['project'], GlobalVar.testParams['portHandle'] = STC.create_project(context, projectCommand,
                                                                    portCommand, chassis_ip, chassis_port)
    print(GlobalVar.testParams['project'], GlobalVar.testParams['portHandle'])


@step('I send request to create device list under created project using "{deviceListCommand}" command')
def create_deviceList(context, deviceListCommand):
    DeviceCount = GlobalVar.testParams.get("DeviceCount")
    GlobalVar.testParams['deviceList'] = STC.create_deviceList(context, deviceListCommand,
                                         GlobalVar.testParams['project'], GlobalVar.testParams['portHandle'],
                                         int(DeviceCount))
    print(GlobalVar.testParams['deviceList'])


@step('I send request to create "{EthIIIfCommand}", "{VlanIfCommand}" and "{Ipv4IfCommand}" under created device list')
def create_deviceList(context, EthIIIfCommand, VlanIfCommand, Ipv4IfCommand):
    GlobalVar.testParams['EthIIIf'] = STC.create_deviceEthIIIf(context, EthIIIfCommand,
                                                               GlobalVar.testParams['deviceList'])
    GlobalVar.testParams['VlanIf'] = STC.create_deviceVlanIf(context, VlanIfCommand, GlobalVar.testParams['deviceList'],
                                                             GlobalVar.testParams['EthIIIf'])
    GlobalVar.testParams['Ipv4If'] = STC.create_deviceIpv4If(context, Ipv4IfCommand, GlobalVar.testParams['deviceList'],
                                                             GlobalVar.testParams['VlanIf'])


@step('I send request to configure the created device list')
def configure_device(context):
    STC.configure_device(context, GlobalVar.testParams['deviceList'], GlobalVar.testParams['Ipv4If'])


@step('I create dhcp block using "{dhcpBlockCommand}" command')
def create_dhcpBlock(context, dhcpBlockCommand):
    CircuitId = GlobalVar.testParams.get("CircuitId")
    EnableCircuitId = GlobalVar.testParams.get("EnableCircuitId")
    EnableRelayAgent = GlobalVar.testParams.get("EnableRelayAgent")
    GlobalVar.testParams['dhcpBlock'] = STC.create_dhcp_block(context, dhcpBlockCommand, GlobalVar.testParams['deviceList'],
                                                              CircuitId, EnableCircuitId, EnableRelayAgent,
                                                              GlobalVar.testParams['Ipv4If'])


@step('I run dhcp results using "{dhcpResultCommand}" command')
def run_dhcpResults(context, dhcpResultCommand):
    projectName = GlobalVar.testParams['project']
    portHandle = GlobalVar.testParams['portHandle']
    resultType = GlobalVar.testParams.get("resultType")
    configType = GlobalVar.testParams.get("configType")
    ViewAttributeList = GlobalVar.testParams.get("ViewAttributeList")
    interval = int(GlobalVar.testParams.get("interval"))
    GlobalVar.testParams['dhcpResults'] = STC.run_dhcp_results(context, dhcpResultCommand, projectName, portHandle,
                                                               resultType, configType, ViewAttributeList, interval)


@step('I create sequencer using "{sequencerCommand}" command')
def create_sequencer(context, sequencerCommand):
    systemValue = GlobalVar.testParams.get("systemValue")
    GlobalVar.testParams['sequencer'] = STC.create_sequencer(context, sequencerCommand, systemValue)


@step('I create bind using "{bindCommand}" and "{bindWaitCommand}" commands')
def create_bind(context, bindCommand, bindWaitCommand):
    waitTime = int(GlobalVar.testParams.get("bindWaitTime"))
    GlobalVar.testParams['bind'], GlobalVar.testParams['bindWait'] = STC.create_bind(context, bindCommand, bindWaitCommand,
                                                    GlobalVar.testParams['sequencer'], GlobalVar.testParams['dhcpBlock'],
                                                    GlobalVar.testParams['deviceList'], waitTime)


@step('I create release using "{releaseCommand}" and "{releaseWaitCommand}" commands')
def create_bind(context, releaseCommand, releaseWaitCommand):
    waitTime = int(GlobalVar.testParams.get("releaseWaitTime"))
    GlobalVar.testParams['release'], GlobalVar.testParams['releaseWait'] = STC.create_release(context, releaseCommand, releaseWaitCommand,
                                                    GlobalVar.testParams['sequencer'], GlobalVar.testParams['dhcpBlock'],
                                                    GlobalVar.testParams['deviceList'], waitTime)


@step('I configure sequencer using "{sequencerInsertCommand}" command')
def configure_sequencer(context, sequencerInsertCommand):
    STC.configure_sequencer(context, sequencerInsertCommand, GlobalVar.testParams['bind'],
                            GlobalVar.testParams['bindWait'], GlobalVar.testParams['release'],
                            GlobalVar.testParams['releaseWait'])


@step('I apply configs using "{reservePortCommand}", "{portMappingsCommand}" and "{attachPortsCommand}" commands')
def apply_configs(context, reservePortCommand, portMappingsCommand, attachPortsCommand):
    chassis_ip = GlobalVar.testParams.get('chassis_ip')
    chassis_port = GlobalVar.testParams.get('chassis_port')
    portHandle = GlobalVar.testParams['portHandle']
    autoConnectValue = GlobalVar.testParams.get('autoConnectValue')
    STC.apply_configs(context, chassis_ip, chassis_port, reservePortCommand, portMappingsCommand, attachPortsCommand,
                  portHandle, autoConnectValue, GlobalVar.testParams['sequencer'])


@step('I start sequencer using "{sequencerStartCommand}" command')
def start_sequencer(context, sequencerStartCommand):
    resultHandle = GlobalVar.testParams.get('resultHandle')
    resultHandleArgs = GlobalVar.testParams.get('resultHandleArgs')
    bindRateHandleArgs = GlobalVar.testParams.get('bindRateHandleArgs')
    STC.start_sequencer(context, sequencerStartCommand, GlobalVar.testParams['dhcpResults'], resultHandle,
                        resultHandleArgs, bindRateHandleArgs, GlobalVar.testParams['sequencer'])


@step('I close and disconnect session')
def close_session(context):
    STC.close_session(context, GlobalVar.testParams.get('chassis_ip'), GlobalVar.testParams['deviceList'],
                      GlobalVar.testParams['portHandle'], GlobalVar.testParams['project'])

@step('I set CS "{apiType}" url')
def set_API_type(context, apiType):
    url = None
    if apiType == 'REST':
        url = '{}APIURL_{}'.format(sys.argv[1], sys.argv[2])
    elif apiType == 'controller':
        url = '{}ControllerURL_{}'.format(sys.argv[1], sys.argv[2])
    elif apiType == 'RMQ':
        url = '{}_RMQ_{}'.format(sys.argv[1], sys.argv[2])
    elif apiType == 'ES':
        url = 'ES_{}'.format(sys.argv[2])
    GlobalVar.api_url = context.config.get(url)
    return GlobalVar.api_url

@step("I set the Dev RMQ URL")
def step_impl(context):
    url = 'RMQ_{}'.format("dev")
    GlobalVar.api_url = context.config.get(url)
    return GlobalVar.api_url

@step('I Set Consumer POST request Body "{data_file}" for decommission')
def set_body(context, data_file):
    payload = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], data_file)
    requestId=payloadGenerator.generate_reqId(context)
    print("requestId: "+ requestId)
    GlobalVar.reqId = requestId
    payload['payload'] = payload['payload'].replace('request-idValue', requestId)
    GlobalVar.api_dict['payload'] = payload

@step('I Set Consumer POST "{data_file}" request Body to publish the message')
def set_publish_message_body(context, data_file):
    payload = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], data_file)
    requestId = payloadGenerator.generate_reqId(context)
    print("requestId: " + requestId)
    GlobalVar.reqId = requestId
    payload['payload'] = payload['payload'].replace('request-idValue', requestId)
    if  ("node1" in payload['payload']):
        payload['payload'] = payload['payload'].replace('node1', GlobalVar.consumerValidNode1)
    if "node2" in payload['payload']:
        payload['payload'] = payload['payload'].replace('node2', GlobalVar.consumerValidNode2)
    if "Invalid1node" in payload['payload']:
        payload['payload'] = payload['payload'].replace('Invalid1node', GlobalVar.consumerInvalidNode1)
    if "Invalid2node" in payload['payload']:
        payload['payload'] = payload['payload'].replace('Invalid2node', GlobalVar.consumerInvalidNode2)
    if  ("termination1" in payload['payload']):
        payload['payload'] = payload['payload'].replace('termination1', GlobalVar.consumerTerminationPoint1)
    if  ("termination2" in payload['payload']):
        payload['payload'] = payload['payload'].replace('termination2', GlobalVar.consumerTerminationPoint2)
    if  ("Invalid1Termination" in payload['payload']):
        payload['payload'] = payload['payload'].replace('Invalid1Termination', GlobalVar.consumerInvalidTerminationPoint1)
    if  ("Invalid2Termination" in payload['payload']):
        payload['payload'] = payload['payload'].replace('Invalid2Termination', GlobalVar.consumerInvalidTerminationPoint2)
    GlobalVar.api_dict['payload'] = payload
    print(GlobalVar.api_dict['payload'])

@step('I Set Consumer POST request Body "{data_file}"')
def set_body(context, data_file):
    payload = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], data_file)
    requestId = payloadGenerator.generate_reqId(context)
    GlobalVar.reqId= requestId
    print("requestId: " + requestId)
    GlobalVar.api_dict['payload'] = payload
    print(GlobalVar.api_dict['payload'])

@step('I send CS "{requestType}" request')
def sendHTTprequest(context, requestType):
    global response
    auth = context.config.get('RMQ_basicAuth')
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        if requestType == 'POST':
            response = requests.post(url=GlobalVar.api_dict['api_endpoint_' + requestType + '_url'],
                                     json=GlobalVar.api_dict['payload'],
                                     auth=HTTPBasicAuth(auth, auth), verify=False)
        if requestType == 'DELETE':
            response = requests.delete(url=GlobalVar.api_dict['api_endpoint_' + requestType + '_url'],
                                       auth=HTTPBasicAuth(auth, auth), verify=False)
        if requestType == 'GET':
            response = requests.get(url=GlobalVar.api_dict['api_endpoint_' + requestType + '_url'],
                                    auth=HTTPBasicAuth(auth, auth), verify=False)
        if requestType == 'PUT':
            response = requests.put(url=GlobalVar.api_dict['api_endpoint_' + requestType + '_url'],
                                    json=GlobalVar.api_dict['payload'],
                                    auth=HTTPBasicAuth(auth, auth), verify=False)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    print("======================"+GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])
    time.sleep(int(2))
    GlobalVar.response = response.text
    print(GlobalVar.response)




@step("I validate the consumer response body contains the request id")
def validate_request_id(context):
    time.sleep(int(1))
    print (GlobalVar.reqId)
    assert GlobalVar.reqId in GlobalVar.response

@step('I validate the consumer response body contains "{expectedText}"')
def step_impl(context, expectedText):
    assert expectedText in GlobalVar.response

@step('I extract the consumer response code value')
def extract_rep_code(context):
    GlobalVar.response_codes['queueStatus'] = response.status_code
    print("Extracted response code:" + str(response.status_code))

@step('I set Consumer "{apiType}" url')
def set_url(context, apiType, appName=''):
    global testCase
    if len(appName) != 0:
        url = ''.join([appName, "_", apiType, "_", sys.argv[2]])
    else: url = ''.join([apiType, "_", sys.argv[2]])
    GlobalVar.api_url = context.config.get(url)
    testCase = GlobalVar.test_case
    return GlobalVar.api_url

@step('I set CS api endpoint "{endpoint}" for "{requestType}"')
def rmq_endpoint(context, endpoint, requestType):
    if ("consumer_rabbit_exchange" in endpoint) and ("preprod" in GlobalVar.api_url):
        endpoint= endpoint.replace("consumer_rabbit_exchange", "rabbit_exchange")
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = set_endpoint_for_CS(context, requestType, endpoint)
    print(GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])

@step('I set CS api endpoint "{endpoint}" for "{requestType}" to publish the message')
def set_endpoint_exchange(context, endpoint, requestType):
    if ("preprod" in GlobalVar.api_url):
        endpoint = endpoint.replace("{exchange_Name}", "rabbit_exchange")
    elif ("qa" in GlobalVar.api_url):
        endpoint = endpoint.replace("{exchange_Name}", "consumer_rabbit_exchange")
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = set_endpoint_for_CS(context, requestType, endpoint)
    print(GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])

@step('I Set "{requestType}" api endpoint for "{endpoint}" for CS')
def set_endpoint_for_CS(context, requestType, endpoint):
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = GlobalVar.api_url + endpoint
    return GlobalVar.api_dict['api_endpoint_' + requestType + '_url']

@step('I validate consumer expected response code "{response_code}" for "{requestType}"')
def validate_consumer_rep_code(context, response_code, requestType):
    validate_consumer_response_code(context, response.status_code, int(response_code))

@step('I receive consumer valid HTTP response code "{actual_response_code}" as "{expected_response_code}"')
def validate_consumer_response_code(context, actual_response_code, expected_response_code):
    try:
        assert actual_response_code == expected_response_code
    except Exception as err:
        raise Exception(err)

@step('I Set POST Consumer request Body "{data_file}" for "{queueName}"')
def set_Consumerbody(context, data_file, queueName):
    payload = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], data_file)
    payload['routing_key'] = queueName
    GlobalVar.api_dict['payload'] = payload

@step('Validate that the queue is empty for Consumer')
def validate_no_response(context):
    assert not len(response.json())

@step('Validate consumer response header "{headerName}" for "{headerValue}"')
def valiadte_Consumer_header(context, headerName, headerValue):
    assert response.headers[headerName] == headerValue

@step('Validate that consumer "{queueName}" queue "{scenario}" "{exchangeName}" exchange as source')
def validate_consumer_queue(context, queueName, scenario, exchangeName):
    response_json['GET'] = response.json()
    try:
        for i in response_json['GET']:
            if 'has' in scenario:
                if i['destination'] == queueName:
                    assert i['source'] == exchangeName
                    GlobalVar.binded = True
                    break
                else:
                    GlobalVar.binded = False

            elif 'not' in scenario:
                assert i['destination'] != queueName

        if not GlobalVar.binded:
            print("Proceed to bind queue....")
    except:
        sys.exit("Queue Assertion Failed...Exiting Process Now")


@step("I configure the Consumer Nodes {Nodes}")
def configure_nodes(context, Nodes):
    nodeValue= Nodes.split(",");
    for node in nodeValue:
        if ("ValidNode1" in node):
            GlobalVar.consumerValidNode1 = context.config.get("ConsumerValidNode1")
            print("Consumer Node 1: " + GlobalVar.consumerValidNode1)
        if ("ValidNode2" in node):
            GlobalVar.consumerValidNode2 = context.config.get("ConsumerValidNode2")
            print("Consumer Node 2:  "+ GlobalVar.consumerValidNode2)
        if ("InvalidNode1" in node):
            GlobalVar.consumerInvalidNode1 = context.config.get("ConsumerInvalidNode1")
            print("Invalid Consumer Node 1:  " + GlobalVar.consumerInvalidNode1)
        if ("InvalidNode2" in node):
            GlobalVar.consumerInvalidNode2 = context.config.get("ConsumerInvalidNode2")
            print("Invalid Consumer Node 2:  " +GlobalVar.consumerInvalidNode2)

@step("I configure the Consumer Termination points {terminationPoints}")
def configure_termination_point(context, terminationPoints):
    termination_Points = terminationPoints.split(",");
    for terminationPoint in termination_Points:
        if ("ValidTerminationPoint1" in terminationPoint):
            GlobalVar.consumerTerminationPoint1 = context.config.get("ConsumerTermination_Point1")
            print("Consumer Termination point 1: " + GlobalVar.consumerTerminationPoint1)
        if ("ValidTerminationPoint2" in terminationPoint):
            GlobalVar.consumerTerminationPoint2 = context.config.get("ConsumerTermination_Point2")
            print("Consumer Termination point 2: " +GlobalVar.consumerTerminationPoint2 )
        if ("InValid1TerminationPoint" in terminationPoint):
            GlobalVar.consumerInvalidTerminationPoint1 = context.config.get("ConsumerTerminationInvalid_Point1")
            print("Invalid Consumer Termination point 1: " +GlobalVar.consumerInvalidTerminationPoint1)
        if ("InValid2TerminationPoint" in terminationPoint):
            GlobalVar.consumerInvalidTerminationPoint2 = context.config.get("ConsumerTerminationInvalid_Point2")
            print("Invalid Consumer Termination point 2: " +GlobalVar.consumerInvalidTerminationPoint2)


@step("I print the response")
def step_impl(context):
    print(response.text)


@then("I Decommission the BNG devices if the devices are onboarded")
def step_impl(context):
    print("******************")
    print(response.text)
    if("EDTNABTFNG03-EDTNABTFNG04" in response.text):
        print("Devices are already onboarded")
        GlobalVar.api_dict['api_endpoint_' + "POST" + '_url'] = set_endpoint_for_BI(context, "POST", "/api/exchanges/%2F/consumer_rabbit_exchange/publish")
        print(GlobalVar.api_dict['api_endpoint_' + "POST" + '_url'])


        payload = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], "DecommissionBNGDevices.json")
        requestId = payloadGenerator.generate_reqId(context)
        print("requestId: " + requestId)
        GlobalVar.reqId = requestId
        payload['payload'] = payload['payload'].replace('request-idValue', requestId)
        GlobalVar.api_dict['payload'] = payload

        auth = context.config.get('RMQ_basicAuth')

        respo = requests.post(url=GlobalVar.api_dict['api_endpoint_' + "POST" + '_url'],
                                 json=GlobalVar.api_dict['payload'],
                                 auth=HTTPBasicAuth(auth, auth), verify=False)

        print(respo.text)
        time.sleep(int(200))
    else:
        print("Devices are not already onboarded")

@then("I Decommission the OLT devices if the devices are onboarded")
def step_impl(context):
    print("******************")
    print(response.text)
    if("EDTNABTFOT39" in response.text):
        print("Devices are already onboarded")
        GlobalVar.api_dict['api_endpoint_' + "POST" + '_url'] = set_endpoint_for_BI(context, "POST", "/api/exchanges/%2F/consumer_rabbit_exchange/publish")
        print(GlobalVar.api_dict['api_endpoint_' + "POST" + '_url'])


        payload = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], "DecommissionOLTDevices.json")
        requestId = payloadGenerator.generate_reqId(context)
        print("requestId: " + requestId)
        GlobalVar.reqId = requestId
        payload['payload'] = payload['payload'].replace('request-idValue', requestId)
        GlobalVar.api_dict['payload'] = payload

        auth = context.config.get('RMQ_basicAuth')

        respo = requests.post(url=GlobalVar.api_dict['api_endpoint_' + "POST" + '_url'],
                                 json=GlobalVar.api_dict['payload'],
                                 auth=HTTPBasicAuth(auth, auth), verify=False)

        print(respo.text)
        time.sleep(int(200))
    else:
        print("Devices are not already onboarded")