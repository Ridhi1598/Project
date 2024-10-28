import json
import os
import sys
import requests
import urllib3
from behave import *
from requests import HTTPError, request
from features.steps.bi.bi_uiFunctional import *
from features.steps.bi.bi_controller import *
from features.steps.bi.bi_apiGateway import *
from features.steps.bi.bi_restApis import *
from features.steps.api_steps_general import *
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
from features.steps.globalVar import GlobalVar
from features.steps.ui_steps_general import page_title_validation, change_currentPage
from common.util.payloadGenerator import payloadGenerator
from common.util.zookeeper import ZK

# declared variables
callbackInfo = {}
param = {}
external_requestId = {}
callbackResponse = {}
index = {}
callbacks = []
testCase = None
requestType = None
payloadParamValue = None
esRequestType = None
response_json = {}
parentPath = ''
# node = ''
# zk = None


# end of declared variables


@step('I set data values against testcase')
def read_test_params(context):
    global testCase
    testCase = context.feature.filename.split('_')[4].split('.')[0]
    GlobalVar.testParams = context.csvReadAPI[int(testCase) - 1]
    assert GlobalVar.testParams.get('TestCase') == testCase
    GlobalVar.testParams[testCase] = GlobalVar.testParams
    GlobalVar.testParams[testCase] = {"requestId": None}


@step('I set api endpoint for "{messageType}" message for "{messageReadType}"')
def set_EP(context, messageType, messageReadType):
    global requestType
    endPoint = GlobalVar.api_url + GlobalVar.testParams.get(messageType + 'RMQEndPoint')
    if messageType == 'read':
        endpoint = endPoint.replace("{queueName}",
                                    GlobalVar.testParams.get(messageType + 'RMQQueueName_' + messageReadType))
    else:
        endpoint = endPoint
    requestType = GlobalVar.testParams.get(messageType + 'RMQRequestType')
    GlobalVar.api_dict[requestType + '_endPoint_' + messageType] = endpoint


@step('I set request body for "{messageType}" message for "{messageReadType}"')
def set_ES_body(context, messageType, messageReadType):
    global payloadParamValue
    messageBody = {}
    # define queue name where the message should be published/read
    queue = GlobalVar.testParams.get(messageType + 'RMQQueueName_' + messageReadType)
    payloadFile = GlobalVar.testParams.get(messageType + 'RMQRequestBody_' + messageReadType)

    if messageType == 'publish':
        # generate request Id and store in a global variable
        if GlobalVar.testParams[testCase]["requestId"] is None:
            GlobalVar.testParams[testCase]["requestId"] = payloadGenerator.generate_reqId(context)
            print("Request_Id: {}".format(GlobalVar.testParams[testCase]["requestId"]))

        # replace request id with a unique value in payload
        messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(), payloadFile)
        messageBody["routing_key"] = queue
        messageBody["payload"] = messageBody["payload"].replace("currentDateTime", str(datetime.datetime.now()))

        if 'display-rollback' in messageBody["payload"]:
            messageBody["payload"] = messageBody["payload"].replace("req_id2", GlobalVar.uuid[testCase][2]).replace(
                "req_id1", GlobalVar.uuid[testCase][1]).replace("req_id0", GlobalVar.uuid[testCase][0])
            payloadParamValue = GlobalVar.uuid[testCase][2]
        else:
            messageBody["payload"] = messageBody["payload"].replace("req_id",
                                                                    GlobalVar.testParams[testCase]["requestId"])
            payloadParamValue = GlobalVar.testParams[testCase]["requestId"]

    if messageReadType == 'rollback':
        messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(), payloadFile)
        messageBody["routing_key"] = queue

        # replace the request id with the same one generated above
        messageBody["payload"] = messageBody["payload"].replace("req_id", GlobalVar.testParams[testCase]["requestId"])

        # extract rollingBack id
        operationsCount = GlobalVar.testParams.get('operationsCount')
        if len(operationsCount) != 0:
            assert len(GlobalVar.uuid[testCase]) == int(GlobalVar.testParams.get('operationsCount'))
            docIdKey = int(operationsCount) - 1
            if 'rollingBackId' in messageBody["payload"]:
                messageBody["payload"] = messageBody["payload"].replace("rollingBackId",
                                                                        GlobalVar.uuid[testCase][docIdKey])
    if messageType == 'read':
        payloadFile = GlobalVar.testParams.get(messageType + 'RMQRequestBody')
        messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(), payloadFile)
    GlobalVar.api_dict[messageType + '_payload'] = messageBody


