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
from features.steps.bi.bi_uiFunctional import *
from features.steps.bi.bi_apiGateway import *
from features.steps.api_steps_general import *
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from features.steps.globalVar import GlobalVar
from features.steps.ui_steps_general import page_title_validation, change_currentPage
from selenium.webdriver.support.select import Select
from common.util.payloadGenerator import payloadGenerator
from common.util.api_test import ApiTest

# declared variables
from features.steps.globalVar import GlobalVar

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
testParams = {}
executedTestCases = []
request_Id = {}
configFiles = {}
addUser = {}
regNewUser = {}
state = {}
roleAdmin = {}
roleRW = {}
roleRead = {}
loginStatus = None
requestState = None
after_requestID = ''


# end of declared variables


@step('I Set HEADER param request for "{header}" as "{value}"')
def set_header_param(context, header, value):
    access_token = GlobalVar.testParams.get("Authorization")
    if access_token == 'Bearer Token':
        access_token = generate_access_token(context)
    if header == 'Authorization':
        request_headers[header] = 'Bearer {}'.format(access_token)
    GlobalVar.api_dict['request_header'] = request_headers


@step('I validate the response schema')
def step_impl(context):
    schema_file = GlobalVar.testParams.get("SchemaFile")
    assert validate_schema(context, schema_file, GlobalVar.testComponent[0],
                           response_json[GlobalVar.testParams.get("RequestType")])


@step('I Set headers "{header_1}" and "{header_2}"')
def set_controller_headers(context, header_1, header_2):
    header_1_Value = GlobalVar.testParams.get(header_1)
    header_2_Value = GlobalVar.testParams.get(header_2)
    set_header_request(context, header_1, header_1_Value)
    set_header_request(context, header_2, header_2_Value)


@step('I Set api endpoint and request Body')
def set_endpoint_and_body(context):
    global requestType, serviceId
    serviceId = GlobalVar.testParams.get('serviceId')
    mwrId = GlobalVar.testParams.get('mwrId')
    GlobalVar.requestType = GlobalVar.testParams.get('RequestType')
    endpoint = GlobalVar.testParams.get('EndPoint')
    api_url = GlobalVar.api_url

    # Set API endpoint
    if endpoint == '/bi/mpls/v1/service':
        api_endpoints[GlobalVar.requestType + '_URL'] = api_url + endpoint

    elif endpoint == '/bi/mpls/v1/service/{service_id}' or endpoint == '/bi/mpls/v1/service/{service_id}/activate':
        api_endpoints[GlobalVar.requestType + '_URL'] = api_url + endpoint.replace('{service_id}', serviceId)

    elif endpoint == '/bi/mpls/v1/service/{service_id}/mwr/{mwr_id}':
        api_endpoints[GlobalVar.requestType + '_URL'] = api_url + (endpoint.replace('{service_id}', serviceId)).replace(
            '{mwr_id}', mwrId)

    elif endpoint == '/bi/mpls/v1/requests/request/{request_id}/update' or \
            endpoint == '/bi/mpls/v1/requests/{request_id}/cancel' or \
            endpoint == '/bi/mpls/v1/requests/request/{request_id}/display' or \
            endpoint == '/bi/mpls/v1/requests/request/{request_id}/rollback' or \
            endpoint == '/bi/mpls/v1/requests/request/{request_id}/execute':
        api_endpoints[GlobalVar.requestType + '_URL'] = api_url + endpoint.replace('{request_id}', GlobalVar.reqId)
        if 'rollback' in endpoint:
            GlobalVar.request_ID['rollingBackId'] = GlobalVar.reqId

    elif endpoint == '/bi/mpls/v1/requests/request/{create_request_id}/update' or \
            endpoint == '/bi/mpls/v1/requests/request/{create_request_id}/rollback':
        api_endpoints[GlobalVar.requestType + '_URL'] = api_url + endpoint.replace('{create_request_id}',
                                                                                   GlobalVar.request_ID['POST'])
        if 'rollback' in endpoint:
            GlobalVar.request_ID['rollingBackId'] = GlobalVar.request_ID['POST']

    else:
        api_endpoints[GlobalVar.requestType + '_URL'] = api_url + endpoint

    # store the URI in the global dictionary api_dict
    GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url'] = api_endpoints[GlobalVar.requestType + '_URL']
    print("Request URL: ", GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url'])

    # Set request Body
    filename = GlobalVar.testParams.get('RequestBody')
    if not bool(filename):
        GlobalVar.api_dict['payload'] = None
    else:
        GlobalVar.api_dict['payload'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0],
                                                                              filename)


