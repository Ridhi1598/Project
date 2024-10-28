import socket
from behave import given, when, then, step
from features.steps.bi.bi_restApis import *
from features.steps.api_steps_general import *
from features.steps.ui_steps_general import page_title_validation, change_currentPage
from features.steps.globalVar import GlobalVar
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from features.steps.l3vpn.l3vpn_restAPIs import *
from requests.auth import HTTPBasicAuth
from requests import HTTPError


@step('I set api endpoint "{endpoint}" for "{requestType}" for IE')
def rmq_endpoint(context, endpoint, requestType):
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = set_endpoint_for_L3VPN(context, requestType, endpoint)
    # print(GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])


@step('I Set "{requestType}" api endpoint for "{endpoint}" for L3VPN')
def set_endpoint_for_L3VPN(context, requestType, endpoint):
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = GlobalVar.api_url + endpoint
    return GlobalVar.api_dict['api_endpoint_' + requestType + '_url']


@step('I set data values against "{scenario}" for Ingestion Engine')
def set_params(context, scenario):
    global testCase
    if 'testCase' in scenario:
        testCase = (scenario.split('_'))[1]
        GlobalVar.testParams = context.csvReadAPI[int(testCase)-1]


@step('I Set headers "{header_1}" and "{header_2}" for IE')
def set_controller_headers(context, header_1, header_2):
    header_1_Value = GlobalVar.testParams.get(header_1)
    header_2_Value = GlobalVar.testParams.get(header_2)
    set_header_request_l3vpn(context, header_1, header_1_Value)
    set_header_request_l3vpn(context, header_2, header_2_Value)


@step('I Set api endpoint and request Body for IE')
def set_endpoint_and_body(context):
    global requestType
    global serviceId
    serviceId = GlobalVar.testParams.get('serviceID')
    request_id = GlobalVar.testParams.get('request_id') #this step will execute only for Monitor request

    requestType = GlobalVar.testParams.get('IERequestType')
    endpoint = GlobalVar.testParams.get('IEEndPoint')
    api_url = GlobalVar.api_url

    # Set API endpoint
    if endpoint == '/l3vpn/svc/v1/service':
        api_endpoints[requestType + '_URL'] = api_url + endpoint

    elif endpoint == '/l3vpn/svc/v1/service/{service_id}':
        api_endpoints[requestType + '_URL'] = api_url + endpoint.replace('{service_id}', serviceId)

    elif endpoint == '/l3vpn/svc/v1/request/{request_Id}':
        api_endpoints[requestType + '_URL'] = api_url + endpoint.replace('{request_Id}', request_id)

    # store the URL in the global dictionary api_dict
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = api_endpoints[requestType + '_URL']
    # print("Endpoint: ", GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])

    # Set request Body
    filename = GlobalVar.testParams.get('IERequestBody')
    if filename == 'None':
        pass
    else:
        rootPath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) \
                   + '/resources/payload/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() + '/' + filename
        GlobalVar.api_dict['payload'] = json.load(open(rootPath))


@step('I Set query parameters for Ingestion engine request')
def set_query_params_IE(context):
    data = {}
    data = {'callback_url': GlobalVar.webhookServer}
    GlobalVar.api_dict['request_params'] = data


@step('I Send HTTP request for IE')
def send_HTTP_request_controller(context):
    # global requestId
    print("Sending ", requestType, " request for Ingestion Engine")
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        if requestType == 'POST':
            response = requests.post(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                     headers=GlobalVar.api_dict.get("request_header"),
                                     json=GlobalVar.api_dict.get("payload"),
                                     params=GlobalVar.api_dict['request_params'],
                                     verify=False)

        if requestType == 'PUT':
            response = requests.put(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                    headers=GlobalVar.api_dict.get("request_header"),
                                    params=GlobalVar.api_dict['request_params'],
                                    json=GlobalVar.api_dict.get("payload"),
                                    verify=False)

        if requestType == 'DELETE':
            response = requests.delete(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                       headers=GlobalVar.api_dict.get("request_header"),
                                       params=GlobalVar.api_dict['request_params'],
                                       verify=False)

        if requestType == 'GET':
            response = requests.get(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                    headers=GlobalVar.api_dict.get("request_header"),
                                    params=GlobalVar.api_dict['request_params'],
                                    verify=False)

        response_codes[requestType] = response.status_code
        response_json[requestType] = response.json()
        print("Response for", requestType, ":", response_json[requestType])

        # Validate response code

        responseCodeVar = GlobalVar.testParams.get('ResponseCode')
        validate_response_code(context, int(response_codes[requestType]), int(responseCodeVar))

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I validate the response schema for IE')
def step_impl(context):
    schema_file = GlobalVar.testParams.get("SchemaFile")
    schema_file_name = os.getcwd() + '/resources/schema/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() \
                       + '/' + schema_file
    # print(GlobalVar.testParams.get("IERequestType"))
    result = validate_schema(context, schema_file_name, response_json[GlobalVar.testParams.get("IERequestType")])
    assert result == True