@step('Send request to "{messageType}" message in RMQ queue')
def step_impl(context, messageType):
    auth = context.config.get('RMQ_basicAuth')
    requestType = GlobalVar.testParams.get(messageType + 'RMQRequestType')
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        GlobalVar.response = requests.request(method=requestType,
                                              url=GlobalVar.api_dict[requestType + '_endPoint_' + messageType],
                                              json=GlobalVar.api_dict[messageType + '_payload'],
                                              auth=HTTPBasicAuth(auth, auth), verify=False)
        # Validate response code
        responseCodeVar = GlobalVar.testParams.get(messageType + 'RMQResponseCode')
        validate_response_code(context, int(GlobalVar.response.status_code), int(responseCodeVar))
        response_json[requestType] = GlobalVar.response.json()
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise err


@step('Validate that response body has "{responseKey}" as "{responseValue}"')
def validate_response(context, responseKey, responseValue):
    response_json[requestType] = GlobalVar.response.json()
    assert str(response_json[requestType][responseKey]).lower() == responseValue.lower()


@step('Validate that there is no message in the RMQ queue')
def validate_no_response(context):
    assert GlobalVar.response.text == '[]'


@step('I set api endpoint for "{recordType}" record for "{messageType}" ES message')
def set_ES_Endpoint(context, recordType, messageType):
    global ESRequestType
    endPoint = GlobalVar.api_url + GlobalVar.testParams.get(messageType + 'ESEndPoint_' + recordType)
    ESRequestType = GlobalVar.testParams.get(messageType + 'ESRequestType')
    GlobalVar.api_dict[ESRequestType + '_endPoint'] = endPoint
    print(GlobalVar.api_dict[ESRequestType + '_endPoint'])


@step('I set request body for "{recordType}" record for "{messageType}" ES message')
def set_ES_body(context, recordType, messageType):
    global esRequestType

    esRequestType = GlobalVar.testParams.get('readESRequestType')
    payloadFileName = GlobalVar.testParams.get(messageType + 'ESRequestBody_' + recordType)
    messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(),
                                                        payloadFileName)

    if recordType == 'request':
        messageBody['query']['bool']['must'][0]['term']['id'] = payloadParamValue

    elif recordType == 'displayRequest':
        messageBody['query']['bool']['must'][0][
            'term']['request-characteristics.response.requestId'] = payloadParamValue

    elif recordType == 'service':
        messageBody['query']['bool']['must'][0]['term']['bi.mpls.bi-services.bi-service.customer-name'] = \
            GlobalVar.testParams.get('customerName')

    GlobalVar.api_dict[recordType + '_payload_' + esRequestType] = messageBody
    print(GlobalVar.api_dict[recordType + '_payload_' + esRequestType])


@step('I validate that a "{recordType}" record is "{createdState}" in "{indexType}" index')
def validateES_record(context, recordType, createdState, indexType):
    time.sleep(5)
    esRequestType = GlobalVar.testParams.get('readESRequestType')
    user = context.config.get('ES_User')
    password = context.config.get('ES_Pass')
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        GlobalVar.response = requests.request(method=esRequestType, url=GlobalVar.api_dict[ESRequestType + '_endPoint'],
                                              json=GlobalVar.api_dict[recordType + '_payload_' + esRequestType],
                                              auth=HTTPBasicAuth(user, password),
                                              verify=False)

        response_codes[esRequestType] = GlobalVar.response.status_code
        response_json[esRequestType] = GlobalVar.response.json()

        # validate response code
        validate_response_code(context, int(response_codes[esRequestType]), context.config.get('ES_APIResponse'))

        recordFound = response_json[esRequestType]['hits']['total']['value']
        # assert the status of record being found or not
        if 'not' in createdState:
            assert recordFound == 0
        else:
            assert recordFound > 0

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except AssertionError as e:
        raise e
    except Exception as err:
        raise err


@step('Validate a request id is returned by mediation layer as synchronous response')
def validate_external_reqId(context):
    global external_requestId
    try:
        external_requestId['request'] = response_json[esRequestType]['hits']['hits'][0]['_source'][
            'external-request-tracker'][0]['id']
        assert len(external_requestId['request']) != 0
        print("External_Request_Tracker: {}".format(external_requestId['request']))
    except Exception as e:
        print(e)


@step('Wait for the callback response from "{component}"')
def wait_for_callback(context, component):
    waitTime = GlobalVar.testParams.get('waitTime_{}'.format(component))
    print("Waiting for: {} seconds".format(str(waitTime)))
    time.sleep(int(waitTime))


@step('Validate a callback response is returned by mediation layer as asynchronous response')
def validate_callback(context):
    global callbackInfo
    callbackInfo = response_json[esRequestType]['hits']['hits'][0]['_source']['external-request-tracker'][0][
        'callback-info']


@step('Validate the "{responseKey}" value in the response')
def validate_res_val(context, responseKey):
    if responseKey == 'request_id':
        assert callbackInfo['payload'][responseKey] == external_requestId['request']
    else:
        assert str(callbackInfo['payload'][responseKey]).lower() == GlobalVar.testParams.get(
            responseKey + '_value').lower()