@step('I Send HTTP request for controller')
def send_HTTP_request_controller(context):
    # global requestId
    print("Sending {} request for controller".format(GlobalVar.requestType))
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        GlobalVar.response = requests.request(method=GlobalVar.requestType,
                                              url=GlobalVar.api_dict.get(
                                                  "api_endpoint_" + GlobalVar.requestType + "_url"),
                                              headers=GlobalVar.api_dict.get("request_header"),
                                              json=GlobalVar.api_dict.get("payload"),
                                              params=GlobalVar.api_dict.get('request_params'), verify=False)

        print(GlobalVar.response.text)
        response_codes[GlobalVar.requestType] = GlobalVar.response.status_code
        response_json[GlobalVar.requestType] = GlobalVar.response.json()

        # Validate response code
        if queryStatus != 'after':
            responseCodeVar = GlobalVar.testParams.get('ResponseCode')
            validate_response_code(context, int(response_codes[GlobalVar.requestType]), int(responseCodeVar))

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I validate response body for expected "{status}" and "{reason}"')
def validate_response(context, status, reason):
    assert GlobalVar.testParams.get('status') == response_json[GlobalVar.requestType][status]
    assert GlobalVar.testParams.get('reason') == response_json[GlobalVar.requestType][reason][0]


@step('I validate that a "{recordType}" record is found in "{indexType}" index')
def validate_ES_record(context, recordType, indexType):
    time.sleep(5)
    global ESRequestType
    searchId = None
    if recordType == 'request':
        searchId = GlobalVar.requestId
    elif recordType == 'service':
        searchId = GlobalVar.testParams.get('serviceId')
    elif recordType == 'MWR_service':
        searchId = GlobalVar.testParams.get('mwrId')
        recordType = 'service'
    url = set_API_type(context, 'ES') + GlobalVar.testParams.get('ES_{}_EndPoint'.format(recordType)) + searchId
    ESRequestType = GlobalVar.testParams.get('ESRequestType')
    print("ES {} URL: {}".format(recordType.upper(), url))
    auth = context.config.get('ES_basicAuth')
    try:
        urllib3.disable_warnings(InsecureRequestWarning)

        GlobalVar.response = requests.request(method=ESRequestType, url=url, auth=HTTPBasicAuth(context.config.get('ES_User'), context.config.get('ES_Pass')),
                                              verify=False)
        response_codes[ESRequestType] = GlobalVar.response.status_code
        response_json[ESRequestType] = GlobalVar.response.json()
        validate_response_code(context, int(response_codes[ESRequestType]),
                               int(GlobalVar.testParams.get('ES_{}_ResponseCode'.format(recordType))))

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I validate record format for "{recordType}" record')
def validate_record_format(context, recordType):
    schema_file = GlobalVar.testParams.get('ES_' + recordType + '_SchemaFile')
    assert validate_schema(context, schema_file, GlobalVar.testComponent[0], response_json[ESRequestType])


@step('I extract response value for expected "{responseKey}"')
def extract_response_val(context, responseKey):
    GlobalVar.requestId = response_json[GlobalVar.requestType]['requestId']
    GlobalVar.request_ID[GlobalVar.requestType] = GlobalVar.requestId
    GlobalVar.reqId = GlobalVar.requestId


@step('Validate that request "{stateName}" is "{stateStatus}"')
def validate_request_state(context, stateName, stateStatus):
    stateNameValue = response_json[ESRequestType]['_source'][stateName]
    assert stateNameValue.lower() == stateStatus.lower()


@step('Validate the service record for expected "{idVal}" and "{stateVal}"')
def validate_service_state(context, idVal, stateVal):
    if response_json[ESRequestType]['found']:
        if 'execute' in GlobalVar.api_dict[f'{GlobalVar.requestType}_URL']:
            GlobalVar.version = response_json[ESRequestType]["_source"]["associated-versions"][0]['version']

        assert response_json[ESRequestType]['_source'][idVal] == GlobalVar.testParams.get("serviceId")
        try:
            assert str(response_json[ESRequestType]['_source']['state']) == GlobalVar.testParams.get(stateVal)
        except:
            assert str(response_json[ESRequestType]['_source']['state']) == GlobalVar.testParams.get(stateVal + '2')
    else:
        assert response_json[ESRequestType]['_id'] == serviceId
        print("Service {} does not Exist".format(serviceId))


@step('Validate the service record for expected "{in_progressVal}" state')
def validate_in_progress_state(context, in_progressVal):
    assert str(response_json[ESRequestType]['_source']['in-progress']).lower() == \
           (GlobalVar.testParams.get(in_progressVal)).lower()


@step('I Set query parameters for controller request for "{precedence}"')
def set_query_params_Controller(context, precedence, value=''):
    global queryStatus
    queryStatus = precedence
    queryParamsFile = GlobalVar.testParams.get('QueryParams_' + precedence).format(value)
    if not bool(queryParamsFile):
        GlobalVar.api_dict['request_params'] = None
    else:
        GlobalVar.api_dict['request_params'] = payloadGenerator.load_payload_message(context,
                                                                                     GlobalVar.testComponent[0],
                                                                                     queryParamsFile)


@step('Validate the response is sorted in "{sortingOrder}" order according to "{requestTimestamp}"')
def assert_sorting_order(context, sortingOrder, requestTimestamp):
    global recordLength, serviceIdList
    recordLength = len(response_json[GlobalVar.requestType]['records'])
    serviceIdList, timeStampList = [], []
    for i in range(recordLength):
        time = response_json[GlobalVar.requestType]['records'][i][requestTimestamp]
        timeStampList.append(time)
        service = response_json[GlobalVar.requestType]['records'][i]['site-id']
        serviceIdList.append(service)

    for i in range(len(timeStampList) - 1):
        if sortingOrder == 'descending':
            assert timeStampList[i] >= timeStampList[i + 1]
        elif sortingOrder == 'ascending':
            assert timeStampList[i] <= timeStampList[i + 1]


