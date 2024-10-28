import time

from behave import *

from common.util.common_util import common_globals_cs_orch
from features.steps.bi_clm.bi_clm_ingestion import *
from features.steps.globalVar import *
from features.steps.global_cs_orchestrator import CsOrch

"""Declared global variables"""
db_count = 0

l2_counter = 0
evpn_counter = 0
bng_counter = 0

l2_published_request = 0
evpn_published_counter = 0
bng_published_counter = 0


@step("I read test data for CS testcases")
def step_impl(context):
    testCase = context.feature.filename.split('_')[2]
    GlobalVar.testParams = context.csvReadAPI[int(testCase) - 1]
    GlobalVar.test_case = testCase
    GlobalVar.testParams[GlobalVar.test_case] = {}
    if "orchestrator" in GlobalVar.testComponent[0].lower() or "bng-controller" in GlobalVar.testComponent[0].lower():
        GlobalVar.testParams["baseRequestId"] = None
        GlobalVar.testParams["requestId"] = None

# @step("I read test data for orchestrator testcases")
# @given("I read test data for BNG controller testcases")
# def step_impl(context):
#     testCase = context.scenario.name.split(':')[0]
#     GlobalVar.testParams = context.csvReadAPI[int(testCase.split('_')[1]) - 1]
#     if "orchestrator" in GlobalVar.testComponent[0].lower() or "bng-controller" in GlobalVar.testComponent[0].lower():
#         GlobalVar.testParams["baseRequestId"] = None
#         GlobalVar.testParams["requestId"] = None


@step('"{action}" "{operation}" message to "{entity}" "{queue}" queue for Orchestrator')
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
        print(f'{entity}_{action}_RequestBody')

    # read and load payload
    GlobalVar.api_dict['request_bodies'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], payloadFile)
    # update payload with the request Id/service Id/csid
    if action.lower() == "publish":
        GlobalVar.api_dict['request_bodies']['routing_key'] = routingQueue
        print("publish:", GlobalVar.api_dict['request_bodies']['routing_key'])
        if "callback" not in operation:
            if GlobalVar.testParams["baseRequestId"] is None:
                print("Base request-id is none:")
                GlobalVar.testParams["baseRequestId"] = payloadGenerator.generate_reqId(context)
                common_globals_cs_orch.requestId = GlobalVar.testParams["baseRequestId"]
                print(f'Request Id: {GlobalVar.testParams["baseRequestId"]}')
                if "push_bng_onboarding_config" in operation:
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"], "push_bng_onboarding")
                elif "push_olt_onboarding_config" in operation:
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"], "push_olt_onboarding")
                elif "get_request_tracker_info" in operation  or "reject_bng_or_olt" in operation:
                    GlobalVar.testParams["baseRequestId"] = payloadGenerator.generate_reqId(context)
                    print(f'Request Id: {GlobalVar.testParams["baseRequestId"]}')
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"], "get_request_tracker_info")
                else:
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"])
                    CsOrch.id['baseRequestId'] = GlobalVar.testParams["baseRequestId"]

            elif "l2_to_orchestrator" in operation:
                global l2_counter
                # published_info is used to store the base requestId value
                GlobalVar.published_info['request-id'] = GlobalVar.published_payload['request-id']
                # common_globals_cs_orch.requestId = GlobalVar.published_info['request-id']
                print(f'Published payload id:', GlobalVar.published_info['request-id'])

                # if "push_bng_onboarding" in operation:
                #     GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.published_payload['request-id'], "l2")
                # else:
                GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.published_payload['request-id'])

                """Assigning published requestID for L2 Topology request"""
                if "create_bng_onboarding" in operation or "create_olt_onboarding" in operation:
                    CsOrch.id[f'l2Published_requestId_{l2_counter}'] = GlobalVar.published_payload['request-id']
                    l2_counter = l2_counter + 1

            elif "evpn_to_orchestrator" in operation:
                global evpn_counter
                # published_info is used to store the base requestId value
                GlobalVar.published_info['request-id'] = GlobalVar.published_payload['request-id']
                # common_globals_cs_orch.requestId = GlobalVar.published_payload['request-id']
                print(f'Published payload id:', GlobalVar.published_info['request-id'])

                # if "push_bng_onboarding" in operation:
                #     GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.published_payload['request-id'], "evpn")
                # else:
                GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.published_payload['request-id'])

                """Assigning published requestID for evpnPublished request"""
                if "create_bng_onboarding" in operation or "create_olt_onboarding" in operation:
                    CsOrch.id[f'evpnPublished_requestId_{evpn_counter}'] = GlobalVar.published_payload['request-id']
                    evpn_counter = evpn_counter + 1
                # elif "push_bng_onboarding" in operation:

            elif "bng_to_orchestrator" in operation:
                global bng_counter
                GlobalVar.published_info['request-id'] = GlobalVar.published_payload['request-id']
                # common_globals_cs_orch.requestId = GlobalVar.published_payload['request-id']
                print(f'Published payload id:', GlobalVar.published_info['request-id'])

                # if "push_bng_onboarding" in operation:
                #     GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.published_payload['request-id'], "bng")
                # else:
                GlobalVar.api_dict['request_bodies'] = update_publish_payload_orchestrator(GlobalVar.api_dict['request_bodies'], GlobalVar.published_payload['request-id'])

                """Assigning published requestID for bngPublished request"""
                if "create_bng_onboarding" in operation or "create_olt_onboarding" in operation:
                    CsOrch.id[f'bngPublished_requestId_{bng_counter}'] = GlobalVar.published_payload['request-id']
                    bng_counter = bng_counter + 1
                # elif "push_bng_onboarding" in operation:

    # read user credentials for authentication
    user = context.config.get(f'{entity}_User')
    password = context.config.get(f'{entity}_Pass')

    time.sleep(3)
    # GlobalVar.api_dict['request_bodies'] = json.dumps(GlobalVar.api_dict['request_bodies'])
    # print("REQUEST BODY:")
    # print(GlobalVar.api_dict['request_bodies'])
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, url, GlobalVar.api_dict['request_bodies'], user, password)
    print(GlobalVar.response)

    assert ApiTest.validateResponseCode(context, GlobalVar.response, int(GlobalVar.testParams.get(f'{entity}_{action}_ResponseCode')))
    if action.lower() == "publish":
        print("ROUTED:")
        assert GlobalVar.response.json().get("routed")
    time.sleep(3)


