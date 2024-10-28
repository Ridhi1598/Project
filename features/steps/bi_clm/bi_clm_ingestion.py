from behave import *
from features.steps.bi.bi_controller import *
from features.steps.bi_clm.bi_clm_uiFunctional import *
from common.util.api_test import ApiTest

# declared variables
testCase = None
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
Id = {}


# end of declared variables

@step("I read test data for e2e test case")
def step_impl(context):
    testCase = context.scenario.name.split(':')[0]
    GlobalVar.testParams = context.csvRead[int(testCase.split('_')[1]) - 1]
    print(testCase)
    GlobalVar.test_case = int(testCase.split('_')[1])
    GlobalVar.testParams[GlobalVar.test_case] = {}


@step("I read test data for testcase")
def step_impl(context):
    global testCase
    testCase = context.feature.filename.split('_')[3]
    if "ui" in GlobalVar.testComponent[0].lower() or "e2e" in GlobalVar.testComponent[0].lower():
        GlobalVar.testParams = context.csvRead[int(testCase) - 1]
    else:
        GlobalVar.testParams = context.csvReadAPI[int(testCase) - 1]
    GlobalVar.test_case = testCase
    GlobalVar.testParams[GlobalVar.test_case] = {}
    if "orchestrator" in GlobalVar.testComponent[0].lower():
        GlobalVar.testParams["baseRequestId"] = None
        GlobalVar.testParams["requestId"] = None
        GlobalVar.testParams["mwrRequestId"] = None
    if "evpn" in GlobalVar.testComponent[0].lower():
        GlobalVar.testParams["baseRequestId"] = {}
        GlobalVar.testParams["zk_timer_node"] = []
        GlobalVar.testParams["zk_deleted_node"] = []
    if "bng-controller" in GlobalVar.testComponent[0].lower():
        GlobalVar.testParams["baseRequestId"] = None


@step('I set "{apiType}" url')
def set_url(context, apiType, appName=''):
    global testCase
    if len(appName) != 0:
        url = ''.join([appName, "_", apiType, "_", sys.argv[2]])
    else:
        url = ''.join([apiType, "_", sys.argv[2]])
    GlobalVar.api_url = context.config.get(url)
    testCase = GlobalVar.test_case
    return GlobalVar.api_url

@step('I set "{apiType}" url for "{app}"')
def set_consumer_rmq_url(context, apiType, app):
    url = ''.join([app, "_", apiType, "_", sys.argv[2]])
    GlobalVar.api_url = context.config.get(url)
    return GlobalVar.api_url

@step('I Set "{component}" api endpoint')
def set_endPoint(context, component):
    global serviceId, mwrId
    serviceId = GlobalVar.testParams.get('serviceId')
    mwrId = GlobalVar.testParams.get('mwrId')
    GlobalVar.requestType = GlobalVar.testParams.get('RequestType')
    endpointFormat = GlobalVar.testParams.get('EndPoint')
    endpoint = ''

    if 'services' in endpointFormat:
        if 'version' in endpointFormat:
            endpoint = GlobalVar.testParams.get('EndPoint').format(serviceId, GlobalVar.version)
        else:
            endpoint = GlobalVar.testParams.get('EndPoint').format(serviceId)
    elif 'requests' in endpointFormat:
        endpoint = GlobalVar.testParams.get('EndPoint').format(GlobalVar.requestId)
    elif "mwr" in endpointFormat:
        endpoint = GlobalVar.testParams.get('EndPoint').format(serviceId, mwrId)
    elif "customer" in endpointFormat:
        endpoint = GlobalVar.testParams.get('EndPoint').format(GlobalVar.customerId)
    else:
        endpoint = GlobalVar.testParams.get('EndPoint').format(serviceId)
    GlobalVar.api_dict[f'{GlobalVar.requestType}_URL'] = ''.join([GlobalVar.api_url, endpoint])
    print("{} {} request URL: {}".format(component.title(), GlobalVar.requestType.lower(),
                                         GlobalVar.api_dict[f'{GlobalVar.requestType}_URL']))