@step('Validate that only records with service-id "{idVal}" are returned')
def validate_serviceId(context, idVal):
    idVal = GlobalVar.api_dict['request_params']["search_query['site-id']"]
    recordLength = len(response_json[GlobalVar.requestType]['records'])
    for i in range(recordLength):
        assert response_json[GlobalVar.requestType]['records'][i]['site-id'] == idVal


@step('Validate the service record for "{progress}" state to be "{value}"')
def validate_service_state(context, progress, value):
    assert response_json[ESRequestType]['_source']['id'] == serviceId
    print(str(response_json[ESRequestType]['_source'][progress]).lower())
    assert str(response_json[ESRequestType]['_source'][progress]).lower() == value


@step('I read service id for test case')
def read_serviceId(context):
    global serviceId
    serviceId = GlobalVar.testParams.get('serviceId')


@step('Update in_progress state for the service')
def change_state(context):
    global requestType
    if sys.argv[1] == "bi_clm":
        url = GlobalVar.api_url + GlobalVar.testParams.get("EndPoint").format(serviceId)
    else:
        url = GlobalVar.api_url + GlobalVar.testParams.get("EndPoint") + serviceId
    print("ES API URL: {}".format(url))
    GlobalVar.api_dict['request_bodies'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0],
                                                                                 GlobalVar.testParams.get(
                                                                                     'RequestBody'))
    GlobalVar.requestType = GlobalVar.testParams.get("RequestType")
    auth = context.config.get('ES_basicAuth')
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        GlobalVar.response = requests.request(method=GlobalVar.requestType, url=url,
                                              json=GlobalVar.api_dict['request_bodies'],
                                              auth=HTTPBasicAuth(auth, auth), verify=False)
        response_codes[GlobalVar.requestType] = GlobalVar.response.status_code
        response_json[GlobalVar.requestType] = GlobalVar.response.json()
        validate_response_code(context, int(response_codes[GlobalVar.requestType]),
                               GlobalVar.testParams.get('ResponseCode'))

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step('Validate that service record "{responseKey}" is "{responseValue}"')
def validate_response(context, responseKey, responseValue):
    assert response_json[GlobalVar.requestType][responseKey] == responseValue


@step('Validate that the "{messageType}" message is published to RMQ "{queueName}" queue')
def validate_request_message(context, messageType, queueName):
    time.sleep(5)
    RMQRequestType = GlobalVar.testParams.get('RMQ_RequestType')
    Endpoint = GlobalVar.testParams.get('RMQ_Fetch_EndPoint').replace('{queueName}', queueName)
    url = set_API_type(context, 'RMQ') + Endpoint
    print("RabbitMQ URL: {}".format(url))
    fileName = GlobalVar.testParams.get('RMQ_Fetch_RequestBody')
    GlobalVar.api_dict['request_bodies'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], fileName)
    auth = context.config.get('RMQ_basicAuth')

    urllib3.disable_warnings(InsecureRequestWarning)
    GlobalVar.response = requests.request(method=RMQRequestType, url=url, json=GlobalVar.api_dict['request_bodies'], auth=HTTPBasicAuth(auth, auth), verify=False)

    response_codes[RMQRequestType] = GlobalVar.response.status_code
    response_json[RMQRequestType] = GlobalVar.response.json()
    print(validate_response_code(context, int(response_codes[RMQRequestType]),
                           int(GlobalVar.testParams.get('RMQ_ResponseCode'))))

    # Messages in the queue are returned in a list
    responseList = response_json[RMQRequestType]
    responseLen = len(responseList)

    # Extracting latest message from the queue
    index = 0
    for i in range(responseLen):
        if not responseList[i]['message_count']:
            index = i
    # Validate the message body has id value same as request id returned by controller
    payloadValue = responseList[index]['payload']

    # convert extracted payload message in dictionary
    payloadConverted = json.loads(payloadValue)

    if messageType == 'request-tracker':
        assert payloadConverted['id'] == GlobalVar.requestId

    # Validate the message body has type as 'rollback' in case of rollback scenario
    if messageType == 'rollback':
        assert payloadConverted['request-characteristics']['type'] == messageType

    # Validate callback message
    if messageType == 'callback':
        assert payloadConverted['correlationId'] == GlobalVar.requestId

    # Validate error rollback message
    if messageType == 'rollback-error-message':
        assert payloadConverted['id'] == GlobalVar.reqId
        assert payloadConverted['request-characteristics']['type'] == messageType

    # Validate rollback timeout message
    if messageType == 'rollback-timeout':
        assert payloadConverted['id'] == GlobalVar.reqId
        assert (payloadConverted['request-characteristics']['type']).lower() == messageType.lower()

    # Validate portal rollback message
    if messageType == 'rollback-portal':
        assert payloadConverted['id'] == GlobalVar.request_ID[GlobalVar.requestType]
        assert payloadConverted['current-request-id'] == GlobalVar.request_ID['rollingBackId']