@step('Validate that a "{messageStatus}" message is published to controller')
def validate_callback_response(context, messageStatus):
    if messageStatus == "no":
        print(response_json[requestType])

    else:
        responseList = response_json[requestType]
        responseLen = len(responseList)

        # Extracting latest message from the queue
        indexVal = None
        for i in range(responseLen):
            if responseList[i]['message_count'] == 0: indexVal = i

        if indexVal is None:
            print("{} response index not accessible".format(messageStatus))

        # Validate the message body has id value same as request id returned by controller
        payloadValue = responseList[indexVal]['payload']

        # convert extracted payload message in dictionary
        response_json['payloadConverted'] = json.loads(payloadValue)

        # Assert correlation id and request status
        assert response_json['payloadConverted']['correlationId'] == payloadParamValue
        assert response_json['payloadConverted']['event']['service']['status'] == messageStatus


@step('Validate response format for "{messageStatus}" message')
def step_impl(context, messageStatus):
    schemaFileName = GlobalVar.testParams.get('callbackSchemaFile')
    result = validate_schema(context, schemaFileName, GlobalVar.testComponent[0], response_json['payloadConverted'])
    assert result


@step('I validate record format for "{recordType}" response')
def step_impl(context, recordType):
    global response_json
    schemaFileName = GlobalVar.testParams.get('ES_' + recordType + '_SchemaFile')
    esRequestType = GlobalVar.testParams.get('readESRequestType')
    response_json[esRequestType] = GlobalVar.response.json()
    result = validate_schema(context, schemaFileName, GlobalVar.testComponent[0], response_json[esRequestType])
    assert result


@step('Validate that the service record has "{availability}" same "{responseKey}"')
def validate_request_value(context, availability, responseKey):
    requestsList = response_json[esRequestType]['hits']['hits'][0]['_source']['bi']['mpls']['bi-services'][
        'bi-service'][0][responseKey]
    for i in range(len(requestsList)):
        if 'not' in availability:
            assert requestsList[i]['id'] != GlobalVar.testParams[testCase]["requestId"]
        else:
            if requestsList[i]['id'] == GlobalVar.testParams[testCase]["requestId"]:
                break


@step('Validate that the service record has "{responseKey}" in correct format')
def validate_request_value(context, responseKey):
    vpnId = response_json[esRequestType]['hits']['hits'][0]['_source']['bi']['mpls']['bi-services']['bi-service'][0][
        responseKey]
    assert vpnId == GlobalVar.testParams.get('customerName') + '-BI-MPLS'


@step('Validate that no callback response is returned by mediation layer')
def validate_callback(context):
    externalTracker = response_json[esRequestType]['hits']['hits'][0]['_source']['external-request-tracker']
    for i in range(len(externalTracker)):
        dictKeys = externalTracker[i].keys()
        for j in range(0, len(dictKeys)): assert dictKeys != 'callback-info'


@step('I set api endpoint for "{processType}" a "{recordType}" record')
def set_endpoint(context, processType, recordType):
    endPoint = GlobalVar.api_url + GlobalVar.testParams.get('ES_' + processType + '_endpoint')

    if processType == 'create':
        if sys.argv[1] == 'l3vpn':
            randomId = GlobalVar.testParams.get("serviceId")
        else:
            randomId = ''.join(random.choices(string.digits + string.ascii_lowercase, k=20))

        if recordType not in GlobalVar.docId[testCase].keys():
            GlobalVar.docId[testCase].update({recordType: randomId})
        print("{} record document id : {}".format(recordType, GlobalVar.docId[testCase][recordType]))

    if processType == 'delete':
        print("{} record document id : {}".format(recordType, GlobalVar.docId[testCase][recordType]))

    GlobalVar.api_dict['ES_' + processType + '_endpoint'] = \
        endPoint.replace('{doc_id}', GlobalVar.docId[testCase][recordType]).replace('recordType', recordType)


@step('I set api request body for "{processType}" a "{recordType}" record')
def set_requestBody(context, processType, recordType):
    payloadFileName = GlobalVar.testParams.get('ES_' + processType + '_' + recordType + '_requestBody')

    if recordType == 'services':
        if payloadFileName != 'None':
            messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(),
                                                                payloadFileName)
            GlobalVar.uuid[testCase] = payloadGenerator.generate_reqId(context)
            # generate a new uuid for record creation
            if sys.argv[1] == 'bi':
                messageBody['bi']['mpls']['bi-services']['bi-service'][0]['associated-requests'][0]['id'] = \
                    GlobalVar.uuid[testCase]
            GlobalVar.api_dict['ES_' + processType + '_requestBody'] = messageBody
        else:
            GlobalVar.api_dict['ES_' + processType + '_requestBody'] = None

    if recordType == 'requests':
        if payloadFileName != 'None':
            messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(),
                                                                payloadFileName)
            messageBody['id'] = GlobalVar.uuid[testCase]
            messageBody['request-characteristics']['response']['requestId'] = GlobalVar.uuid[testCase]
            messageBody['external-request-tracker'][0]['request-characteristics']['payload']['config']['bi-service'][
                0]['associated-requests'][0]['id'] = GlobalVar.uuid[testCase]
            GlobalVar.api_dict['ES_' + processType + '_requestBody'] = messageBody
        else:
            GlobalVar.api_dict['ES_' + processType + '_requestBody'] = None