@step('I Set "{component}" api request body')
def set_request_body(context, component):
    url = (GlobalVar.api_dict[f'{GlobalVar.requestType}_URL']).split('/')
    GlobalVar.eventType = GlobalVar.testParams.get('event')
    filename = GlobalVar.testParams.get('RequestBody')
    if not bool(filename):
        GlobalVar.api_dict['payload'] = None

    else:
        GlobalVar.api_dict['payload'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], filename)
        if "update" in url or "execute" in url:
            GlobalVar.api_dict['payload'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], filename)

        elif "api-" not in GlobalVar.testComponent[0].lower():
            if GlobalVar.testParams.get("RequestBodyType") != "static":
                if GlobalVar.testParams.get("RequestBodyType") == "customer_id":
                    GlobalVar.api_dict['payload']["id"] = GlobalVar.customerId
                else:
                    print("Update service id supported")
                    GlobalVar.api_dict['payload'] = payloadGenerator.update_serviceId(context, GlobalVar.api_dict['payload'], GlobalVar.testParams)
    print(json.dumps(GlobalVar.api_dict['payload'], indent=4))


@step('I Set query parameters for "{component}" request for "{precedence}"')
def set_action_param(context, component, precedence, value=''):
    global queryStatus
    queryStatus = precedence
    queryParamsFile = GlobalVar.testParams.get(f'QueryParams_{precedence}').format(value)
    if not bool(queryParamsFile):
        GlobalVar.api_dict['request_params'] = None
    else:
        GlobalVar.api_dict['request_params'] = payloadGenerator.load_payload_message(
            context, GlobalVar.testComponent[0], queryParamsFile)
    # print(json.dumps(GlobalVar.api_dict['request_params'], indent=4))


@when('I Send HTTP request for "{component}"')
def step_impl(context, component):
    global response_json
    urllib3.disable_warnings(InsecureRequestWarning)
    GlobalVar.response = ApiTest.sendRequestjson(context, GlobalVar.requestType,
                                                 GlobalVar.api_dict[f'{GlobalVar.requestType}_URL'],
                                                 GlobalVar.api_dict['request_header'],
                                                 GlobalVar.api_dict['request_params'], GlobalVar.api_dict['payload'])
    response_json[GlobalVar.requestType] = GlobalVar.response.json()

    # Validate response
    if queryStatus != 'after':
        responseCodeVar = GlobalVar.testParams.get('ResponseCode')
        validate_response_code(context, int(GlobalVar.response.status_code), int(responseCodeVar))


@step('I validate the expected response schema')
def step_impl(context):
    schema_file = GlobalVar.testParams.get("SchemaFile")
    assert validate_schema(context, schema_file, GlobalVar.testComponent[0], response_json[GlobalVar.requestType])


@step('I validate response should have "{keyName}" as expected response')
def validate_response(context, keyName, templist=[]):
    templist = []
    print(GlobalVar.response.json())
    print(GlobalVar.response.json()[keyName])
    if isinstance(GlobalVar.response.json()[keyName], list):
        templist.append(GlobalVar.testParams.get(keyName))
        assert (GlobalVar.response.json()[keyName]) == templist
    else:
        assert GlobalVar.response.json()[keyName] == GlobalVar.testParams.get(keyName)


def update_rmq_payload(context, payload, message, serviceID, requestId, event):
    # Update correlation Id in payload
    payload['payload'] = (payload['payload']).replace('requestId', requestId)

    # generate eventId
    randomId = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    payload['payload'] = (payload['payload']).replace('randomId', randomId)

    # update event
    payload['payload'] = (payload['payload']).replace('operation', event.upper())

    # update time
    payload['payload'] = (payload['payload']).replace('currentTime', str(datetime.datetime.utcnow()))

    # update service Id in payload
    payload['payload'] = (payload['payload']).replace('serviceId', serviceID)

    if "mwr" in message:
        # update mwr Id in payload
        payload['payload'] = (payload['payload']).replace('mwrId', GlobalVar.testParams.get("mwrId"))

        # update mwr Req Id in payload
        payload['payload'] = (payload['payload']).replace('mwrReqId', payloadGenerator.generate_reqId(context))
    return payload