@step('Mock "{message}" response to be published to RMQ "{queueName}" queue')
def mock_response(context, message, queueName):
    global filepath
    time.sleep(5)
    RMQRequestType = GlobalVar.testParams.get('RMQ_RequestType')
    Endpoint = GlobalVar.testParams.get('RMQ_Publish_EndPoint')
    url = set_API_type(context, 'RMQ') + Endpoint
    print("RabbitMQ URL: {}".format(url))
    fileName = GlobalVar.testParams.get('RMQ_Publish_RequestBody').format(message)
    # read and update payload with the request Id/service Id
    payloadMessage = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], fileName)
    payloadMessage['routing_key'] = queueName
    GlobalVar.api_dict['request_bodies'] = update_payload(payloadMessage, message)
    auth = context.config.get('RMQ_basicAuth')
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        GlobalVar.response = requests.request(method=RMQRequestType, url=url, json=GlobalVar.api_dict['request_bodies'],
                                              auth=HTTPBasicAuth(auth, auth), verify=False)

        response_codes[RMQRequestType] = GlobalVar.response.status_code
        response_json[RMQRequestType] = GlobalVar.response.json()
        validate_response_code(context, int(response_codes[RMQRequestType]),
                               int(GlobalVar.testParams.get('RMQ_ResponseCode')))
        assert response_json[RMQRequestType]['routed']

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step('Validate that a callback is sent to PubSub for "{statusType}"')
def validate_callback_response(context, statusType):
    if sys.argv[1] == "bi_clm":
        context.callbackInfo = response_json[ESRequestType]['_source']['callback-info']
    else:
        context.callbackInfo = response_json[ESRequestType]['_source']['callback-info']
    schema_file = 'pubSub_{}.json'.format(statusType)
    assert validate_schema(context, schema_file, GlobalVar.testComponent[0], context.callbackInfo)


@step('Validate that the callback info has expected "{correlationId}" and status "{status}"')
def validate_callback_info(context, correlationId, status):
    assert context.callbackInfo['response']['event']['service']['status'] == status
    assert context.callbackInfo['response']['correlationId'] == GlobalVar.requestId


@step('I set api endpoint "{endpoint}" for "{requestType}"')
def rmq_endpoint(context, endpoint, requestType):
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = set_endpoint_for_BI(context, requestType, endpoint)
    print(GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])

@step('I Set POST request Body "{data_file}" for "{queueName}"')
def set_body(context, data_file, queueName):
    payload = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], data_file)
    payload['routing_key'] = queueName
    GlobalVar.api_dict['payload'] = payload


@step('I send "{requestType}" request')
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
            print(response.json())
        if requestType == 'PUT':
            response = requests.put(url=GlobalVar.api_dict['api_endpoint_' + requestType + '_url'],
                                    json=GlobalVar.api_dict['payload'],
                                    auth=HTTPBasicAuth(auth, auth), verify=False)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I validate expected response code "{response_code1}" or "{response_code2}" for "{requestType}"')
def validate_rep_code(context, response_code1, response_code2, requestType):
    try:
        validate_response_code(context, response.status_code, int(response_code1))
    except:
        validate_response_code(context, response.status_code, int(response_code2))


@step('I validate expected response code "{response_code}" for "{requestType}"')
def validate_rep_code(context, response_code, requestType):
    print(response.status_code)
    print(response_code)
    validate_response_code(context, response.status_code, int(response_code))


@step('Validate response header "{headerName}" for "{headerValue}"')
def valiadte_header(context, headerName, headerValue):
    assert response.headers[headerName] == headerValue


@step('Validate that "{queueName}" queue "{scenario}" "{exchangeName}" exchange as source')
def validate_queue(context, queueName, scenario, exchangeName):
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


@step('Validate the response is sorted in "{sortingOrder}" order for "{matchType}" match of "{searchTerm}"')
def assert_order(context, sortingOrder, matchType, searchTerm):
    global recordLength
    searchText = GlobalVar.api_dict['request_params']["search_query['{}']".format(searchTerm)]
    recordLength = len(response_json[GlobalVar.requestType]['records'])
    timeStampList = []
    for i in range(recordLength):
        if 'exact' in matchType:
            assert response_json[GlobalVar.requestType]['records'][i][searchTerm] == searchText
        elif 'partial' in matchType:
            assert searchText in response_json[GlobalVar.requestType]['records'][i][searchTerm]

        time = response_json[GlobalVar.requestType]['records'][i]['request-timestamp']
        timeStampList.append(time)

    for i in range(len(timeStampList) - 1):
        if sortingOrder == 'descending':
            assert timeStampList[i] >= timeStampList[i + 1]
        elif sortingOrder == 'ascending':
            assert timeStampList[i] <= timeStampList[i + 1]


@step('Validate that no duplicate records are returned for service-id')
def validate_records(context):
    serviceIdSet = set(serviceIdList)
    assert len(serviceIdSet) == len(serviceIdList)


@step('Validate the response has correct values against each key')
def validate_response(context):
    testFile = GlobalVar.testParams.get('responseDataFile')
    data = payloadGenerator.load_schema_message(context, GlobalVar.testComponent[0], 'testData/{}'.format(testFile))
    testData = json.dumps(data, sort_keys=True)
    responseData = json.dumps(response_json[GlobalVar.requestType], sort_keys=True)
    assert testData == responseData
    assert data == response_json[GlobalVar.requestType]


