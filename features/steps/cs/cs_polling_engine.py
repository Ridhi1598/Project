import sys
import time
import uuid
from behave import given, when, then
import psycopg2

from behave import *
from features.steps.bi_clm.bi_clm_ingestion import *
from features.steps.globalVar import *




@step('"{action}" "{operation}" request message to "{entity}" "{queue}" queue for polling engine')
def rmq_actions_bng(context, action, operation, entity, queue):
    # set request parameters

    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}_{action}_RequestType')
    print(GlobalVar.requestType)
    endpoint = GlobalVar.testParams.get(f'{entity}_{action}_EndPoint')
    print(endpoint)
    routingQueue = GlobalVar.testParams.get(f'{queue}_Queue')
    print(routingQueue)

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
        print("PUBLISH:", GlobalVar.api_dict['request_bodies']['routing_key'])
        if "callback" not in operation:
            if GlobalVar.testParams["baseRequestId"] is None:
                if "create_tp_request" in operation:
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload(
                        GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"],
                        "create_tp_request")
                elif "create_bng_dry_run" in operation or "create_l3vpn_dry_run" in operation:
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload(
                        GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"], "dry_run_request")
                else:
                    GlobalVar.testParams["baseRequestId"] = payloadGenerator.generate_reqId(context)
                    GlobalVar.api_dict['request_bodies'] = update_publish_payload(
                        GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"])
            elif "commit" in operation:
                GlobalVar.api_dict['request_bodies'] = update_publish_payload(
                    GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"], "commit")
            elif "l2_to_bng" in operation and "create_tp_request" not in operation:
                GlobalVar.published_info['request-id'] = GlobalVar.published_payload['request-id']
                GlobalVar.api_dict['request_bodies'] = update_publish_payload(
                    GlobalVar.api_dict['request_bodies'], GlobalVar.published_payload['request-id'])
                print(f'PUBLISHED PAYLOAD ID', GlobalVar.published_info['request-id'])

            else:
                GlobalVar.testParams["baseRequestId"] = payloadGenerator.generate_reqId(context)
                GlobalVar.api_dict['request_bodies'] = update_publish_payload(
                    GlobalVar.api_dict['request_bodies'], GlobalVar.testParams["baseRequestId"])
    print(">>>>>Base request id:", GlobalVar.testParams["baseRequestId"])

    # read user credentials for authentication
    user = context.config.get(f'{entity}_User')
    password = context.config.get(f'{entity}_Pass')

    time.sleep(3)
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, url, GlobalVar.api_dict['request_bodies'], user, password)

    print(GlobalVar.response.status_code)
    print(f'{entity}_{action}_ResponseCode')
    print(GlobalVar.testParams.get(f'{entity}_{action}_ResponseCode'))
    assert ApiTest.validateResponseCode(context, GlobalVar.response, int(GlobalVar.testParams.get(f'{entity}_{action}_ResponseCode')))
    if action.lower() == "publish":
        print("Published request routed:" + str(GlobalVar.response.json().get("routed")))
        assert GlobalVar.response.json().get("routed")
    time.sleep(5)



def update_publish_payload(payload, requestId, test=None):
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



# Database connection parameters

DB_USER = 'user@telus.com'
DB_PASSWORD = 'portal_user'

@given('I have a database connection')
def step_impl(context):
    context.conn = psycopg2.connect( user=DB_USER, password=DB_PASSWORD)
    context.cursor = context.conn.cursor()

@when('I execute the SQL query')
def step_impl(context):
    query = "SELECT * FROM public.polling_engine_bsaf_request_tracker WHERE id = '0428d69a-43d5-4533-80c7-8962fd5fdabf'"
    context.cursor.execute(query)
    context.result = context.cursor.fetchall()

expected_result = {
    "result": [
        {
            "id": "0428d69a-43d5-4533-80c7-8962fd5fdabf",
            "state": "FAILED"
        }
    ],
    "message": "Data fetch successfully"
}

@then('I print the result')
def step_impl(context):
    actual_result = {
        "result": [
            {"id": row[0], "state": row[1]} for row in context.result
        ],
        "message": "Data fetch successfully"
    }
    print(actual_result)
    assert actual_result == expected_result, f"Expected: {expected_result}, Actual: {actual_result}"

@step('Verify the "{field_name}" value from "{table_name}"')
def verify_res(context, table_name, field_name):
    try:
        fileName = GlobalVar.testParams.get("testFile")
        filePath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                            "../.."))) + '/resources/TestData/' + '/' + GlobalVar.testComponent[0].lower() + '/' + fileName
        with open(filePath) as messageFile:
            data = json.load(messageFile)
            expectedResponse = data.get(field_name)   

        print(GlobalVar.create_request_obj["result"][0].keys())
        assert GlobalVar.create_request_obj["result"][0][field_name] == expectedResponse
        print(f"Response matched for {field_name}")
    
    except AssertionError:
        fileName = GlobalVar.testParams.get("testFile2")
        if bool(fileName) == False:
            raise AssertionError("Response not matched")
            
        else:
            print(fileName)
            filePath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                "../.."))) + '/resources/TestData/' + '/' + GlobalVar.testComponent[0].lower() + '/' + fileName
            print(filePath)
            with open(filePath) as messageFile:
                data = json.load(messageFile)
                expectedResponse = data.get(field_name)  
                print(GlobalVar.create_request_obj["result"][0].keys())
        assert GlobalVar.create_request_obj["result"][0][field_name] == expectedResponse 
        print(f"Response matched for {field_name}")




@step('"{action}" "{operation}" value in postgres db')
def pg_actions(context, action, operation):
    bng_tables = ["vpn_service", "vpn_nodes", "vpn_node", "vpn_network_accesses", "subscriber_interfaces", "subscriber_interface", "vpn_network_access", "routing_protocols", "routing_protocol", "srrp", "vpn_network_access"]
    evpn_tables = ["evpn_service", "telus_cust_info", "evpn", "evpn_instances", "evpn_instance", "re_service_info", "interface", "local_attachment_circuit", "remote_attachment_circuit", "ethernet_segments", "ethernet_segment_identifier", "ac_pw_tina"]
    
    # define the URL
    url = context.config.get(f"postgresql_{sys.argv[2]}")

    # Read the SQL query
    fileName = GlobalVar.testParams.get(f"{action}QueryFile")
    filePath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + '/resources/TestData/' + '/' + GlobalVar.testComponent[0].lower() + '/' + fileName
    with open(filePath, "r") as queryFile:
                queries = queryFile.readlines()

    # send query to the database to update db for every iteration    
    for i in range(len(queries)):
            query_prepared = queries[i].replace("\n", "")
    
            # identify table name
            table_name = query_prepared.split(" ")[2]
            if table_name in bng_tables:
                appName = "bng"
            elif table_name in evpn_tables:
                appName = "evpn"  
            else:
                appName = "bng"     

            # create payload for the query
            payload = json.dumps({"controller_name": appName,
                "query": query_prepared})

            # define headers
            headers = {'Content-Type': 'application/json'}

            # print("URL:", url)
            print("**********************************")
            print("PAYLOAD ", payload)

            # send HTTP request to the server to update the database
            try:
                response = requests.request("POST", url, headers=headers, data=payload, verify=False)
                print("RESPONSE ", response.text)
                assert response.json().get("message") == "No data found!"
            except Exception as e:
                print(e)
            