@step('I send HTTP request for "{processType}" service')
def send_ES_request(context, processType):
    global ES_requestType
    endpointFormat = GlobalVar.testParams.get('EndPoint')
    ES_requestType = GlobalVar.testParams.get('ES_' + processType + '_requestType')
    if ES_requestType == "POST":
        GlobalVar.api_dict['header'] = {"Content-Type": "application/json"}
    else:
        GlobalVar.api_dict['header'] = None
    user = context.config.get("ES_User")
    password = context.config.get("ES_Pass")
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        GlobalVar.response = requests.request(method=ES_requestType,
                                              url=GlobalVar.api_dict['ES_' + processType + '_endpoint'],
                                              headers=GlobalVar.api_dict['header'],
                                              json=GlobalVar.api_dict['ES_' + processType + '_requestBody'],
                                              auth=HTTPBasicAuth(user, password), verify=False)
        # Validate response code
        print("RESPONSE CODE::", GlobalVar.response.status_code)
        print("RESPONSE{}{}",GlobalVar.response.json())
        responseCodeVar = GlobalVar.testParams.get('ES_' + processType + '_responseCode')
        validate_response_code(context, int(GlobalVar.response.status_code), int(responseCodeVar))
        response_json[ES_requestType] = GlobalVar.response.json()
        GlobalVar.api_dict['requestType'] = ES_requestType

        if sys.argv[1] == "bi_clm":
            if 'cancel' in endpointFormat:
                pass
            else:
                GlobalVar.requestId = response_json[ES_requestType]['_id']
                GlobalVar.node = GlobalVar.requestId
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise err


@step('I validate that the "{recordType}" record is "{recordResult}" in "{indexType}" index for "{operationType}"')
def validate_record(context, recordType, recordResult, indexType, operationType):
    recordCreated = response_json[ES_requestType]['result']
    assert recordCreated == recordResult
    documentId = response_json[ES_requestType]['_id']

    if recordType == 'requests':
        assert documentId == GlobalVar.docId[testCase][recordType][operationType]
    elif recordType == 'services':
        assert documentId == GlobalVar.docId[testCase][recordType]


@step('I validate the "{value}" value in "{tracker}"')
def validate_request_type(context, value, tracker):
    externalRequestType = response_json[esRequestType]['hits']['hits'][0]['_source'][tracker][0][
        'request-characteristics'][value]
    assert externalRequestType.lower() == GlobalVar.testParams.get('externalRequestType').lower()


@step('Validate there is a "{fieldName}" field "{foundStatus}" in the error message')
def validate_error_category(context, fieldName, foundStatus):
    errorMessage = callbackInfo['payload']['errors'][0]
    dictKeys = list(errorMessage.keys())

    for i in range(len(dictKeys)):
        if 'not' in foundStatus:
            assert dictKeys[i] != fieldName
        else:
            if dictKeys[i] == fieldName:
                print("{} - Field name found".format(fieldName))


@step('I find document id for the created "{recordType}" record')
def find_doc_id(context, recordType):
    global esRequestType
    user = context.config.get("ES_User")
    password = context.config.get("ES_Pass")
    esRequestType = GlobalVar.testParams.get('readESRequestType')
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        GlobalVar.response = requests.get(url=GlobalVar.api_dict[esRequestType + '_endPoint'],
                                          json=GlobalVar.api_dict['service_payload_' + esRequestType],
                                          auth=HTTPBasicAuth(user, password), verify=False)

        response_codes[esRequestType] = GlobalVar.response.status_code
        response_json[esRequestType] = GlobalVar.response.json()

        # validate response code
        validate_response_code(context, int(response_codes[esRequestType]), context.config.get('ES_APIResponse'))

        docId = response_json[esRequestType]['hits']['hits'][0]['_id']
        GlobalVar.docId[testCase] = {recordType: docId}

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise err


@step('Validate that the service record has no record of "{responseKey}"')
def validate_request_value(context, responseKey):
    requestsList = response_json[esRequestType]['hits']['hits'][0]['_source']['bi']['mpls']['bi-services'][
        'bi-service'][0][responseKey]
    for i in range(len(requestsList)):
        assert requestsList[i]['id'] != GlobalVar.testParams[testCase]["requestId"]


@step('Validate there is "{occurrence}" site instance under site')
def validate_site_instances(context, occurrence):
    global siteResponse
    sitesResponse = response_json[esRequestType]['hits']['hits'][0]['_source']['bi']['mpls']['bi-services'][
        'bi-service'][0]['sites']
    siteResponse = sitesResponse['site'][0]['telus-pe-ce-network-accesses']['site-network-access']
    assert len(siteResponse) == int(occurrence)