@step('Validate that the queue is empty')
def validate_no_response(context):
    assert not len(response.json())


@step('Validate all records are sorted in "{sortingOrder}" order according to "{requestTimestamp}"')
def assert_sorting_order(context, sortingOrder, requestTimestamp):
    global recordLength
    recordLength = len(response_json[GlobalVar.requestType]['records'])
    timeStampList = []
    for i in range(recordLength):
        time = response_json[GlobalVar.requestType]['records'][i][requestTimestamp]
        timeStampList.append(time)

    for i in range(len(timeStampList) - 1):
        if sortingOrder == 'descending':
            assert timeStampList[i] >= timeStampList[i + 1]
        elif sortingOrder == 'ascending':
            assert timeStampList[i] <= timeStampList[i + 1]


@step('Validate that all records have request "{resKey}" as "{resValue}"')
def validate_response_state(context, resKey, resValue):
    for i in range(recordLength):
        assert response_json[GlobalVar.requestType]['records'][i][resKey] == resValue


@step('Validate that a new request id is returned')
def validate_new_request_id(context):
    GlobalVar.request_ID['PUT'] = response_json[GlobalVar.requestType]['requestId']
    assert GlobalVar.request_ID['POST'] != GlobalVar.request_ID['PUT']
    GlobalVar.reqId = GlobalVar.request_ID['PUT']


