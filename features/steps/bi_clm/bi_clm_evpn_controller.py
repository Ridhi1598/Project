from behave import *
from features.steps.bi.bi_orchestrator import *
from features.steps.bi_clm.bi_clm_orchestrator import *
from common.util.api_test import ApiTest
from common.util.postgres_helper import Postgres
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

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
# end of declared variables


@step('"{action}" "{operation}" evpn message to "{entity}" "{queue}" queue')
def cs_rmq_actions(context, action, operation, entity, queue):
    # set request parameters
    url = ""
    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}_{action}_RequestType')
    endpoint = GlobalVar.testParams.get(f'{entity}_{action}_EndPoint')
    routingQueue = GlobalVar.testParams.get(f'{queue}_Queue')
    profile = GlobalVar.testParams.get('profile')

    if "evpn" in routingQueue:app = "cs"
    else: app = sys.argv[1]

    url = ''.join([set_url(context, entity, app), endpoint.format(routingQueue)])
    print(url)

    payloadFile = GlobalVar.testParams.get(f'{entity}_{action}_RequestBody').format(operation)
    # read and load payload
    GlobalVar.api_dict['request_bodies'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], payloadFile)

    # update payload with the request Id/service Id/csid
    if action.lower() == "publish":
        GlobalVar.testParams["baseRequestId"][operation] = payloadGenerator.generate_reqId(context)
        print(f'Request Id: {GlobalVar.testParams["baseRequestId"]}')

        GlobalVar.api_dict['request_bodies']['routing_key'] = routingQueue

        GlobalVar.api_dict['request_bodies'] = update_evpn_payload(GlobalVar.api_dict['request_bodies'], GlobalVar.testParams, GlobalVar.testParams["baseRequestId"][operation], profile)

    # print(json.dumps(GlobalVar.api_dict['request_bodies'], indent=4))

    # Send HTTP request and validate response
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, url, GlobalVar.api_dict['request_bodies'], context.config.get(f'{entity}_User'), context.config.get(f'{entity}_Pass'))

    print(GlobalVar.response.text)
    assert ApiTest.validateResponseCode(context, GlobalVar.response, int(GlobalVar.testParams.get(f'{entity}_{action}_ResponseCode')))

    if action.lower() == "publish":
        assert GlobalVar.response.json().get("routed")
    print("Message published", str(datetime.datetime.utcnow()))


def update_evpn_payload(payload, testparams, requestId, profileEntry):
    # update request id in payload
    payload['payload'] = (payload['payload']).replace('req_Id', requestId)

    # update service id in payload
    payload['payload'] = (payload['payload']).replace('serviceId', testparams['serviceId'])

    # update evpn Id
    payload['payload'] = (payload['payload']).replace('evpnId', testparams[profileEntry])

    # update primary device detail
    payload['payload'] = (payload['payload']).replace('primarySE', testparams['primarySE'])

    # update secondary device detail
    payload['payload'] = (payload['payload']).replace('secondarySE', testparams['secondarySE'])

    # update vpls value
    payload['payload'] = (payload['payload']).replace('vplsId', testparams['vplsId'])

    # update lag valie
    payload['payload'] = (payload['payload']).replace('lagEntry', testparams['lagId'])

    # print(json.dumps(payload, indent=4))
    return payload


@step('"{action}" and validate that a "{operation}" "{message}" response is published in the "{entity}" "{queue}" queue')
def rmq(context, action, operation, message, entity, queue, configType=None):
    global publishedMessage
    cs_rmq_actions(context, action, operation, entity, queue)

    # Messages in the queue are returned in a list
    responseList = GlobalVar.response.json()
    responseLen = len(responseList)
    print("Messages in callback queue: ", responseLen)

    # Extracting latest message from the queue
    index = 0
    print(f'Search for request Id... {GlobalVar.testParams["baseRequestId"][operation]}')
    for response in responseList:
        if GlobalVar.testParams["baseRequestId"][operation] in response["payload"]:
            publishedMessage = json.loads(response["payload"])
            break
    print(publishedMessage)

    if "callback" in message:
        print(publishedMessage["request-id"])
        print(GlobalVar.testParams["baseRequestId"][operation])
        assert publishedMessage["request-id"] == GlobalVar.testParams["baseRequestId"][operation]
        schemaFileName = f"{message}.json"
        assert ApiTest.validateResponseSchema(context, publishedMessage, schemaFileName, GlobalVar.testComponent[0])


@step('"{action}" and validate that the message is consumed by evpn from "{entity}" "{queue}" queue')
def rmq(context, action, entity, queue):
    cs_rmq_actions(context, action, '', entity, queue)
    assert not bool(len(GlobalVar.response.json()))


@step('I fetch "{package}" node data from zookeeper for "{operation}"')
def extract_nodes(context, package, operation):
    node = ""
    expectedId = GlobalVar.testParams["baseRequestId"][operation]
    print("Search Request Id:", GlobalVar.testParams["baseRequestId"][operation])
    parentPath = GlobalVar.testParams.get("zk_parent_path")
    GlobalVar.testParams["zk_timer_node"] = []
    try:
        brk_flag = False
        # try 5 times to connect with zookeeper and find zk timer node
        for i in range(5):
            time.sleep(10)
            print(f"Current Time: {str(datetime.datetime.utcnow())}")
            # calls method to return all nodes
            childNodes = ZK.get_children1(context, GlobalVar.zk, parentPath, node)
            print(f"child nodes found: {len(childNodes)}")
            if len(childNodes) > 0:
                for child in childNodes:
                    if expectedId == childNodes[child]["params"]["request_tracker"]["id"]:
                        if childNodes[child]["timer_id"] not in GlobalVar.testParams["zk_timer_node"]:
                            GlobalVar.testParams["zk_timer_node"].append(childNodes[child]["timer_id"])
                            print("Available Nodes: ", GlobalVar.testParams["zk_timer_node"])
                            for node in GlobalVar.testParams["zk_timer_node"]:
                                if node in GlobalVar.testParams["zk_deleted_node"]:
                                    GlobalVar.testParams["zk_timer_node"].remove(node)

                        print(f"Active Node found for request id {expectedId}: {len(GlobalVar.testParams['zk_timer_node'])}")

                    print(f"Zk Timer node for {package}: {GlobalVar.testParams['zk_timer_node']}")
                    brk_flag = True
            # break loop if node is found
            if brk_flag:
                break
        else:
            print(f"No node found for request id {expectedId}")
        print(f'{GlobalVar.testParams["zk_timer_node"]}')

    except Exception as err:
        print(f"Error: {err}")
        # raise Exception(err)