@step('Validate the "{serviceType}" service with "{resKey}" has "{availability}" value "{resValue}"')
def validate_network_access_id(context, serviceType, resKey, availability, resValue):
    if serviceType == 'base': assert siteResponse[0][resKey] == resValue
    if serviceType == 'MWR':
        if availability == 'no':
            assert len(siteResponse) == 1
        else:
            assert siteResponse[1][resKey] == resValue


@step('Validate the "{precedence}" values of "{field}"')
def validate_field_value(context, precedence, field):
    global param
    siteValue = response_json[esRequestType]['hits']['hits'][0]['_source']['request-characteristics'][
        'payload']['serviceCharacteristic'][0]['value']['site']

    if field == 'speed':
        param[field + '_' + precedence] = siteValue['telus-pe-ce-network-accesses']['site-network-access']['bearer'][
            'telus-pe-tp-info'][field]

    elif field == 'ipv4-lan-prefix':
        param[field + '_' + precedence] = siteValue['vpn-policies']['vpn-policy']['mpls-bi']['entries'][
            'telus-provider-prefixes']['filters']['filter'][field]


@step('The "{before}" and "{after}" values of the "{fieldName}" should be "{matchResult}"')
def validate_modified_values(context, before, after, fieldName, matchResult):
    print(GlobalVar.param[fieldName + '_' + before])
    print(GlobalVar.param[fieldName + '_' + after])
    if matchResult == 'same':
        assert set(GlobalVar.param[fieldName + '_' + before]) == set(GlobalVar.param[fieldName + '_' + after])
    else:
        assert set(GlobalVar.param[fieldName + '_' + before]) != set(GlobalVar.param[fieldName + '_' + after])


@step('Validate the value of "{respKey}" is "{respValue}"')
def validate_admin_state(context, respKey, respValue):
    adminState = response_json[esRequestType]['hits']['hits'][0]['_source']['bi']['mpls']['bi-services']['bi-service'][
        0]['sites']['site'][0]['telus-pe-ce-network-accesses']['site-network-access'][0]['bearer'][
        'telus-pe-tp-info']['ethernet-underlay'][respKey]
    assert adminState == respValue


@step('Validate that a "{resKey}" section "{availability}" in the callback response')
def validate_resources(context, resKey, availability):
    callbackMessageKeys = list(response_json['payloadConverted'].keys())
    for keyName in callbackMessageKeys:
        if 'not' in availability:
            assert keyName != resKey
            print("{} section is not present".format(resKey))
        else:
            if keyName == resKey:
                print("{} section is present".format(resKey))


@step('Validate the "{oldValue}" and "{newValue}" for resources are present in the callback response')
def validate_callback_values(context, oldValue, newValue):
    resources = response_json['payloadConverted']['resources']
    print("Changed resources: {}".format(len(resources)))

    for resource in resources:
        resourceName = list(resource.keys())[0]
        params = list(resource[resourceName].keys())
        for i in range(len(params)):
            if params[i] == 'oldValue':
                print("Old Value Found for {}".format(resourceName))
            elif params[i] == 'newValue':
                print("New Value Found for {}".format(resourceName))


@step('Validate the "{error_code}" is the expected value')
def validate_error_code(context, error_code):
    errorMessage = callbackInfo['payload']['errors'][0]
    mediationErrorCode = errorMessage[error_code]
    assert mediationErrorCode == int(GlobalVar.testParams.get('mediationErrorCode'))


@step('Validate that the error "{param}" in callback is correctly mapped')
def validate_code_mapping(context, param):
    if param == "code":
        orchestratorErrorCode = response_json['payloadConverted']['event']['service'][param]
        assert orchestratorErrorCode == GlobalVar.testParams.get('orchestratorErrorCode')
    elif param == "message":
        orchestratorErrorMessage = response_json['payloadConverted']['event']['service']['statusChangeReason']
        expectedErrorMessage = GlobalVar.testParams.get('orchestratorErrorMessage').strip().split(",")
        expectedErrorMessage = [item.strip() for item in expectedErrorMessage]
        assert set(orchestratorErrorMessage) == set(expectedErrorMessage)


@step('Validate the "{precedence}" values of "{fieldName}" for "{recordType}" record')
def read_prefix_value(context, precedence, fieldName, recordType):
    siteValue = response_json[esRequestType]['hits']['hits'][0]['_source']['bi']['mpls']['bi-services']['bi-service'][
        0]['sites']['site'][0]

    if fieldName == 'speed' or fieldName == 'port':
        GlobalVar.param[fieldName + '_' + precedence] = \
            siteValue['telus-pe-ce-network-accesses']['site-network-access'][
                0]['bearer']['telus-pe-tp-info']['ethernet-underlay'][fieldName]

    if fieldName == 'ipv4-lan-prefix':
        GlobalVar.param[fieldName + '_' + precedence] = siteValue['vpn-policies']['vpn-policy'][0]['entries'][
            1]['filters']['filter'][0][fieldName]

    if fieldName == 'provider-prefixes' or fieldName == 'customer-prefixes':
        entries = siteValue['vpn-policies']['vpn-policy'][0]['entries']
        for item in entries:
            if item["id"] == fieldName:
                GlobalVar.param[fieldName + '_' + precedence] = item['filters']['filter'][0]['ipv4-lan-prefix']