@step('Validate that the request id has "{updateState}" parameters')
def validate_new_params(context, updateState):
    global requestType
    endpoint = None
    # define request method and endpoint for fetch request
    GlobalVar.requestType = GlobalVar.testParams.get('requestTypeFetch')
    if sys.argv[1] == 'bi_clm':
        endpoint = GlobalVar.testParams.get('endPointFetch').replace("{requestId}", GlobalVar.requestId)
        GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url'] = GlobalVar.api_url + endpoint
    else:
        endpoint = GlobalVar.testParams.get('endPointFetch').replace("{requestId}", GlobalVar.request_ID['PUT'])
        GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url'] = GlobalVar.api_url + endpoint
    print("Endpoint: ", GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url'])

    # send fetch parameter request which saves response in dictionary response_json
    send_HTTP_request_controller(context)
    # extract response value for prefixes, port and speed
    ipv4TprefixValue = response_json[GlobalVar.requestType]['Site Information']['Prefixes']['Ipv4 Provider Prefixes']
    ipv4CprefixValue = response_json[GlobalVar.requestType]['Site Information']['Prefixes']['IPv4 Customer Prefixes']
    if sys.argv[1] == 'bi_clm':
        pass
    else:
        port = response_json[GlobalVar.requestType]['Site Information']['Port']['Port']
        speed = response_json[GlobalVar.requestType]['Site Information']['Port']['Speed']
    inputBandwidth = response_json[GlobalVar.requestType]['Site Information']['QoS']['Ingress Override Rate (Kbps)']
    outputBandwidth = response_json[GlobalVar.requestType]['Site Information']['QoS']['Egress Override Rate (Kbps)']

    # assert that the response values are same as the ones sent in the payload for update request
    assert ipv4TprefixValue == GlobalVar.api_dict['payload']['ipv4-telus-prefixes']
    assert ipv4CprefixValue == GlobalVar.api_dict['payload']['ipv4-customer-prefixes']
    if sys.argv[1] != 'bi_clm':
        assert port == GlobalVar.api_dict['payload']['port']
        assert speed == GlobalVar.api_dict['payload']['speed']
    assert inputBandwidth == GlobalVar.api_dict['payload']['svc-input-bandwidth']
    assert outputBandwidth == GlobalVar.api_dict['payload']['svc-output-bandwidth']


@step('Validate that no duplicate records are returned for "{resKey}"')
def validate_no_duplicacy(context, resKey):
    serviceIdList = []
    for i in range(recordLength):
        service = response_json[GlobalVar.requestType]['records'][i][resKey]
        serviceIdList.append(service)
    serviceIdSet = set(serviceIdList)
    assert len(serviceIdSet) == len(serviceIdList)


@step('Validate that "{adminState}" is "{value}"')
def validate_admin_state(context, adminState, value):
    assert response_json[GlobalVar.requestType]["Site Information"]["Port"][adminState] == value


@step('Validate that the request is "{availabilityState}" in "{page}"')
def validate_request_queue(context, availabilityState, page):
    global requestType
    # define request method and endpoint for fetch request
    GlobalVar.requestType = GlobalVar.testParams.get('requestTypeFetch')
    endpoint = GlobalVar.testParams.get('endPointFetch')
    if 'queue' in page:
        endpoint = GlobalVar.testParams.get('endPointFetch') + '/queue'
    GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url'] = GlobalVar.api_url + endpoint
    print("Endpoint: {}".format(GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url']))

    # set query params for request
    if 'queue' in page:
        set_query_params_Controller(context, 'after', 'queue')
    else:
        set_query_params_Controller(context, 'after', 'dashboard')

    # send fetch parameter request which saves response in dictionary response_json
    send_HTTP_request_controller(context)
    recordLength = len(response_json[GlobalVar.requestType]['records'])
    record = {}
    if 'not' in availabilityState:
        # validate service record for request is not in service queue
        for i in range(recordLength):
            assert response_json[GlobalVar.requestType]['records'][i]['Service ID'] != serviceId
    else:
        # validate service record for request in dashboard
        # record = response_json[GlobalVar.requestType]['records'][0]
        # record = response_json[GlobalVar.requestType]['records'][0]['history'][0]
        for i in range(recordLength):
            if response_json[GlobalVar.requestType]['records'][i]['site-id'] == serviceId:
                record = response_json[GlobalVar.requestType]['records'][i]

        assert record['site-id'] == serviceId
        assert record['request-id'] == GlobalVar.requestId
        assert record['request-state'] == GlobalVar.testParams.get('stateChange')


@step('Execute the "{action}" request for processing')
def execute_controller_request(context, action):
    # generate access token and set header
    access_token = generate_access_token(context)
    set_header_request(context, 'Authorization', access_token)

    # generate url for the request
    url_Execute = 'executeAPIURL_' + sys.argv[2]
    GlobalVar.api_dict['executeURL'] = context.config.get(url_Execute).format(GlobalVar.requestId)
    print("Execute API URL: ", GlobalVar.api_dict['executeURL'])

    # set request body for execute api
    payloadFile = GlobalVar.testParams.get('executePayload')
    GlobalVar.api_dict['executePayload'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], payloadFile)

    # send API Request for execution
    try:
        GlobalVar.response = ApiTest.sendRequestjson(context, "POST", GlobalVar.api_dict['executeURL'], GlobalVar.api_dict.get("request_header"), None, GlobalVar.api_dict['executePayload'])

        # urllib3.disable_warnings(InsecureRequestWarning)
        # GlobalVar.response = requests.post(url=GlobalVar.api_dict['executeURL'], headers=GlobalVar.api_dict.get("request_header"),
        #                          json=GlobalVar.api_dict['executePayload'], verify=False)
        print(GlobalVar.response.text)

        if "rate" not in str(context.feature.filename).lower():
            # Validate Response Code
            validate_response_code(context, int(GlobalVar.response.status_code), context.config.get('executeAPIResponse'))

            # extract request execution status from the response
            print('BI Service Request Execute Status: ', GlobalVar.response.json()['status'])
            assert GlobalVar.response.json()['status'] == 'success'

    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I validate response body should have "{keyName}" as expected response')
def validate_response(context, keyName):
    assert response_json[GlobalVar.requestType][keyName] == GlobalVar.testParams.get(keyName)


@step('Validate that request "{stateName}" is not "{stateStatus}"')
def validate_request_state(context, stateName, stateStatus):
    stateNameValue = response_json['GET']['_source'][stateName]
    assert stateNameValue.lower() != stateStatus.lower()


@step('Validate that "{adminState}" is either "{value1}" or "{value2}"')
def validate_admin_state(context, adminState, value1, value2):
    assert response_json[GlobalVar.requestType]["Site Information"]["Port"][adminState] == value1 or \
           response_json[GlobalVar.requestType]["Site Information"]["Port"][adminState] is None


@step('Validate that correct error code "{errCode}" is published to NB')
def validate_error_code(context, errCode):
    assert context.callbackInfo['response']['event']['service']['code'] == errCode


@step('I validate response body should have "{response_key}" as "{response_value}"')
def validate_response_value(context, response_key, response_value):
    assert response_json[GlobalVar.requestType][response_key] == response_value


@step('I set data values against test case "{scenario}"')
def set_params(context, scenario):
    global testCase
    testCase = scenario
    GlobalVar.testParams = context.csvReadAPI[int(testCase) - 1]


@step('Wait for the expected timeout value for service')
def wait_for_timeout(context):
    waitTime = GlobalVar.testParams.get("waitTime")
    print("Waiting for timeout value:", waitTime, 'Seconds')
    time.sleep(int(waitTime))


@step('I extract the response code value')
def extract_rep_code(context):
    GlobalVar.response_codes['queueStatus'] = response.status_code
    # print("Extracted response code:" + str(response.status_code))
    #Using above commented line for CS Only


@step('I validate "{queueName}" queue is binded to "{exchangeName}" exchange')
def assert_responseCode(context, queueName, exchangeName):
    if response.status_code == 200:
        endpoint = None
        # if sys.argv[1] == 'bi':
        endpoint = f'/api/exchanges/%2F/{exchangeName}/bindings/source'
        # elif sys.argv[1] == 'l3vpn':
        #     endpoint = f'api/exchanges/%2F/{exchangeName}/bindings/source'
        requestType = 'GET'
        rmq_endpoint(context, endpoint, requestType)
        sendHTTprequest(context, requestType)
        validate_queue(context, queueName, 'has', exchangeName)
    else:
        print("Info: Queue Does not exist")


@step('I validate bind status from the previous step')
def assert_code(context):
    if GlobalVar.binded:
        print('Info: Skipping Create Queue Scenario as Queue already Exists and Binded')
        context.scenario.skip(reason='Queue Exists')
    else:
        print('Info: Proceed to Create and Bind Queue as Queue do not already Exist')


@step('I Set PUT request Body "{fileName}" for "{queueName}"')
def set_body(context, fileName, queueName):
    payload = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(), fileName)
    GlobalVar.api_dict['payload'] = payload


# XX-------------------------------XX Methods common to Controller Tests XX---------------------------------------XX

def validate_schema(context, schema_file, component, response):
    schema_file_name = os.getcwd() + '/resources/schema/' + sys.argv[1] + '/' + component.lower() \
                       + '/' + schema_file
    with open(schema_file_name, "r") as read_file:
        data = read_file.read()
        schema = json.loads(data)
        try:
            validate(instance=response, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            print(err)
            return False


def update_payload(payload, message):
    # Update correlation Id in payload
    if 'display' in GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url'] or \
            'execute' in GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url']:
        payload['payload'] = (payload['payload']).replace('requestId', GlobalVar.reqId)
    else:
        payload['payload'] = (payload['payload']).replace('requestId', GlobalVar.request_ID[GlobalVar.requestType])

    # Update rollback id in payload
    if 'rollback' in GlobalVar.api_dict['api_endpoint_' + GlobalVar.requestType + '_url']:
        payload['payload'] = (payload['payload']).replace('rollingBackId', GlobalVar.reqId)

    # update service Id in payload
    payload['payload'] = (payload['payload']).replace('serviceId', GlobalVar.testParams.get('serviceId'))

    # Update mwr Id in payload
    if 'mwr' in message:
        payload['payload'] = (payload['payload']).replace('mwrId', GlobalVar.testParams.get('mwrId'))

    return payload


# XX-------------------------------XX End of Methods  XX---------------------------------------XX


@step('Validate that no callback is sent to PubSub')
def validate_callback_response(context):
    context.callbackInfo = response_json['GET']['_source']['callback-info']
    assert context.callbackInfo['url'] is None


@step("I create a document id for request record creation")
def step_impl(context):
    global after_requestID
    if GlobalVar.uuid == {}:
        GlobalVar.uuid['req_id'] = payloadGenerator.generate_reqId(context)
        after_requestID = GlobalVar.uuid['req_id']


@step('I set api endpoint for "{processType}" a requests record')
def set_endpoint(context, processType):
    endPoint = GlobalVar.api_url + GlobalVar.testParams.get('ES_' + processType + '_endpoint')

    GlobalVar.api_dict['ES_' + processType + '_endpoint'] = endPoint.replace('{doc_id}', GlobalVar.uuid['req_id'])
    print(GlobalVar.api_dict['ES_' + processType + '_endpoint'])


@step('I set api request body for "{processType}" a requests record')
def set_endpoint(context, processType):
    if sys.argv[1] == 'bi_clm':
        if processType == 'delete':
            payloadFileName = GlobalVar.testParams.get('ES_' + processType + '_requestBody')
        else:
            payloadFileName = processType + 'RequestRecord.json'
    else:
        payloadFileName = GlobalVar.testParams.get('ES_' + processType + '_requestBody')


    if bool(payloadFileName):
        messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(),
                                                            payloadFileName)
        messageBody['id'] = GlobalVar.uuid['req_id']
        print(messageBody["id"])

        if sys.argv[1] == "bi":
            messageBody['request-characteristics']['response'] = GlobalVar.uuid['req_id']
        elif sys.argv[1] == "bi_clm":
            print(sys.argv[1])
            messageBody['request-characteristics']['url-query-parameters'][0]['value'] = GlobalVar.testParams.get(
                "serviceId")
            messageBody['request-characteristics']['payload']['serviceCharacteristic'][0]['value'][
                'telus-network-resource']['telus-network-resource-id'] = GlobalVar.testParams.get("serviceId")
            messageBody['request-characteristics']['payload']["serviceCharacteristic"][0]["value"][
                "telus-network-resource"][
                "telus-cust-service-id"] = GlobalVar.testParams.get("serviceId")
            messageBody['request-characteristics']['payload']["supportingService"][0]["serviceCharacteristic"][0][
                "value"]["telus-network-resource"]["telus-cust-service-id"] = GlobalVar.testParams.get("serviceId")
            messageBody['request-characteristics']['response']['requestId'] = GlobalVar.uuid['req_id']

        print(json.dumps(messageBody, indent=4))
        GlobalVar.api_dict['ES_' + processType + '_requestBody'] = messageBody
    else:
        GlobalVar.api_dict['ES_' + processType + '_requestBody'] = None