def validate_schema(context, schema_file_name, response):
    with open(schema_file_name, "r") as read_file:
        data = read_file.read()
        schema = json.loads(data)
        try:
            validate(instance=response, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            print(err)
            return False


@step('I validate response body should have "{response_key}" as "{response_value}" for IE')
def validate_response_value(context, response_key, response_value):
    assert response_json[requestType][response_key] == response_value


@step('I validate response body for expected result of "{status}" and "{reason}" for IE')
def validate_response(context, status, reason):
    assert GlobalVar.testParams.get('status') == response_json[requestType][status]
    assert GlobalVar.testParams.get('reason') == response_json[requestType][reason]


@step('I validate response body for expected result of failed Request')
def validation_monitor_api(context):
    assert GlobalVar.testParams.get('reason') == response_json[requestType]['message']


@step('I validate response body for expected "{status}" and "{reason}" for IE')
def validate_response(context, status, reason):
    assert GlobalVar.testParams.get('status') == response_json[requestType][status]
    assert GlobalVar.testParams.get('reason') == response_json[requestType][reason][0]


@step('I extract "{responseKey}" from the expected response')
def extract_response_value(context, responseKey):
    # global requestId
    GlobalVar.requestId = response_json[requestType]['requestId']
    GlobalVar.request_ID[requestType] = GlobalVar.requestId
    GlobalVar.reqId = GlobalVar.requestId

@step('I validate that a "{recordType}" record is found in "{indexType}" index for IE')
def validate_ElasticSerach_record(context, recordType, indexType):
    id = None
    if recordType == 'request':
        id = GlobalVar.reqId
    elif recordType == 'service':
        id = serviceId

    url_RecordType = 'l3vpn_' + recordType + '_ES_' + sys.argv[2]
    url = context.config.get(url_RecordType) + id

    user = context.config.get('ES_User')
    password = context.config.get('ES_Pass')

    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url=url, auth=HTTPBasicAuth(user, password),
                                verify=False)
        response_codes['GET'] = response.status_code
        response_json['GET'] = response.json()

        validate_response_code(context, int(response_codes['GET']), context.config.get('ES_APIResponse'))

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I validate "{recordType}" record format')
def validate_record_format(context, recordType):
    schema_file = GlobalVar.testParams.get('ES_' + recordType + '_SchemaFile')
    schema_file_name = os.getcwd() + '/resources/schema/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() \
                       + '/' + schema_file
    result = validate_schema(context, schema_file_name, response_json['GET'])
    assert result == True


@step('I validate that the request "{stateName}" is "{stateStatus}"')
def validate_request_state(context, stateName, stateStatus):
    stateNameValue = response_json['GET']['_source'][stateName]
    assert stateNameValue.lower() == stateStatus.lower()


@step('I validate the service record for expected "{idVal}" and "{stateVal}"')
def validate_service_state(context, idVal, stateVal):
    if response_json['GET']['found']:
        assert response_json['GET']['_source'][idVal] == serviceId
        try:
            assert str(response_json['GET']['_source']['state']) == GlobalVar.testParams.get(stateVal)
        except Exception as e:
            print(e)
    else:
        assert response_json['GET']['_id'] == serviceId
        print("Service {} does not Exist".format(serviceId))

    # assert response_json['GET']['_id'] == serviceId
    # print(str(response_json['GET']['found']).lower())
    # print(str(GlobalVar.testParams.get(stateVal)).lower())
    # assert str(response_json['GET']['found']).lower() == str(GlobalVar.testParams.get(stateVal)).lower()


@step('I validate the service record for expected "{in_progressVal}" state')
def validate_in_progress_state(context, in_progressVal):
    assert str(response_json['GET']['_source']['in_progress']).lower() == (GlobalVar.testParams.get(in_progressVal)).lower()