@step('Mock "{message}" response to "{entity}" "{queueName}" queue')
def mock_response(context, message, entity, queueName):
    global filepath
    RMQRequestType = GlobalVar.testParams.get(f'{entity}_RequestType')
    Endpoint = GlobalVar.testParams.get(f'{entity}_Publish_EndPoint')
    url = set_url(context, entity) + Endpoint
    fileName = GlobalVar.testParams.get(f'{entity}_Publish_RequestBody').format(message)
    # read and update payload with the request Id/service Id
    if "ui" in GlobalVar.testComponent[0]:
        payloadMessage = payloadGenerator.load_payload_message(context, 'ingestion', fileName)
    else:
        payloadMessage = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], fileName)

    payloadMessage['routing_key'] = queueName
    GlobalVar.api_dict['request_bodies'] = update_rmq_payload(context, payloadMessage, message,
                                                              GlobalVar.testParams.get("serviceId"),
                                                              GlobalVar.requestId, GlobalVar.testParams.get("event"))

    # Send HTTP request and validate response
    GlobalVar.response = ApiTest.sendRequestAuth(context, RMQRequestType, url, GlobalVar.api_dict['request_bodies'],
                                                 context.config.get(f'{entity}_User'),
                                                 context.config.get(f'{entity}_Pass'))

    assert ApiTest.validateResponseCode(context, GlobalVar.response,
                                        int(GlobalVar.testParams.get(f'{entity}_ResponseCode')))
    assert GlobalVar.response.json().get("routed")


@step('I extract response value for "{responseKey}"')
def extract_response_value(context, responseKey):
    if "display" not in GlobalVar.scenario:
        if "execute" not in GlobalVar.scenario:
            if "error" not in responseKey:
                GlobalVar.requestId = response_json[GlobalVar.requestType]['requestId']
                GlobalVar.node = GlobalVar.requestId
                GlobalVar.reqId = GlobalVar.requestId
            else:
                GlobalVar.reason = response_json[GlobalVar.requestType]["reason"]
            if GlobalVar.scenario == "update" or GlobalVar.scenario == "rollback" or GlobalVar.scenario == "create" or GlobalVar.scenario == "delete":
                context.scenario.skip(reason="no further action required for update scenario")


@step('I validate the "{messageType}" response format for "{responseType}" message')
def validate_callback(context, messageType, responseType):
    responseValue = GlobalVar.response.json()
    schemaFile = (GlobalVar.testParams.get(f'{messageType}_schemaFile').format(responseType))
    schemaResponse = ApiTest.validateResponseSchema(context, responseValue, schemaFile, GlobalVar.testComponent[0])
    assert schemaResponse


@step('I send request to fetch "{messageType}" response for "{scenario}"')
def fetch_callbacks(context, messageType, scenario):
    reqType = GlobalVar.testParams.get(f'{messageType}_RequestType')
    reqEndpoint = GlobalVar.testParams.get(f'{messageType}_EndPoint')
    endpoint = ApiTest.setEndpoint(context, GlobalVar.api_url, reqEndpoint.format(GlobalVar.requestId))
    param = ApiTest.setParams(context, None, GlobalVar.testComponent[0])
    GlobalVar.response = ApiTest.sendRequest(context, reqType, endpoint, param, None)
    assert ApiTest.validateResponseCode(context, GlobalVar.response,
                                        GlobalVar.testParams.get(f'{messageType}_ResponseCode_{scenario}'))


@step('I send request to "{action}" "{messageType}" record from "{server}"')
def callback_records(context, action, messageType, server):
    GlobalVar.api_url = set_url(context, server)
    reqType = GlobalVar.testParams.get(f'{action}_{messageType}_RequestType')
    reqEndpoint = GlobalVar.testParams.get(f'{action}_{messageType}_EndPoint')
    queryParam = GlobalVar.api_dict['request_params']

    if action == 'fetch':
        endpoint = ApiTest.setEndpoint(context, GlobalVar.api_url, reqEndpoint.format(GlobalVar.requestId))
    else:
        endpoint = ApiTest.setEndpoint(context, GlobalVar.api_url, reqEndpoint)
        queryParam = None
    print(endpoint)

    GlobalVar.response = ApiTest.sendRequest(context, reqType, endpoint, requestParams=queryParam, requestHeaders=None)
    print(GlobalVar.response.text)
    print(GlobalVar.response.status_code)
    print(GlobalVar.testParams.get(f'{action}_{messageType}_ResponseCode'))

    assert ApiTest.validateResponseCode(context, GlobalVar.response,
                                        GlobalVar.testParams.get(f'{action}_{messageType}_ResponseCode'))


@step('I validate that the response has "{fieldName}" as "{expectedValue}"')
def validate_status(context, fieldName, expectedValue):
    assert GlobalVar.response.json()[fieldName] == expectedValue


@step('Validate that the callback info has expected "{param}" value')
def assert_res_values(context, param):
    if param == "correlationId":
        assert GlobalVar.response.json()[param] == GlobalVar.requestId

    if param == "status" or param == "code":
        assert GlobalVar.response.json()["event"]["service"][param] == GlobalVar.testParams[f"expected_{param}"]