@step('Update request state "{value}" for "{value2}" service')
def chnage_state(context, value, value2):
    # payloadFileName = value2 + 'RequestRecord.' + 'json'
    # messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(),
    #                                                     payloadFileName)
    # messageBody['state'] = value
    GlobalVar.api_dict[f'ES_{value2}_requestBody']['state'] = value
    print(json.dumps(GlobalVar.api_dict[f'ES_{value2}_requestBody'], indent=4))


@step('I validate that the requests record is "{recordResult}"')
def validate_record(context, recordResult):
    ES_RequestType = GlobalVar.api_dict['requestType']
    response_json[ES_RequestType] = GlobalVar.response.json()
    recordCreated = response_json[ES_RequestType]['result']
    assert recordCreated == recordResult
    documentId = response_json[ES_RequestType]['_id']
    assert documentId == GlobalVar.uuid['req_id']


@step('Validate that "{fieldName}" field is "{scenario}" in callback info')
def validate_callback_info(context, fieldName, scenario):
    global index, characteristicsList
    matched = None
    characteristicsList = context.callbackInfo['response']['event']['data']['Event'][
        'OrderStatusNotification']['CharacteristicValue']
    index = None
    for i in range(len(characteristicsList)):
        dictList = list(characteristicsList[i])
        for entry in dictList:
            if entry == fieldName:
                matched = True
                index = i
                break
            else:
                matched = False
        if matched: break
    if 'not' in scenario:
        assert not matched
    else:
        assert matched