@step('Validate that the "{messageType}" message is published to RMQ "{queueName}" queue for IE')
def validate_request_message(context, messageType, queueName):
    time.sleep(5)
    url = context.config.get('l3vpn_RMQ_' + sys.argv[2]) + 'api/queues/%2F/' + queueName + '/get'
    print("RabbitMQ_URL: ", url)
    filepath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + \
               '/resources/payload/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() + \
               '/rmq_get_message.json'
    GlobalVar.api_dict['request_bodies'] = json.load(open(filepath))
    auth = context.config.get('RMQ_basicAuth_' + sys.argv[2])
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=url, json=GlobalVar.api_dict['request_bodies'],
                                 auth=HTTPBasicAuth(auth, auth), verify=False)
        response_codes['POST'] = response.status_code
        response_json['POST'] = response.json()
        validate_response_code(context, int(response_codes['POST']), context.config.get('RMQ_APIResponse'))

        # Messages in the queue are returned in a list
        responseList = response_json['POST']
        responseLen = len(responseList)

        # Extracting latest message from the queue
        index = 0
        for i in range(0, responseLen):
            if responseList[i]['message_count'] == 0:
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

        # Validate portal rollback message
        if messageType == 'rollback-portal':
            assert payloadConverted['id'] == GlobalVar.request_ID[requestType]
            assert payloadConverted['current-request-id'] == GlobalVar.reqId


    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')


@step('Mock "{message}" response to be published to RMQ "{queueName}" queue for IE')
def mock_response(context, message, queueName):
    global filepath
    time.sleep(5)
    url = context.config.get('l3vpn_RMQ_' + sys.argv[2]) + 'api/exchanges/%2F/amq.default/publish'
    print("RabbitMQ_URL: ", url)
    requestType = GlobalVar.testParams['IERequestType']
    filepath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + \
               '/resources/payload/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() + \
               '/rmq_'+requestType.lower()+'_' + message + '_message.json'

    # read and update payload with the request Id
    updatedPayload = update_payload(json.load(open(filepath)))
    GlobalVar.api_dict['request_bodies'] = updatedPayload
    auth = context.config.get('RMQ_basicAuth_' + sys.argv[2])
    print("Mock method:")
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=url, json=GlobalVar.api_dict['request_bodies'],
                                 auth=HTTPBasicAuth(auth, auth), verify=False)
        response_codes['POST'] = response.status_code
        response_json['POST'] = response.json()

        # print(response_json['POST'])

        validate_response_code(context, int(response_codes['POST']), context.config.get('RMQ_APIResponse'))
        assert response_json['POST']['routed'] == True

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def update_payload(payload):
    payload['payload'] = (payload['payload']).replace('requestId', GlobalVar.request_ID[requestType])
    payload['payload'] = (payload['payload']).replace('service_id', GlobalVar.testParams['serviceID'])
    payload['payload'] = (payload['payload']).replace('callbackURL', 'http://'+GlobalVar.webhookServer)
    return payload


def restore_payload(payload):
    if 'display' in GlobalVar.api_dict['api_endpoint_' + requestType + '_url']:
        payload['payload'] = (payload['payload']).replace(GlobalVar.reqId, 'requestId')
    else:
        payload['payload'] = (payload['payload']).replace(GlobalVar.request_ID[requestType], 'requestId')
    if 'rollback' in GlobalVar.api_dict['api_endpoint_' + requestType + '_url']:
        payload['payload'] = (payload['payload']).replace(GlobalVar.reqId, 'rollingBackId')
    with open(filepath, "w") as outfile:
        json.dump(payload, outfile)
        return payload


@step('I validate the service record for "{progress}" state to be "{value}"')
def validate_service_state(context, progress, value):
    assert response_json['GET']['_source']['id'] == serviceId
    assert str(response_json['GET']['_source'][progress]).lower() == value


@step('I Wait for the expected timeout value for service')
def wait_for_timeout(context):
    waitTime = GlobalVar.testParams.get("waitTime")
    print("Waiting for timeout value:", waitTime, 'Seconds')
    time.sleep(int(waitTime))


@step('I validate that the callback info has expected "{correlationId}" and status "{status}"')
def validate_callback_info(context, correlationId, status):
    assert context.callbackInfo['response']['event']['service']['status'] == status
    assert context.callbackInfo['response'][correlationId] == GlobalVar.requestId


@step('I validate that a callback response is sent for "{statusType}"')
def validate_callback_response(context, statusType):
    context.callbackInfo = response_json['GET']['_source']['callback-info']
    # schema_file_name = os.getcwd() + '/resources/schema/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() \
    #                    + '/' + '/pubSub_' + statusType + '.json'
    # result = validate_schema(context, schema_file_name, context.callbackInfo)
    # print("Schema matched: {}".format(result))
    # assert result == True


@step('I Set POST request Body "{data_file}" for "{queueName}" for IE')
def set_body(context, data_file, queueName):
    payload = set_HTTP_request_body_IE(context, '/' + GlobalVar.testComponent[0].lower() + '/', data_file)
    if 'requests' in queueName:
        payload['routing_key'] = 'tinaa-l3vpn-requests'
    elif 'callbacks' in queueName:
        payload['routing_key'] = 'tinaa-l3vpn-request-callbacks'
    GlobalVar.api_dict['payload'] = payload
    print(GlobalVar.api_dict['payload'])