@step('"{action}" and validate that the message is consumed by orchestrator from "{entity}" "{queue}" queue for Orchestrator')
def rmq(context, action, entity, queue):
    rmq_actions_bng(context, action, '', entity, queue)
    assert not bool(len(GlobalVar.response.json()))


def update_publish_payload_orchestrator(payload, requestId, test = None):
    global l2_published_request
    if test != None:
        # if test == "l2":
        #     payload['payload'] = (payload['payload']).replace('req_Id', requestId)
        #     payload['payload'] = (payload['payload']).replace('uuid', CsOrch.id[f'l2Published_requestId_{l2_published_request}'])
        #     l2_published_request = l2_published_request + 1
        # elif test == "evpn":
        #     payload['payload'] = (payload['payload']).replace('req_Id', requestId)
        #     payload['payload'] = (payload['payload']).replace('uuid', CsOrch.id[f'evpnPublished_requestId_{evpn_published_counter}'])
        #     l2_published_request = l2_published_request + 1
        # elif test == "bng":
        #     payload['payload'] = (payload['payload']).replace('req_Id', requestId)
        #     payload['payload'] = (payload['payload']).replace('uuid', CsOrch.id[f'bngPublished_requestId_{bng_published_counter}'])
        #     l2_published_request = l2_published_request + 1
        if test == "push_bng_onboarding":
            print("Create BNG Onboarding", CsOrch.id['baseRequestId'])
            payload['payload'] = (payload['payload']).replace('req_Id', requestId)
            payload['payload'] = (payload['payload']).replace('uuid', CsOrch.id['baseRequestId'])
        elif test == "push_olt_onboarding":
            print("Create OLT Onboarding", CsOrch.id['baseRequestId'])
            payload['payload'] = (payload['payload']).replace('req_Id', requestId)
            payload['payload'] = (payload['payload']).replace('uuid', CsOrch.id['baseRequestId'])
        elif test == "get_request_tracker_info":
            print("Create OLT Onboarding", CsOrch.id['baseRequestId'])
            payload['payload'] = (payload['payload']).replace('req_Id', requestId)
            payload['payload'] = (payload['payload']).replace('uuid', CsOrch.id['baseRequestId'])
    else:
        payload['payload'] = (payload['payload']).replace('req_Id', requestId)
    return payload