@step('Validate a "{operation}" node is "{nodeState}" in zookeeper for "{package}"')
def get_node(context, operation, nodeState, package):
    print(GlobalVar.testParams["zk_timer_node"])
    parentPath = GlobalVar.testParams.get("zk_parent_path")
    for node in GlobalVar.testParams["zk_timer_node"]:
        print(node)
        try:
            nodeStatus = ZK.get_node(context, GlobalVar.zk, parentPath, node)
            print("Node Type: ", type(nodeStatus))
            if nodeState == "created":
                assert nodeStatus
                print(f"Node {node} found in zookeeper {parentPath}")

            if nodeState == "deleted":
                print(f'Deleted Node List: {GlobalVar.testParams["zk_deleted_node"]}')
                assert not nodeStatus
                print(f"Node {node} not found")
                GlobalVar.testParams["zk_deleted_node"].append(node)
                print(f'Deleted Node List: {GlobalVar.testParams["zk_deleted_node"]}')

        except AssertionError as err:
            print(err)
            raise AssertionError(err)
        except Exception as err:
            print(Exception(err))
            # raise Exception(err)


@step('Validate a record is "{action}" in "{table_name}" table in "{entity}" db for "{operation}"')
def postgres(context, action, table_name, entity, operation):
    column_name = GlobalVar.testParams.get(f"{table_name}_column")
    filter_term = None
    if table_name == "evpn_bsaf_request_tracker" or table_name == "evpn_external_request_tracker":
        filter_term = GlobalVar.testParams["baseRequestId"][operation]

    if table_name == "evpn_service" or table_name == "qos_service_bi_clm":
        filter_term = GlobalVar.testParams.get(GlobalVar.testParams.get("profile"))

    print(f'Search for term "{filter_term}" in column "{column_name}" of table "{table_name}"')
    try:
        GlobalVar.testParams[table_name] = Postgres().get_table_data(table_name, column_name, filter_term)
        print(GlobalVar.testParams[table_name])
        if "not" in action:
            assert len(GlobalVar.testParams[table_name]) == 0
            print("Result: No Record found")
        else:
            assert len(GlobalVar.testParams[table_name]) > 0
            if table_name == "evpn_service":
                assert len(GlobalVar.testParams[table_name]) == 1
                assert GlobalVar.testParams[table_name][0][0] == filter_term
            print(f"Result: Expected Record found for {filter_term}")

    except AssertionError as err:
        print(err)
        # raise err
    except Exception as err:
        print(f"Other error occurred: {err}")


@step('Validate "{entries}" entries are found for "{table_name}" table for "{operation}"')
def validate_entries(context, entries, table_name, operation):
    try:
        assert len(GlobalVar.testParams[table_name]) == int(entries)
    except Exception as err:
        print(err)

@step('Validate that "{responseType}" response has "{field}" as "{value}"')
def step_impl(context, responseType, field, value):
    assert publishedMessage[field].lower() == value.lower()


@then('Validate that the request state is "{value}" for "{table_name}" table')
def step_impl(context, value, table_name):
    try:
        if table_name == "evpn_bsaf_request_tracker":
            assert str(GlobalVar.testParams[table_name][0][1]).lower() == value

        elif table_name == "evpn_external_request_tracker":
            print(GlobalVar.testParams[table_name])
            values = []
            for entry in GlobalVar.testParams[table_name]:
                values.append(str(entry[1]).lower())
            print(values)
            assert value in values

    except AssertionError as err:
        print(err)
        raise AssertionError(err)
    except Exception as err:
        print(err)


@step("Wait for expected request processing duration")
def step_impl(context):
    waitTime = GlobalVar.testParams.get("waitTime")
    print(f"Waiting for {waitTime} seconds..")
    time.sleep(int(waitTime))
    print("Time after Waiting", str(datetime.datetime.utcnow()))


@step('Read the input and output value for "{bandwidth}" in "{table_name}" table for "{scenario}"')
def step_impl(context, bandwidth, table_name, scenario):
    GlobalVar.testParams[scenario] = []
    try:
        if table_name == "qos_service_bi_clm":
            for entry in GlobalVar.testParams[table_name]:
                if GlobalVar.testParams[scenario] == []:
                    GlobalVar.testParams[scenario] = [{"input": entry[5], "output": entry[6]}]
                else:
                    GlobalVar.testParams[scenario].append({"input": entry[5], "output": entry[6]})
        print(GlobalVar.testParams[scenario])

    except Exception as err:
        print(err)


@step('Validate that the "{before}" and "{after}" values for "{bandwidth}" are "{result}"')
def step_impl(context, before, after, bandwidth, result):
    if "not" in result:
        assert GlobalVar.testParams["before"] == GlobalVar.testParams["after"]
    else:
        assert GlobalVar.testParams["before"] != GlobalVar.testParams["after"]