def set_HTTP_request_body_IE(context, filePath, fileName):
    rootPath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) \
               + '/resources/payload/' + sys.argv[1] + filePath + fileName
    payload = json.load(open(rootPath, 'r'))
    return payload


@step('I send "{requestType}" request for IE')
def sendHTTprequest(context, requestType):
    global response
    auth = context.config.get('RMQ_basicAuth_' + sys.argv[2])
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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


@step('Validate expected response code "{response_code}" for "{requestType}" for IE')
def validate_rep_code(context, response_code, requestType):
    assert response.status_code == int(response_code)


@step('Validate response header "{headerName}" for "{headerValue}" for IE')
def valiadte_header(context, headerName, headerValue):
    assert response.headers[headerName] == headerValue


@step('Validate that "{queueName}" queue "{scenario}" "{exchangeName}" exchange as source for IE')
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


@step('I extract the response code value for IE')
def extract_rep_code(context):
    GlobalVar.response_codes['queueStatus'] = response.status_code
    print(GlobalVar.response_codes['queueStatus'])


@step('I validate "{queueName}" queue is binded to "{exchangeName}" exchange for IE')
def assert_responseCode(context, queueName, exchangeName):
    if response.status_code == 200:
        endpoint = 'api/exchanges/%2F/bi-ctrl/bindings/source'
        requestType = 'GET'
        rmq_endpoint(context, endpoint, requestType)
        sendHTTprequest(context, requestType)
        validate_queue(context, queueName, 'has', exchangeName)
    else:
        print("Info: Queue Does not exist")


@step('I validate bind status from the previous step for IE')
def assert_code(context):
    if GlobalVar.binded:
        print('Info: Skipping Create Queue Scenario as Queue already Exists and Binded')
        context.scenario.skip(reason='Queue Exists')
    else:
        print('Info: Proceed to Create and Bind Queue as Queue do not already Exist')


@step('I Set PUT request Body "{fileName}" for "{queueName}" for IE')
def set_body(context, fileName, queueName):
    payload = set_HTTP_request_body_IE(context, '/' + GlobalVar.testComponent[0].lower() + '/', fileName)
    GlobalVar.api_dict['payload'] = payload


@step('I validate expected response code "{response_code1}" or "{response_code2}" for "{requestType}" for IE')
def validate_rep_code(context, response_code1, response_code2, requestType):
    try:
        validate_response_code(context, response.status_code, int(response_code1))
    except:
        validate_response_code(context, response.status_code, int(response_code2))


@step('Validate that the queue is empty for IE')
def validate_no_response(context):
    assert response.text == '[]'


@step('I validate that the callback response is sent for "{val}"')
def validate_callback(context, val):
    path = 'webhookResponse.json'
    GlobalVar.callbackValue = json.load(open(path))
    # print(GlobalVar.callbackValue)


@step('I validate the service record "{key}" value should be "{value}"')
def state_val(context, key, value):
    assert str(response_json['GET'][key]).lower() == value.lower()


@step('I get the Webhook instance for validating callback responses')
def get_webhook_instance(context):
    port = "8080"
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    serverUrl = ipAddress+':'+port
    if GlobalVar.testParams.get('Type') == "Timeout":
        GlobalVar.webhookServer = 'http://'+serverUrl
    else:
        GlobalVar.webhookServer = serverUrl
    print(GlobalVar.webhookServer)


@step('I validate the in-progress state of the existing service by "{testcaseName}"')
def validate_service(context, testcaseName):
    testData = {}
    if 'testCase' in testcaseName:
        testCase = (testcaseName.split('_'))[1]
        testData = context.csvReadAPI[int(testCase)-1]

    url = 'l3vpn_ingestion_engine_url_' + sys.argv[2]
    base_url = context.config.get(url)
    apiURL = base_url + testData.get('IEEndPoint')

    GlobalVar.ie_header['Content'] = testData.get('Content')
    GlobalVar.ie_header['Authorization']= GlobalVar.access_token

    serviceId = testData.get('serviceID')
    GET_URL = apiURL.replace('{service_id}', serviceId)

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.get(url=GET_URL,
                            headers= GlobalVar.ie_header,
                            verify=False)

    statusCode = response.status_code
    serviceResponse = response.json()

    schema_file = testData.get("SchemaFile")
    schema_file_name = os.getcwd() + '/resources/schema/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() \
                       + '/' + schema_file
    result = validate_schema(context, schema_file_name, serviceResponse)
    assert result == True
    assert str(statusCode) == str(testData.get('ResponseCode'))


@step('Validate that callback info has expected "{correlationId}" and status "{status}"')
def validate_callback_info(context, correlationId, status):
    assert GlobalVar.callbackValue['event']['service']['status'] == status
    assert GlobalVar.callbackValue['correlationId'] == GlobalVar.requestId