@step('Validate that the "{messageStatus}" message has correct error code "{errCode}"')
def validate_callback_error_code(context, messageStatus, errCode):
    actualErrorCode = response_json['payloadConverted']['event']['service']['code']
    assert actualErrorCode == errCode


@step('Validate that "{num}" request ids are returned by mediation layer')
def validate_external_reqId(context, num):
    global value
    value = response_json[esRequestType]['hits']['total']['value']
    assert value == int(num)


@step('Validate a request id is returned for "{configType}" config')
def read_external_tracker(context, configType):
    global external_requestId, index
    for i in range(value):
        displayType = response_json[esRequestType]['hits']['hits'][i]['_source']['external-request-tracker'][0][
            'request-characteristics']['request_type']
        if 'delete' in displayType.lower():
            index["current"] = i
        elif 'update' in displayType.lower():
            index["expected"] = i

    external_requestId[configType] = response_json[esRequestType]['hits']['hits'][index.get(configType)]['_source'][
        'external-request-tracker'][0]['id']


@step('Validate a callback response is returned by mock server for "{configType}" config')
def step_impl(context, configType):
    global callbackResponse
    callbackResponse[configType] = response_json[esRequestType]['hits']['hits'][index.get(configType)]['_source'][
        'external-request-tracker'][0]['callback-info']['payload']


@step('Validate the "{paramName}" value in the response for "{configType}" config')
def step_impl(context, paramName, configType):
    if paramName == 'request_id':
        assert callbackResponse[configType][paramName] == external_requestId[configType]
    else:
        assert str(callbackResponse[configType][paramName]).lower() == GlobalVar.testParams.get(
            paramName + '_responseValue_' + configType).lower()


@step('I validate the "{messageStatus}" response and format for "{configType}" config')
def step_impl(context, messageStatus, configType):
    expectedDisplayConfigResponse = GlobalVar.testParams.get(configType + '_config_response')
    schemaFileName = GlobalVar.testParams.get(configType + '_callbackSchemaFile')

    for index in range(0, len(callbacks)):
        keysList = callbacks[index]['display_config_payload'].keys()
        for key in keysList:
            if configType in key:
                assert (callbacks[index]['event']['service']['status']) == messageStatus
                assert callbacks[index]['display_config_payload'][key].lower() == expectedDisplayConfigResponse.lower()
                assert validate_schema(context, schemaFileName, GlobalVar.testComponent[0], callbacks[index])


@step("Extract current and expected config messages")
def step_impl(context):
    global callbacks
    callbacks = []
    responseList = response_json[requestType]

    # Extracting latest messages from the queue
    for index in range(0, len(responseList)):
        payloadValue = responseList[index]['payload']

        # convert extracted payload message in dictionary and store the messages with matching correlation id
        response_json['payloadConverted'] = json.loads(payloadValue)
        if response_json['payloadConverted']['correlationId'] == GlobalVar.testParams[testCase]['requestId']:
            callbacks.append(response_json['payloadConverted'])
    assert len(callbacks) == 2


@step('Validate that "{paramName}" field is not present in the response for "{configType}" config')
def step_impl(context, paramName, configType):
    dictKeys = callbackResponse[configType].keys()
    for key in dictKeys: assert key.lower() != paramName.lower()


@step("I create and assign document id for record creation")
def step_impl(context):
    if testCase not in GlobalVar.docId.keys():
        GlobalVar.docId[testCase] = {}


@step('I set api request body for "{processType}" a "{recordType}" record for "{operationsCount}" operations')
def set_requestBody(context, processType, recordType, operationsCount):
    payloadFileName = GlobalVar.testParams.get('ES_' + processType + '_' + recordType + '_requestBody')

    if payloadFileName != 'None':
        messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(),
                                                            payloadFileName)
        GlobalVar.uuid[testCase] = {}
        for i in range(int(operationsCount)):
            GlobalVar.uuid[testCase].update({i: payloadGenerator.generate_reqId(context)})

            messageBody['bi']['mpls']['bi-services']['bi-service'][0]['associated-requests'][i]['id'] = \
                GlobalVar.uuid[testCase][i]

        GlobalVar.api_dict['ES_' + processType + '_requestBody'] = messageBody

    else:
        GlobalVar.api_dict['ES_' + processType + '_requestBody'] = None


