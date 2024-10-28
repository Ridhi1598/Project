import sys
import time
import uuid

from behave import *
from features.steps.bi_clm.bi_clm_ingestion import *
from features.steps.globalVar import *




@step('"{action}" "{operation}" request message to "{entity}" "{queue}" queue for BNG')
def rmq_actions_bng(context, action, operation, entity, queue):
    # set request parameters

    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}_{action}_RequestType')
    endpoint = GlobalVar.testParams.get(f'{entity}_{action}_EndPoint')
    routingQueue = GlobalVar.testParams.get(f'{queue}_Queue')

    url = ''.join([set_url(context, entity), endpoint.format(routingQueue)])
    print(f"{entity} Url: {url}")

    payloadFile = ''
    if "callback" not in operation:
        payloadFile = GlobalVar.testParams.get(f'{entity}_{action}_RequestBody').format(operation)
        # print(f'{entity}_{action}_RequestBody')
        # print(payloadFile)

    # read and load payload
    GlobalVar.api_dict['request_bodies'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0],
                                                                                 payloadFile)

    if action.lower() == "publish":
        GlobalVar.api_dict['request_bodies']['routing_key'] = routingQueue
        # print("PUBLISH:", GlobalVar.api_dict['request_bodies']['routing_key'])
        if "callback" not in operation:
            if GlobalVar.testParams["baseRequestId"] is None:
                if "create_tp_request" in operation:
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload_bng_controller(
                        GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"],
                        "create_tp_request")
                elif "create_bng_dry_run" in operation or "create_l3vpn_dry_run" in operation:
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload_bng_controller(
                        GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"], "dry_run_request")
                else:
                    GlobalVar.testParams["baseRequestId"] = payloadGenerator.generate_reqId(context)
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload_bng_controller(
                        GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"])
            elif "commit" in operation:
                GlobalVar.api_dict['request_bodies'] = update_publish_payload_bng_controller(
                    GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"], "commit")
            elif "l2_to_bng" in operation and "create_tp_request" not in operation:
                GlobalVar.published_info['request-id'] = GlobalVar.published_payload['request-id']
                GlobalVar.api_dict['request_bodies'] = update_publish_payload_bng_controller(
                    GlobalVar.api_dict['request_bodies'], GlobalVar.published_payload['request-id'])
                print(f'PUBLISHED PAYLOAD ID', GlobalVar.published_info['request-id'])

            else:
                GlobalVar.testParams["baseRequestId"] = payloadGenerator.generate_reqId(context)
                GlobalVar.api_dict['request_bodies'] = update_publish_payload_bng_controller(
                    GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"])
    print(">>>>>Base request id:", GlobalVar.testParams["baseRequestId"])

    # read user credentials for authentication
    user = context.config.get(f'{entity}_User')
    password = context.config.get(f'{entity}_Pass')

    time.sleep(3)
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, url,
                                                 GlobalVar.api_dict['request_bodies'], user, password)

    # print(GlobalVar.response.status_code)
    # print(f'{entity}_{action}_ResponseCode')
    # print(GlobalVar.testParams.get(f'{entity}_{action}_ResponseCode'))
    assert ApiTest.validateResponseCode(context, GlobalVar.response,
                                        int(GlobalVar.testParams.get(f'{entity}_{action}_ResponseCode')))
    if action.lower() == "publish":
        print("Published request routed:")
        assert GlobalVar.response.json().get("routed")
    time.sleep(5)


@step('"{action}" and validate that the message is consumed by orchestrator from "{entity}" "{queue}" queue for BNG')
def rmq(context, action, entity, queue):
    rmq_actions_bng(context, action, '', entity, queue)
    assert not bool(len(GlobalVar.response.json()))


def update_publish_payload_bng_controller(payload, requestId, test=None):
    if test != None:
        if "commit" in test:
            print("IN COMMIT SECTION")
            random_uuid = str(uuid.uuid4())
            payload['payload'] = (payload['payload']).replace('req_Id', random_uuid)

            GlobalVar.commit_uuid = requestId
            payload['payload'] = (payload['payload']).replace('uuid', requestId)
            GlobalVar.testParams["baseRequestId"] = random_uuid
            print("COMMIT BASE REQUEST ID ", GlobalVar.testParams["baseRequestId"])

        if "dry_run_request" in test:
            random_uuid = str(uuid.uuid4())
            payload['payload'] = (payload['payload']).replace('req_Id', random_uuid)
            GlobalVar.testParams["baseRequestId"] = random_uuid
            print("dry run base-request id ", GlobalVar.testParams["baseRequestId"])

            if GlobalVar.testParams.get("jobOrderId") is None:
                print("No job order id- exist")
                job_order_uuid = str(uuid.uuid4())
                payload['payload'] = (payload['payload']).replace('job_Id', job_order_uuid)
                GlobalVar.testParams["jobOrderId"] = job_order_uuid
                print("NEW JOB-ORDER ID ", GlobalVar.testParams["jobOrderId"])
            else:
                random_uuid = str(uuid.uuid4())
                payload['payload'] = (payload['payload']).replace('req_Id', random_uuid)
                payload['payload'] = (payload['payload']).replace('job_Id', GlobalVar.testParams["jobOrderId"])
                print("EXISTING JOB-ORDER ID ", GlobalVar.testParams["jobOrderId"])

        if "create_tp_request" in test:
            print(GlobalVar.l2Topology_response["request-id"])
            payload['payload'] = (payload['payload']).replace('req_Id', GlobalVar.l2Topology_response["request-id"])
            print(">>>>>CREATE TP REQUEST<<<<<<<", GlobalVar.l2Topology_response["request-id"])

    else:
        payload['payload'] = (payload['payload']).replace('req_Id', requestId)
    return payload


@step(
    '"{action}" and validate that the "{operation}" "{message}" message is published in the "{entity}" "{queue}" queue for BNG')
def rmq(context, action, operation, message, entity, queue):
    global l3Event
    flag = False
    time.sleep(5)
    rmq_actions_bng(context, action, operation, entity, queue)

    # Messages in the queue are returned in a list
    responseList = GlobalVar.response.json()
    responseLen = len(responseList)

    if "l2_topology_test" not in queue:
        for i in range(responseLen):
            payloadValue = responseList[i]['payload']
            publishedMessage = json.loads(payloadValue)
            print(f'Response list value {i}:')
            print(payloadValue)
            try:
                if publishedMessage['request-id'] == GlobalVar.testParams['baseRequestId']:
                    print(f'Published message request-id {publishedMessage["request-id"]}')
                    print(f'Test-param base request-id {GlobalVar.testParams["baseRequestId"]}')
                    print("Successfully matched:")
                    flag = True
                    GlobalVar.published_payload = publishedMessage
                    break
            except Exception as e:
                assert False, "RMQ error: while validating the published message"
        assert flag == True
    else:
        index = 0
        for i in range(responseLen):
            if not responseList[i]['message_count']:
                index = i
        payloadValue = responseList[index]['payload']
        publishedMessage = json.loads(payloadValue)
        GlobalVar.published_payload = publishedMessage

    # Here, we are performing validations based on the request and published Request-Id
    if 'l2_request' in message and "publishedRequestId" not in operation:
        # we are checking the callback-url value of the published payload from L2-Topology test queue
        print("published message", GlobalVar.published_payload)
        print(GlobalVar.testParams['published_callback_value'])
        print(GlobalVar.published_payload['callback-url'])
        # assert GlobalVar.testParams['published_callback_value'] == GlobalVar.published_payload['callback-url']
        # assert GlobalVar.testParams['type'] == GlobalVar.published_payload['type']

    elif 'bng_to_portal' in message and "publishedRequestId" in operation:
        # we are validating that the request-id of the published payload and the callback message should be similar
        schemaFileName = f"{message}.json"
        print("Schema file", schemaFileName)
        assert publishedMessage["request-id"] == GlobalVar.published_info['request-id']
        assert ApiTest.validateResponseSchema(context, publishedMessage, schemaFileName, GlobalVar.testComponent[0])

    elif 'bng_to_portal' in message and "baseRequestId" in operation:
        schemaFileName = f"{message}.json"
        print("Schema file", schemaFileName)
        assert publishedMessage["request-id"] == GlobalVar.testParams["baseRequestId"]
        assert ApiTest.validateResponseSchema(context, publishedMessage, schemaFileName, GlobalVar.testComponent[0])


@step('Get and verify the "{action}" request record by "{key}" from table "{table_name}" with "{state}" state')
def verify_request_in_postgres_db(context, action, key, table_name, state):
    global result
    if action == "committed":
        count = 0
        result = execute_select_query_bng(table_name, where_conditions={key: GlobalVar.commit_uuid})
        print("COMMITTED DB:")
        print(result)
        while result['result'][0]['state'].lower() != state:
            print(f'In while condition and record is in {result["result"][0]["state"].lower()} state')
            time.sleep(15)
            result = execute_select_query_bng(table_name, where_conditions={key: GlobalVar.commit_uuid})
            count = count + 1
            if count == 5:
                assert False, f'Record found but is not in expected state {result["result"][0]["state"].lower()}'
        print("Query output :", result)
        GlobalVar.create_request_obj = result

    else:
        db_count = 0
        if key == "id" or key == "parent_request_tracker_id":
            filter_value = GlobalVar.testParams["baseRequestId"]
        elif key == "bng_group_id":
            filter_value =  GlobalVar.testParams["bng_group_id"]
        result = execute_select_query_bng(table_name, where_conditions={key: filter_value})
        print("<<<DB RESULT>>>", result)

        while result['result'][0]['state'].lower() != state:
            time.sleep(15)
            print(f'<<< In while condition and record is in {result["result"][0]["state"].lower()} state')
            result = execute_select_query_bng(table_name, where_conditions={key: filter_value})
            db_count = db_count + 1
            if db_count == 5:
                assert False, f'Record found but is not in expected state {result["result"][0]["state"].lower()}'
        print("Query output", result)
        GlobalVar.create_request_obj = result


def execute_select_query_bng(table_name: str = None, col_names=['*'], where_conditions=None):
    appName = None
    url = "https://bi-mocking-server.qa.app01.toll6.tinaa.tlabs.ca/query-v2"
    col_name_str = ', '.join(f'{col}' for col in col_names)

    # Construct the SQL query
    if where_conditions:
        where_clause = ' AND '.join(f"{key} = '{value}'" for key, value in where_conditions.items())
        query_prepared = f"SELECT {col_name_str} FROM {table_name} WHERE {where_clause}"
    else:
        query_prepared = f"SELECT {col_name_str} FROM {table_name}"
    print("Query:", query_prepared)

    print(GlobalVar.testComponent[0].lower())
    if "bng-controller" in GlobalVar.testComponent[0].lower():
        appName = 'bng'
    elif "evpn" in GlobalVar.testComponent[0].lower():
        appName = 'evpn'
    elif "orchestrator" in GlobalVar.testComponent[0].lower():
        appName = 'orchestrator'
    elif "polling" in GlobalVar.testComponent[0].lower():
        appName = 'polling'        

    payload = json.dumps({
        "controller_name": appName,
        "query": query_prepared
    })

    headers = {
        'Content-Type': 'application/json'
    }
    print("URL:", url)
    print(payload)
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print("RESPONSE ", response.text)
    return response.json()


@step('I validate that the request record should "{action}" in the table "{table_name}" by "{key}"')
def verify_db_record(context, action, table_name, key):
    global result
    if table_name == "bng_group":
        result = execute_select_query_bng(table_name, where_conditions={key: GlobalVar.testParams["bng_group_id"]})
        if action.lower() == "exist":
            assert result['message'] == "Data fetch successfully"
        else:
            assert result['message'] == "No data found!"

    elif table_name == "vpn_node":
        if action.lower() == "exist":
            result = execute_select_query_bng(table_name, where_conditions={key: GlobalVar.testParams["vpn_id"]})
            assert len(result['result']) == 4
            assert result['message'] == "Data fetch successfully"
        else:
            result = execute_select_query_bng(table_name, where_conditions={key: GlobalVar.testParams["vpn_id"]})
            assert result['message'] == "No data found!"

    elif table_name == "bng_external_request_tracker":
        if key == "id":
            result = execute_select_query_bng(table_name, where_conditions={key: GlobalVar.l2topology_uuid})
        else:
            result = execute_select_query_bng(table_name, where_conditions={key: GlobalVar.testParams["baseRequestId"]})
            GlobalVar.commit_request_id = GlobalVar.testParams["baseRequestId"]

        if action.lower() == "exist":
            assert result['message'] == "Data fetch successfully"
        else: assert result['message'] == "No data found!"


    elif table_name == "vpn_service":
        if action.lower() == "not exist":
            result = execute_select_query_bng(table_name, where_conditions={key: GlobalVar.testParams["vpn_id"]})
            assert result['message'] == "No data found!"
        elif action.lower() == "exist":
            result = execute_select_query_bng(table_name, where_conditions={key: GlobalVar.testParams["vpn_id"]})
            assert result['message'] == "Data fetch successfully"

    elif table_name == "pw_port":
        if action == "exist":
            result = execute_select_query_bng(table_name,
                                              where_conditions={key: GlobalVar.testParams["first_bng_name"]})
            assert result['result'][0]['id'] == "300"
            assert result['message'] == "Data fetch successfully"

            result = execute_select_query_bng(table_name,
                                              where_conditions={key: GlobalVar.testParams["second_bng_name"]})
            assert result['result'][0]['id'] == "300"
            assert result['message'] == "Data fetch successfully"

        elif table_name == "pw_port" and action == "not exist":
            result = execute_select_query_bng(table_name,
                                              where_conditions={key: GlobalVar.testParams["first_bng_name"]})
            assert result['message'] == "No data found!"

            result = execute_select_query_bng(table_name,
                                              where_conditions={key: GlobalVar.testParams["second_bng_name"]})
            assert result['message'] == "No data found!"

    elif table_name == "vpn_network_access":
        existing_row_count = 2
        if action == "exist":
            result = execute_select_query_bng(table_name, where_conditions={key: "EDTNABTFOT39"})
            assert len(result['result']) == existing_row_count
            assert result['message'] == "Data fetch successfully"

            result = execute_select_query_bng(table_name, where_conditions={key: "EDTNABTFOT39-DV"})
            assert result['message'] == "Data fetch successfully"
            assert len(result['result']) == existing_row_count

            result = execute_select_query_bng(table_name, where_conditions={key: "EDTNABTFOT39-FIXED"})
            assert len(result['result']) == existing_row_count
            assert result['message'] == "Data fetch successfully"

        elif action == "non-exist":
            result = execute_select_query_bng(table_name, where_conditions={key: "EDTNABTFOT39"})
            assert result['message'] == "No data found!"

            result = execute_select_query_bng(table_name, where_conditions={key: "EDTNABTFOT39-DV"})
            assert result['message'] == "No data found!"

            result = execute_select_query_bng(table_name, where_conditions={key: "EDTNABTFOT39-FIXED"})
            assert result['message'] == "No data found!"

    GlobalVar.db_obj = result
    print(">>>>>>>>DATABASE OBJECT START")
    print(GlobalVar.db_obj)
    print(">>>>>>>>DATABASE OBJECT END")
    #
    # if action.lower() == 'exist':
    #     assert result['message'] == "Data fetch successfully"
    # elif action.lower() == 'not-exist':
    #     assert result['message'] == "No data found!"
    #


@step('I validate the state of requests for the "{action}" scenario in the "{table_name}" table using the "{key}"')
def validate_multiple_record_from_table(context, action, table_name, key):
    global query_op
    time.sleep(30)
    if None != GlobalVar.db_obj and table_name == "bng_external_request_tracker":
        result_list = GlobalVar.db_obj['result']
        for entry in result_list:
            id_value = entry['id']
            if '-' not in id_value:
                query_op = execute_select_query_bng(table_name, where_conditions={'id': id_value})
                print(query_op['result'][0])
                if action == "commit success":
                    assert 'completed' == str(query_op['result'][0]['state']).lower()
            else:
                query_op = execute_select_query_bng(table_name, where_conditions={'id': id_value})
                print(">>>>>>>Query result start")
                print(query_op['result'][0])
                print(">>>>>>>Query result end")
                GlobalVar.l2topology_uuid = str(query_op['result'][0]['id'])
                assert 'completed' == str(query_op['result'][0]['state']).lower()


@step('I validate the L3VPN request record from "{table_name}" table using the "{key}"')
def validate_l3vpn_record_from_table(context, table_name, key):
    global topology_id
    if None != GlobalVar.db_obj and table_name == "bng_external_request_tracker":
        result_list = GlobalVar.db_obj['result']
        for entry in result_list:
            id_value = entry['id']
            if '-' in id_value:
                query_result = execute_select_query_bng(table_name, where_conditions={'id': id_value})
                print("QUERY OUTPUT:-")
                print(query_result['result'])
                if 'completed' == str(query_result['result'][0]['state']).lower():
                    topology_id = str(query_result['result'][0]['id'])
                    GlobalVar.l2topology_uuid = topology_id


@step(
    '"{action}" and validate that the "{operation}" "{message}" message is published in the "{entity}" "{queue}" queue for commit requests')
def rmq(context, action, operation, message, entity, queue):
    global l3Event
    time.sleep(5)
    rmq_actions_bng(context, action, operation, entity, queue)

    # Messages in the queue are returned in a list
    responseList = GlobalVar.response.json()
    responseLen = len(responseList)
    for i in range(responseLen):
        payloadValue = responseList[i]['payload']
        publishedMessage = json.loads(payloadValue)
        try:
            if publishedMessage['request-id'] == GlobalVar.l2topology_uuid:
                print(f'Published message request-id {publishedMessage["request-id"]}')
                print(f'Test-param base request-id {GlobalVar.l2topology_uuid}')
                print("Successfully matched:")
                GlobalVar.l2Topology_response = publishedMessage
                break
        except Exception as e:
            assert False, "RMQ error: while validating the published message"
    print(GlobalVar.l2Topology_response)

    print("published message", GlobalVar.l2Topology_response)
    print(GlobalVar.testParams['published_callback_value'])
    print(GlobalVar.l2Topology_response['callback-url'])
    assert GlobalVar.testParams['published_callback_value'] == GlobalVar.l2Topology_response['callback-url']
    assert GlobalVar.testParams['type'] == GlobalVar.l2Topology_response['type']


@step('I validate the "{key}" from "{table_name}" for patch_l3vpn_service')
def step_impl(context, key, table_name):
    time.sleep(20)
    GlobalVar.db_obj = execute_select_query_bng(table_name,
                                                where_conditions={key: GlobalVar.testParams["baseRequestId"]})
    if None != GlobalVar.create_request_obj and table_name == "bng_external_request_tracker":
        result_list = GlobalVar.db_obj['result']
        for entry in result_list:
            id_value = entry['id']
            query_op = execute_select_query_bng(table_name, where_conditions={'id': id_value})
            print(query_op['result'][0])
            assert 'completed' == str(query_op['result'][0]['state']).lower()


@step('I wait for "{seconds}" seconds to update the parent request record')
def step_impl(context, seconds):
    time.sleep(int(seconds))


@step(
    'I validate that all the requests state should be "completed" from "{table_name}" for commit patch L3VPN dry run request')
def step_impl(context, table_name):
    global topology_id
    if None != GlobalVar.db_obj and table_name == "bng_external_request_tracker":
        result_list = GlobalVar.db_obj['result']
        for entry in result_list:
            id_value = entry['id']
            if '-' in id_value:
                query_result = execute_select_query_bng(table_name, where_conditions={'id': id_value})
                print("Query output:")
                print(query_result['result'])
                assert 'completed' == str(query_result['result'][0]['state']).lower()
                topology_id = str(query_result['result'][0]['id'])
                GlobalVar.l2topology_uuid = topology_id
            else:
                query_result = execute_select_query_bng(table_name, where_conditions={'id': id_value})
                print("QUERY OUTPUT:-")
                print(query_result['result'])
                assert 'completed' == str(query_result['result'][0]['state']).lower()


@step("I read test data for BNG controller testcases")
def step_impl(context):
    testCase = context.scenario.name.split(':')[0]
    print(int(testCase.split('_')[1]) - 1)
    GlobalVar.testParams = context.csvReadAPI[int(testCase.split('_')[1]) - 1]
    # print("------------------")
    # print(GlobalVar.testComponent[0].lower())
    if "orchestrator" in GlobalVar.testComponent[0].lower() or "bng-controller" in GlobalVar.testComponent[0].lower() or "polling" in GlobalVar.testComponent[0].lower():
        GlobalVar.testParams["baseRequestId"] = None
        GlobalVar.testParams["requestId"] = None
    # print(GlobalVar.testParams)


@step('I read the testdata for L3VPN dry run testcase')
def step_impl(context):
    jobOrderId = GlobalVar.testParams["jobOrderId"]
    testCase = context.scenario.name.split(':')[0]
    GlobalVar.testParams = context.csvReadAPI[int(testCase.split('_')[1]) - 1]

    GlobalVar.testParams["jobOrderId"] = jobOrderId
    GlobalVar.testParams['baseRequestId'] = None


@step('I read the testdata for commit the patch l3vpn dry run request')
def step_impl(context):
    baseRequestId = GlobalVar.testParams['baseRequestId']
    testCase = context.scenario.name.split(':')[0]
    GlobalVar.testParams = context.csvReadAPI[int(testCase.split('_')[1]) - 1]

    GlobalVar.testParams['baseRequestId'] = baseRequestId


@step('I read the testdata for commit requests')
def step_impl(context):
    baseRequestId = GlobalVar.testParams['baseRequestId']
    jobOrderId = GlobalVar.testParams["jobOrderId"]
    testCase = context.scenario.name.split(':')[0]
    GlobalVar.testParams = context.csvReadAPI[int(testCase.split('_')[1]) - 1]

    GlobalVar.testParams['baseRequestId'] = baseRequestId
    GlobalVar.testParams["jobOrderId"] = jobOrderId


@step('I read the testdata for patch commit multicast dry run request')
def step_impl(context):
    baseRequestId = GlobalVar.testParams['baseRequestId']
    testCase = context.scenario.name.split(':')[0]
    GlobalVar.testParams = context.csvReadAPI[int(testCase.split('_')[1]) - 1]

    GlobalVar.testParams['baseRequestId'] = baseRequestId

    