@step('"{action}" and validate that the "{operation}" "{message}" message is published in the "{entity}" "{queue}" queue for Orchestrator')
def rmq(context, action, operation, message, entity, queue):
    time.sleep(5)
    global l3Event
    flag = False
    rmq_actions_bng(context, action, operation, entity, queue)
    # Messages in the queue are returned in a list
    responseList = GlobalVar.response.json()
    responseLen = len(responseList)
    if "l2_topology_test" not in queue and "evpn_controller_test" not in queue and "bng_controller_test" not in queue:
        for i in range(responseLen):
            payloadValue = responseList[i]['payload']
            publishedMessage = json.loads(payloadValue)
            print(payloadValue)
            try:
                if publishedMessage['request-id'] == GlobalVar.testParams['baseRequestId']:
                    print(f'Published message request-id {publishedMessage["request-id"]}')
                    print(f'Test-param base request-id {GlobalVar.testParams["baseRequestId"]}')
                    print("---Successfully matched---")
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
        print(f"RMQ {queue} MESSAGE:")
        print(GlobalVar.published_payload)

    # Here, we are performing validations based on the request and published Request-Id
    if 'l2_request' in message and "publishedRequestId" not in operation:
        # we are checking the callback-url value of the published payload from L2-Topology test queue
        if "second" in operation:
            # print("published message", GlobalVar.published_payload)
            # print(GlobalVar.testParams['l2Topology_second_published_callback_value'])
            # print(GlobalVar.published_payload['callback-url'])
            assert GlobalVar.testParams['l2Topology_second_published_callback_value'] == GlobalVar.published_payload['callback-url']
            assert GlobalVar.testParams['l2Topology_second_published_request_type'] == GlobalVar.published_payload['type']

        else:
            # print("published message", GlobalVar.published_payload)
            # print(GlobalVar.testParams['l2Topology_first_published_callback_value'])
            # print(GlobalVar.published_payload['callback-url'])
            assert GlobalVar.testParams['l2Topology_first_published_callback_value'] == GlobalVar.published_payload['callback-url']
            assert GlobalVar.testParams['l2Topology_first_published_request_type'] == GlobalVar.published_payload['type']

    elif 'evpn_request' in message:
        if "second" in operation:
            # print("published message", GlobalVar.published_payload)
            print(GlobalVar.testParams['evpn_second_published_request_callback_value'])
            print(GlobalVar.published_payload['callback-url'])
            assert GlobalVar.testParams['evpn_second_published_request_callback_value'] == GlobalVar.published_payload['callback-url']
            assert GlobalVar.testParams['evpn_second_published_request_type'] == GlobalVar.published_payload['type']

        elif "rollback_first_evpn" in operation:
            assert GlobalVar.testParams['rollback_evpn_first_callback'] == GlobalVar.published_payload['callback-url']

        elif "rollback_second_evpn" in operation:
            assert GlobalVar.testParams['rollback_evpn_second_callback'] == GlobalVar.published_payload['callback-url']


        else:
            print(GlobalVar.testParams['evpn_first_published_request_callback_value'])
            print(GlobalVar.published_payload['callback-url'])
            assert GlobalVar.testParams['evpn_first_published_request_callback_value'] == GlobalVar.published_payload['callback-url']
            assert GlobalVar.testParams['evpn_first_published_request_type'] == GlobalVar.published_payload['type']

    elif 'bng_request' in message:
        if "second" in operation:
            # print("published message", GlobalVar.published_payload)
            print(GlobalVar.testParams['bng_second_published_request_callback_value'])
            print(GlobalVar.published_payload['callback-url'])
            assert GlobalVar.testParams['bng_second_published_request_callback_value'] == GlobalVar.published_payload['callback-url']
            assert GlobalVar.testParams['bng_second_published_request_type'] == GlobalVar.published_payload['type']

        elif "rollback_first_bng" in operation:
            assert GlobalVar.testParams['rollback_bng_first_callback'] == GlobalVar.published_payload['callback-url']

        elif "rollback_second_bng" in operation:
            assert GlobalVar.testParams['rollback_bng_second_callback'] == GlobalVar.published_payload['callback-url']

        else:
            print(GlobalVar.testParams['bng_first_published_request_callback_value'])
            print(GlobalVar.published_payload['callback-url'])
            assert GlobalVar.testParams['bng_first_published_request_callback_value'] == GlobalVar.published_payload['callback-url']
            assert GlobalVar.testParams['bng_first_published_request_type'] == GlobalVar.published_payload['type']


    elif 'orchestrator_to_portal' in message and "publishedRequestId" in operation:
        # we are validating that the request-id of the published payload and the callback message should be similar
        schemaFileName = f"{message}.json"
        print("Schema file", schemaFileName)
        # GlobalVar.testParams["baseRequestId"] = GlobalVar.published_info['request-id']
        # assert publishedMessage["request-id"] == GlobalVar.testParams["baseRequestId"]
        assert publishedMessage["request-id"] == GlobalVar.published_info['request-id']
        assert ApiTest.validateResponseSchema(context, publishedMessage, schemaFileName, GlobalVar.testComponent[0])

    elif 'orchestrator_to_portal' in message and "baseRequestId" in operation:
        schemaFileName = f"{message}.json"
        print("Schema file", schemaFileName)
        assert publishedMessage["request-id"] == GlobalVar.testParams["baseRequestId"]
        assert ApiTest.validateResponseSchema(context, publishedMessage, schemaFileName, GlobalVar.testComponent[0])
    print("IDs", CsOrch.id)