@step('I set api request body for "{processType}" a "{recordType}" record for "{operationType}"')
def set_requestBody(context, processType, recordType, operationType):
    payloadFileName = GlobalVar.testParams.get('ES_' + processType + '_' + recordType + '_' +
                                               operationType + '_requestBody')

    if payloadFileName != 'None':
        messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(),
                                                            payloadFileName)
        keyName = None
        if operationType == 'baseService' or operationType == 'deleteService':
            keyName = 0
        if operationType == 'createMwrService' or operationType == 'modifyBaseService' or \
                operationType == 'activateService':
            keyName = 1
        if operationType == 'deleteMwrService' or operationType == 'rollbackService' or \
                operationType == 'modifyActiveService':
            keyName = 2

        messageBody['id'] = GlobalVar.uuid[testCase][keyName]
        messageBody['request-characteristics']['response']['requestId'] = GlobalVar.uuid[testCase][keyName]
        if operationType == 'baseService':
            messageBody['external-request-tracker'][0]['request-characteristics']['payload']['config']['bi-service'][
                0]['associated-requests'][0]['id'] = GlobalVar.uuid[testCase][keyName]
        if operationType == 'rollbackService':
            messageBody['external-request-tracker'][0]['request-characteristics']['rollback_request_id'] = \
                GlobalVar.uuid[testCase][0]

        GlobalVar.api_dict['ES_' + processType + '_requestBody'] = messageBody

    else:
        GlobalVar.api_dict['ES_' + processType + '_requestBody'] = None


@step('I set api endpoint for "{processType}" a "{recordType}" record for "{operationType}"')
def set_endpoint(context, processType, recordType, operationType):
    endPoint = GlobalVar.api_url + GlobalVar.testParams.get('ES_' + processType + '_endpoint')

    if processType == 'create':
        randomId = ''.join(random.choices(string.digits + string.ascii_lowercase, k=20))
        if recordType not in GlobalVar.docId[testCase].keys():
            GlobalVar.docId[testCase].update({recordType: {operationType: randomId}})
            print("{} record document id : {}".format(recordType, GlobalVar.docId[testCase][recordType][operationType]))
        elif operationType not in GlobalVar.docId[testCase][recordType].keys():
            GlobalVar.docId[testCase][recordType].update({operationType: randomId})
            print("{} record document id : {}".format(recordType, GlobalVar.docId[testCase][recordType][operationType]))

    if processType == 'delete':
        print("{} record document id : {}".format(recordType, GlobalVar.docId[testCase][recordType][operationType]))

    GlobalVar.api_dict['ES_' + processType + '_endpoint'] = endPoint.replace('{doc_id}', GlobalVar.docId[
        testCase][recordType][operationType]).replace('recordType', recordType)


@step('I validate that the "{recordType}" record is "{recordResult}" in "{indexType}" index')
def validate_record(context, recordType, recordResult, indexType):
    recordCreated = response_json[ES_requestType]['result']
    assert recordCreated == recordResult
    documentId = response_json[ES_requestType]['_id']
    assert documentId == GlobalVar.docId[testCase][recordType]


@step('Validate that response has "{resKey}" as "{resValue}"')
def validate_callback_response(context, resKey, resValue):
    assert response_json['payloadConverted'][resKey].lower() == resValue.lower()


@step('Validate a callback response is returned by mock server for display rollback config')
def validate_callback(context):
    global callbackInfo
    hits = len(response_json[esRequestType]['hits']['hits'])

    i = None
    for i in range(hits):
        request_type = response_json[esRequestType]['hits']['hits'][i]['_source']['external-request-tracker'][0][
            'request-characteristics']['request_type']
        if 'delete' in request_type.lower(): break

    callbackInfo = response_json[esRequestType]['hits']['hits'][i]['_source']['external-request-tracker'][0][
        'callback-info']


@step('Validate a request id is returned by mock server for display rollback config')
def validate_external_reqId(context):
    global external_requestId
    hits = len(response_json[esRequestType]['hits']['hits'])
    i = None
    for i in range(hits):
        request_type = response_json[esRequestType]['hits']['hits'][i]['_source']['external-request-tracker'][0][
            'request-characteristics']['request_type']
        if 'delete' in request_type.lower(): break

    external_requestId['request'] = response_json[esRequestType]['hits']['hits'][i]['_source'][
        'external-request-tracker'][0]['id']
    assert len(external_requestId['request']) != 0
    print("External_Request_Tracker: {}".format(external_requestId['request']))


@step('Validate that "{paramName}" field is not present in the response')
def step_impl(context, paramName):
    dictKeys = callbackInfo.keys()
    for key in dictKeys: assert key.lower() != paramName.lower()


@step('Validate that the "{messageType}" message in callback is as expected')
def step_impl(context, messageType):
    errorMessage = response_json['payloadConverted']['event']['service']['statusChangeReason'][0]
    assert errorMessage == GlobalVar.testParams.get('orchestrator_' + messageType + '_message')