@step('Validate that response is sorted in "{sortingOrder}" order according to "{requestTimestamp}"')
def assert_sorting_order(context, sortingOrder, requestTimestamp):
    global recordLength, serviceIdList
    recordLength = len(response_json[GlobalVar.testParams.get('RequestType')]['records'])
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


@step('Verify that response has correct values against each key')
def validate_response(context):
    testFile = GlobalVar.testParams.get('responseDataFile')
    data = payloadGenerator.load_schema_message(context, GlobalVar.testComponent[0], 'testData/{}'.format(testFile))
    testData = json.dumps(data, sort_keys=True)
    responseData = json.dumps(response_json[GlobalVar.requestType], sort_keys=True)
    assert testData == responseData
    assert data == response_json[GlobalVar.requestType]


@step('Validate the "{fieldName}" in response is not a null value')
def validate_field_not_null(context, fieldName):
    assert response_json[GlobalVar.requestType]['Site Information']['SAP'][fieldName] is not None


@step('Validate that response is sorted in "{sortingOrder}" order for "{matchType}" match of "{searchTerm}"')
def assert_order(context, sortingOrder, matchType, searchTerm):
    global recordLength
    searchText = GlobalVar.api_dict['request_params']["search_query['{}']".format(searchTerm)]
    recordLength = len(response_json[GlobalVar.requestType]['records'])
    timeStampList = []
    for i in range(recordLength):
        resValue = response_json[GlobalVar.requestType]['records'][i][searchTerm]
        if 'exact' in matchType:
            assert resValue == searchText
        elif 'partial' in matchType:
            assert searchText in resValue

        time = response_json[GlobalVar.requestType]['records'][i]['request-timestamp']
        timeStampList.append(time)

    for i in range(len(timeStampList) - 1):
        if sortingOrder == 'descending':
            assert timeStampList[i] >= timeStampList[i + 1]
        elif sortingOrder == 'ascending':
            assert timeStampList[i] <= timeStampList[i + 1]


@step('Validate that only records with a "{matchType}" match for "{searchTerm}" are returned')
def validate_serviceId(context, matchType, searchTerm):
    searchResult = GlobalVar.api_dict['request_params']["search_query['{}']".format(searchTerm)]
    recordLength = len(response_json[GlobalVar.requestType]['records'])
    for i in range(recordLength):
        if 'exact' in matchType:
            resValue = response_json[GlobalVar.requestType]['records'][i][searchTerm].lower()
            assert resValue == searchResult.lower()
        elif 'partial' in matchType:
            assert searchResult.lower() in resValue


@step('I validate the response body for expected "{status}" and "{reason}"')
def validate_response(context, status, reason):
    assert GlobalVar.testParams.get(status) == response_json[GlobalVar.requestType][status]
    assert GlobalVar.testParams.get(reason) == response_json[GlobalVar.requestType][reason][0]


@step('Validate that a service record for expected "{idVal}" and "{stateVal}"')
def validate_service_state(context, idVal, stateVal):
    if response_json[ESRequestType]['found']:
        assert response_json[ESRequestType]['_source'][idVal] == GlobalVar.testParams.get("serviceId")
        try:
            assert str(response_json[ESRequestType]['_source']['state']) == GlobalVar.testParams.get(stateVal)
        except:
            assert str(response_json[ESRequestType]['_source']['state']) == GlobalVar.testParams.get(f"{stateVal}2")
    else:
        assert response_json[ESRequestType]['_id'] == serviceId
        print("Service {} does not Exist".format(serviceId))


@step('Validate that all records are sorted in "{sortingOrder}" order according to "{requestTimestamp}"')
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


@step('Validate all records have request "{resKey}" as "{resValue}"')
def validate_response_state(context, resKey, resValue):
    for i in range(recordLength):
        assert response_json[GlobalVar.requestType]['records'][i][resKey] == resValue


@step('Validate no duplicate records are returned for "{resKey}"')
def validate_no_duplicacy(context, resKey):
    serviceIdList = []
    for i in range(recordLength):
        service = response_json[GlobalVar.requestType]['records'][i][resKey]
        serviceIdList.append(service)
    serviceIdSet = set(serviceIdList)
    assert len(serviceIdSet) == len(serviceIdList)