@step('Validate that the callback info has "{fieldName}" set as "{Value}"')
def validate_callback_info(context, fieldName, Value):
    assert characteristicsList[index][fieldName] == Value


@step('Validate that the callback info has "{fieldName}" as "{Value}"')
def validate_callback_info(context, fieldName, Value):
    assert characteristicsList[index][fieldName] == GlobalVar.testParams.get(Value)


@step('Validate that "{fieldName}" in response is not a null value')
def validate_field_not_null(context, fieldName):
    assert response_json[GlobalVar.requestType]['Site Information']['SAP'][fieldName] is not None


@step('Validate the service record for expected "{mwrId}" value')
def validate_in_progress_state(context, mwrId):
    assert str(response_json['GET']['_source'][mwrId]).lower() == str(GlobalVar.testParams.get('mwrIDValue')).lower()


@step('Validate that service "{key}" is "{value}"')
def step_impl(context, key, value):
    if 'not' in value:
        assert str(response_json['GET']['_source'][key]).lower() == str(GlobalVar.testParams.get('mwrIDValue')).lower()
    else:
        assert str(response_json['GET']['_source'][key]).lower() == str(value).lower()


@step('Validate that parameters information is available')
def validate_new_params(context):
    global requestType
    # define request method and endpoint for fetch request
    requestType = GlobalVar.testParams.get('requestTypeFetch')
    endpoint = GlobalVar.testParams.get('endPointFetch').replace("{requestId}", GlobalVar.request_ID['PUT'])
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = GlobalVar.api_url + endpoint
    print("Endpoint: ", GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])

    # send fetch parameter request which saves response in dictionary response_json
    send_HTTP_request_controller(context)


@step('Validate that the "{fieldName}" value is "{expectedValue}"')
def validate_ipv6(context, fieldName, expectedValue):
    assert response_json[GlobalVar.requestType]['Site Information']['Prefixes'][fieldName] is not None


@step('Validate that only records with "{matchType}" match for "{searchTerm}" are returned')
def validate_serviceId(context, matchType, searchTerm):
    searchResult = GlobalVar.api_dict['request_params']["search_query['{}']".format(searchTerm)]
    recordLength = len(response_json[GlobalVar.requestType]['records'])
    for i in range(recordLength):
        if 'exact' in matchType:
            assert response_json[GlobalVar.requestType]['records'][i][searchTerm].lower() == searchResult.lower()
        elif 'partial' in matchType:
            assert searchResult.lower() in response_json[GlobalVar.requestType]['records'][i][searchTerm].lower()


@step('Validate that "{responseVal}" records for the search are returned')
def no_records(context, responseVal):
    if 'no' in responseVal:
        assert not len(response_json[GlobalVar.requestType]['records'])
        assert not response_json[GlobalVar.requestType]['total_size']
    else:
        assert len(response_json[GlobalVar.requestType]['records'])
        assert response_json[GlobalVar.requestType]['total_size']


@step('I validate response body for expected "{fieldName}"')
def validate_response(context, fieldName):
    assert GlobalVar.testParams.get(fieldName).lower().replace(" ", "") == \
           response_json[GlobalVar.requestType][fieldName].lower().replace(" ", "")


@step('Validate that the "{fieldName}" is same as the query parameter')
def step_impl(context, fieldName):
    assert response_json[ESRequestType]['_source']['user-id'] == GlobalVar.api_dict['request_params'][fieldName]


@step('Validate that the request id has deleted parameters')
def validate_new_params(context):
    global requestType
    endpoint = None
    # define request method and endpoint for fetch request
    requestType = GlobalVar.testParams.get('requestTypeFetch')
    endpoint = GlobalVar.testParams.get('endPointFetch').replace("{requestId}", GlobalVar.request_ID['DELETE'])
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = GlobalVar.api_url + endpoint
    print("Endpoint: ", GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])

    # send fetch parameter request which saves response in dictionary response_json
    send_HTTP_request_controller(context)


@step("I create a document id for after request record creation")
def step_impl(context):
    GlobalVar.uuid['req_id'] = payloadGenerator.generate_reqId(context)

@step('I set api endpoint for "{processType}" a after requests record')
def set_endpoint(context, processType):
    global after_requestID
    endPoint = GlobalVar.api_url + GlobalVar.testParams.get('ES_' + processType + '_endpoint')

    GlobalVar.api_dict['ES_' + processType + '_endpoint'] = endPoint.replace('{doc_id}', after_requestID)
    print(GlobalVar.api_dict['ES_' + processType + '_endpoint'])