@step('I validate record format for "{recordType}" response for "{requestType}"')
def step_impl(context, recordType, requestType):
    schemaFileName = GlobalVar.testParams.get('ES_' + recordType + '_SchemaFile')
    schemaFileName = schemaFileName.format('1')
    result = validate_schema(context, schemaFileName, GlobalVar.testComponent[0], response_json[esRequestType])
    if not result:
        schemaFileName = GlobalVar.testParams.get('ES_' + recordType + '_SchemaFile')
        schemaFileName = schemaFileName.format('2')
        result = validate_schema(context, schemaFileName, GlobalVar.testComponent[0], response_json[esRequestType])
    assert result


@step('I set request query for "{recordType}" record for "{messageType}" ES message')
def set_ES_body(context, recordType, messageType):
    global esRequestType
    esRequestType = GlobalVar.testParams.get('readESRequestType')
    queryFileName = GlobalVar.testParams.get(messageType + 'ESQueryParam_' + recordType)
    messageBody = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0].lower(),
                                                        queryFileName)
    testCase = GlobalVar.testParams.get('TestCase')
    if recordType == 'request':
        messageBody['query']['match']['id'] = GlobalVar.testParams[testCase]["requestId"]

    elif recordType == 'service':
        messageBody['query']['match']['id'] = GlobalVar.testParams["serviceId"]

    GlobalVar.api_dict[recordType + '_payload_' + esRequestType] = messageBody


@step("Validate there are no unicode characters in the response")
def step_impl(context):
    resValue = response_json['payloadConverted']['event']['service']['statusChangeReason'][0]
    try:
        resValue.decode("ascii")
    except Exception as err:
        print("No unicode characters found")


@step('Validate that "{resourceEntity}" values are "{availability}" in the callback response')
def validate_callback_values(context, resourceEntity, availability):
    resources = response_json['payloadConverted']['resources']
    found = False
    for resource in resources:
        resourceName = list(resource.keys())[0]
        if resourceName == resourceEntity:
            found = True
            params = list(resource[resourceName].keys())
            for param in params:
                if param == 'oldValue':
                    print("Old Value Found for {}: {}".format(resourceName, resource[resourceName][param]))
                    print(GlobalVar.param[resourceName + '_original'])
                    if resourceName == "port":
                        assert resource[resourceName][param].lower() == GlobalVar.param[
                            resourceName + '_original'].lower()
                    else:
                        assert set(resource[resourceName][param]) == set(GlobalVar.param[resourceName + '_original'])
                if param == 'newValue':
                    print("New Value Found for {}: {}".format(resourceName, resource[resourceName][param]))
                    print(GlobalVar.param[resourceName + '_modified'])
                    if resourceName == "port":
                        assert resource[resourceName][param].lower() == GlobalVar.param[
                            resourceName + '_modified'].lower()
                    else:
                        assert resource[resourceName][param] == GlobalVar.param[resourceName + '_modified']
    if 'not' in availability:
        assert not found
    else:
        assert found


@step('I validate that request "{field}" is "{expectedValue}"')
def validate_state(context, field, expectedValue):
    actualValue = response_json[esRequestType]['hits']['hits'][0]['_source'][field]
    assert actualValue.lower() == expectedValue.lower()


@step('I "{action}" zookeeper connectivity for node validation')
def zk_connection(context, action):
    global parentPath
    hosts = context.config.get("zk_hosts")
    parentPath = GlobalVar.testParams.get(f"zk_parent_path")
    try:
        if action == "start":
            GlobalVar.zk = ZK.connect(context, hosts, parentPath)
        elif action == "stop":
            GlobalVar.zk = ZK.stop(context, GlobalVar.zk)
    except Exception as err:
        print("Error: Failed to {} connection: {}".format(action, err))
        # raise Exception(err)


@step("Validate a request id is returned by resource entity as synchronous response")
def extract_requestId(context):
    global node
    expectedId = GlobalVar.testParams[testCase]["requestId"]
    try:
        childNodes = ZK.get_children1(context, GlobalVar.zk, parentPath, node)
        for child in childNodes:
            actualId = childNodes[child]["nb_request_payload"]["id"]
            if actualId == expectedId:
                external_requestId["resourceEntity"] = node = child
                print("Node {} found for request id {}".format(external_requestId["resourceEntity"], expectedId))
                break
        print("External_Request_Tracker_Resource_Entity: {}".format(external_requestId['resourceEntity']))

    except Exception as err:
        print("Error: {}".format(err))
        # raise Exception(err)


@step('I validate that a "{node_name}" is "{nodeState}" in zookeeper instance')
def validate_node(context, node_name, nodeState):
    eventType = f"__{GlobalVar.eventType}"
    node_Event = GlobalVar.node + eventType
    try:
        nodeStatus = ZK.get_node(context, GlobalVar.zk, parentPath, node_Event)
        if nodeState == "created":
            assert nodeStatus
        else:
            assert not nodeStatus

    except Exception as err:
        print(Exception(err))
        # raise Exception(err)