@step('I validate the response body should have "{response_key}" as "{response_value}"')
def validate_response_value(context, response_key, response_value):
    try:
        assert response_json[GlobalVar.requestType]['event']['service'][response_key] == response_value
    except:
        assert response_json[GlobalVar.requestType][response_key] == response_value


@step('I extract the response value for expected "{responseKey}"')
def extract_response_value(context, responseKey):
    GlobalVar.requestId = response_json[GlobalVar.requestType]['requestId']
    GlobalVar.request_ID[GlobalVar.requestType] = GlobalVar.requestId
    GlobalVar.reqId = GlobalVar.requestId


@step('Validate that the new request id is returned')
def validate_new_request_id(context):
    GlobalVar.request_ID['PUT'] = response_json[GlobalVar.requestType]['requestId']
    assert GlobalVar.requestId != GlobalVar.request_ID['PUT']
    GlobalVar.reqId = GlobalVar.request_ID['PUT']


@step('I validate the response body should have "{response_key}" as expected response')
def validate_response_(context, response_key):
    try:
        assert response_json[GlobalVar.requestType]['event']['service'][response_key] == GlobalVar.testParams.get(
            response_key)
    except:
        assert response_json[GlobalVar.requestType][response_key] == GlobalVar.testParams.get(response_key)


@step('Validate service record for expected "{in_progressVal}" state')
def validate_in_progress_state(context, in_progressVal):
    assert str(response_json[ESRequestType]['_source']['in-progress']).lower() == (
        GlobalVar.testParams.get(in_progressVal)).lower()


@step('I extract response value for service version')
def extract_response_value(context):
    searchId = None
    recordType = 'service'
    if recordType == 'request':
        searchId = GlobalVar.requestId
    elif recordType == 'service':
        searchId = GlobalVar.testParams.get('serviceId')
        recordType = 'service'
    url = set_API_type(context, 'ES') + GlobalVar.testParams.get('ES_{}_EndPoint'.format(recordType)) + searchId
    ESRequestType = GlobalVar.testParams.get('ESRequestType')
    print("ES {} URL: {}".format(recordType.upper(), url))
    auth = context.config.get('ES_basicAuth')
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.request(method=ESRequestType, url=url,
                                    auth=HTTPBasicAuth(context.config.get('ES_User'), context.config.get('ES_Pass')),
                                    verify=False)
        response_codes[ESRequestType] = response.status_code
        responsejson = response.json()
        validate_response_code(context, int(response_codes[ESRequestType]),
                               int(GlobalVar.testParams.get('ES_{}_ResponseCode'.format(recordType))))
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    GlobalVar.version = responsejson["_source"]["associated-versions"][0]['version']
    GlobalVar.requestId = responsejson["_source"]["associated-versions"][0]['request-id']


@step('I Validate that the syncback response has expected transactionId')
def validate_id(context):
    TransactionId = GlobalVar.response.json()['event']['orderstatusnotification'][0]['characteristicvalue'][2]['value']
    assert GlobalVar.requestId in TransactionId


@step('Rollback the update request for processing')
def rollback_ingestion_request(context):
    # generate access token and set header
    access_token = generate_access_token(context)
    set_header_request(context, 'Authorization', access_token)

    # generate url for the request
    url_Execute = 'executeAPIURL_' + sys.argv[2]
    GlobalVar.api_dict['executeURL'] = context.config.get(url_Execute).format(GlobalVar.requestId)
    print("Execute API URL: ", GlobalVar.api_dict['executeURL'])

    # set request body for execute api
    payloadFile = GlobalVar.testParams.get('executePayload')
    GlobalVar.api_dict['executePayload'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0],
                                                                                 payloadFile)
    # send API Request for execution
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=GlobalVar.api_dict['executeURL'], headers=GlobalVar.api_dict.get("request_header"),
                                 json=GlobalVar.api_dict['executePayload'], verify=False)
        # Extracting Response from Execute API
        response_codes['POST'] = response.status_code
        response_json['POST'] = response.json()

        # Validate Response Code
        validate_response_code(context, int(response_codes['POST']), context.config.get('executeAPIResponse'))

        # extract request execution status from the response
        executeStatus = response_json['POST']['status']
        print('BI Service Request Execute Status: ', executeStatus)
        assert executeStatus == 'success'

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I validate the service record for expected "{occurrence}" "{field}" value')
def validate_in_progress_state(context, occurrence, field):
    try:
        assert str(GlobalVar.response.json()['_source'][field]).lower() == str(
            GlobalVar.testParams.get(f'{field}_{occurrence}')).lower()
    except:
        assert str(GlobalVar.response.json()['_source'][field]).lower() == str(
            GlobalVar.testParams.get(f'{field}2_{occurrence}')).lower()