@step('I wait for "{seconds}" seconds for request to be timed out')
def step_impl(context, seconds):
    time.sleep(int(seconds))

@step('I wait for "{seconds}" seconds')
def step_impl(context, seconds):
    time.sleep(int(seconds))


@step('I dump the cs_orchestrator object')
def step_impl(context):
    CsOrch.id = None


def execute_select_query_orchestrator(table_name: str = None, col_names=['*'], where_conditions=None):
    appName = None
    url = "https://bi-mocking-server.qa.app01.toll6.tinaa.tlabs.ca/query-v2"
    col_name_str = ', '.join(f'{col}' for col in col_names)

    # Construct the SQL query
    if where_conditions:
        where_clause = ' AND '.join(f"{key} = '{value}'" for key, value in where_conditions.items())
        query_prepared = f"SELECT {col_name_str} FROM {table_name} WHERE {where_clause};"
    else:
        query_prepared = f"SELECT {col_name_str} FROM {table_name};"
    print("Query:", query_prepared)

    if "bng-controller" in GlobalVar.testComponent[0].lower():
        appName = 'bng'
    elif "evpn" in GlobalVar.testComponent[0].lower():
        appName = 'evpn'
    elif "orchestrator" in GlobalVar.testComponent[0].lower():
        appName = 'orchestrator'

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
    return response.json()

@step('I validate that the request record should "{action}" in the table "{table_name}" by "{key}" for orchestrator')
def verify_db_record(context, action, table_name, key):
    global result
    if table_name == "active_bngs":
        result = execute_select_query_orchestrator(table_name,
                                                   where_conditions={key: GlobalVar.testParams["bng_group_id"]})
    elif table_name == "active_olts":
        result = execute_select_query_orchestrator(table_name,
                                                   where_conditions={key: GlobalVar.testParams["clli_name"]})
    print(">>>>>>>>DB RESULT<<<<<<<<<:")
    print(result)
    if action.lower() == "exist":
        print("Data fetch successfully")
        assert result['message'] == "Data fetch successfully"
    else:
        print("No data found!")
        assert result['message'] == "No data found!"

@step('I validate the "{action}" request record by "{key}" from table "{table_name}" with "{state}" state')
def verify_request_in_postgres_db(context, action, key, table_name, state):
    global result
    global db_count

    result = execute_select_query_orchestrator(table_name, where_conditions={key: GlobalVar.testParams["baseRequestId"]})
    while result['result'][0]['state'].lower() != state:
        time.sleep(5)
        print(f'>>>><<<<<<< In while condition and record is in {result["result"][0]["state"].lower()} state')
        result = execute_select_query_orchestrator(table_name, where_conditions={key: GlobalVar.testParams["baseRequestId"]})
        db_count = db_count + 1
        if db_count == 10:
            assert False, f'Record found but is not in expected state {result["result"][0]["state"].lower()}'
    print("Query output", result)
    GlobalVar.create_request_obj = result
    db_count = 0