@step('I send request to "{action}" a "{recordType}" record in "{entity}" "{indexType}" record')
def action_record_status(context, action, recordType, entity, indexType):
    global Id
    # read request method
    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}_{action}_requestType')

    # read and update request body
    payloadFile = GlobalVar.testParams.get(f'{entity}_{action}_{recordType}_requestBody')
    if bool(payloadFile):
        GlobalVar.api_dict['request_bodies'] = ApiTest.setBody(context, payloadFile, GlobalVar.testComponent[0].lower())
        # set service Id
        if indexType.lower() == "service":
            Id[recordType] = GlobalVar.api_dict['request_bodies']["id"]

            versions = GlobalVar.api_dict['request_bodies']['associated-versions']
            for version in versions:
                if version["request-type"].lower() == "create_service":
                    version["request-id"] = GlobalVar.uuid[0]
                    GlobalVar.requestId = version["request-id"]

        # set request Id
        if indexType.lower() == "request":
            if recordType.lower() == "baseservice":
                Id[recordType] = GlobalVar.uuid[0]
            if recordType.lower() == "updateservice":
                Id[recordType] = GlobalVar.uuid[1]
            if recordType.lower() == "mwrservice":
                Id[recordType] = GlobalVar.uuid[1]

            GlobalVar.api_dict['request_bodies']['id'] = Id[recordType]
            GlobalVar.api_dict['request_bodies']['request-characteristics']['response']['requestId'] = Id[recordType]
            if GlobalVar.api_dict['request_bodies']['callback-info'] is not None:
                if GlobalVar.api_dict['request_bodies']['callback-info']['response'] is not None:
                    GlobalVar.api_dict['request_bodies']['callback-info']['response']['correlationId'] = Id[recordType]

    else:
        GlobalVar.api_dict['request_bodies'] = None

    # read and update request endpoint
    reqURL = ApiTest.setEndpoint(context, set_url(context, entity), GlobalVar.testParams.get(
        f'{entity}_{action}_endpoint').format(indexType, Id[recordType]))

    # send request and store response
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, reqURL, GlobalVar.api_dict[
        'request_bodies'], context.config.get(f"{entity}_User"), context.config.get(f"{entity}_Pass"))

    # validate response code
    if indexType.lower() != "service":
        assert ApiTest.validateResponseCode(context, GlobalVar.response,
                                            GlobalVar.testParams.get(f'{entity}_{action}_responseCode'))


@step('I create "{num}" document id for request record creation')
def step_impl(context, num):
    for i in range(int(num)):
        GlobalVar.uuid[i] = payloadGenerator.generate_reqId(context)


@step('I Send "{operation}" request for "{component}"')
def step_impl(context, operation, component):
    global response_json
    set_url(context, component, appName='')
    if bool(GlobalVar.testParams.get("Authorization")):
        set_controller_headers(context, "Content", "Authorization")
    else:
        GlobalVar.api_dict['request_header'] = None
    set_endPoint(context, component)
    set_request_body(context, component)
    set_action_param(context, component, "before", value='')

    # send request
    GlobalVar.response = ApiTest.sendRequestjson(context, GlobalVar.requestType,
                                                 GlobalVar.api_dict[f'{GlobalVar.requestType}_URL'],
                                                 GlobalVar.api_dict['request_header'],
                                                 GlobalVar.api_dict['request_params'], GlobalVar.api_dict['payload'])
    print(GlobalVar.response.request.url)
    print(GlobalVar.response.status_code)
    print(GlobalVar.response.text)

    # validate response schema and status code
    assert ApiTest.validateResponseCode(context, GlobalVar.response, GlobalVar.testParams.get('ResponseCode'))

    # validate response schema
    schemaFile = GlobalVar.testParams.get("SchemaFile")
    assert ApiTest.validateResponseSchema(context, GlobalVar.response, schemaFile, GlobalVar.testComponent[0])

    # convert and store response in json object
    response_json[GlobalVar.requestType] = GlobalVar.response.json()

    if queryStatus != 'after':
        responseCodeVar = GlobalVar.testParams.get('ResponseCode')
        validate_response_code(context, int(GlobalVar.response.status_code), int(responseCodeVar))
