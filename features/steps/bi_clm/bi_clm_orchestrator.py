from features.steps.bi_clm.bi_clm_ingestion import *
from common.util.api_test import ApiTest
from behave import *

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
prefix = {"before": {}, "after": {}}
speed = {"before": {}, "after": {}}
serviceParams = {}


# end of declared variables


@step('"{action}" "{operation}" service message to "{entity}" "{queue}" queue')
def rmq_actions(context, action, operation, entity, queue, profile=''):
    # set request parameters
    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}_{action}_RequestType')
    endpoint = GlobalVar.testParams.get(f'{entity}_{action}_EndPoint')
    routingQueue = GlobalVar.testParams.get(f'{queue}_Queue')

    if "evpn" in routingQueue:
        url = ''.join([set_url(context, entity, "cs"), endpoint.format(routingQueue)])
    else:
        url = ''.join([set_url(context, entity), endpoint.format(routingQueue)])
    print(f"{entity} Url: {url}")

    payloadFile = ''
    if "callback" in operation:
        if "evpn" in profile.lower():
            payloadFile = GlobalVar.testParams.get(f'{entity}_{action}_callback_RequestBody').format(operation)
        if "l3vpn" in profile.lower():
            payloadFile = GlobalVar.testParams.get(f'{entity}_{action}_callback_RequestBody').format(operation)
    else:
        payloadFile = GlobalVar.testParams.get(f'{entity}_{action}_RequestBody').format(operation)

    # read and load payload
    GlobalVar.api_dict['request_bodies'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0],
                                                                                 payloadFile)

    # update payload with the request Id/service Id/csid
    if action.lower() == "publish":
        GlobalVar.api_dict['request_bodies']['routing_key'] = routingQueue
        if "callback" not in operation:
            if GlobalVar.testParams["baseRequestId"] is None:
                GlobalVar.testParams["baseRequestId"] = payloadGenerator.generate_reqId(context)
                print(f'Request Id: {GlobalVar.testParams["baseRequestId"]}')

            if "mwr" in operation:
                GlobalVar.api_dict['request_bodies'] = update_publish_payload(GlobalVar.api_dict['request_bodies'],
                                                                              GlobalVar.testParams["serviceId"],
                                                                              GlobalVar.testParams["baseRequestId"],
                                                                              GlobalVar.testParams["mwrId"])
            else:
                GlobalVar.api_dict['request_bodies'] = update_publish_payload(GlobalVar.api_dict['request_bodies'],
                                                                              GlobalVar.testParams["serviceId"],
                                                                              GlobalVar.testParams["baseRequestId"])

        else:
            if "evpn" in profile.lower():
                if "display" in operation:
                    profileName = profile.split("_current")[0].split("_expected")[0]
                    GlobalVar.api_dict['request_bodies'] = update_evpn_callback_payload(GlobalVar.api_dict['request_bodies'], GlobalVar.testParams[profileName], GlobalVar.testParams[f"{profile}_RequestId"])
                else:
                    GlobalVar.api_dict['request_bodies'] = update_evpn_callback_payload(GlobalVar.api_dict['request_bodies'], GlobalVar.testParams[profile], GlobalVar.testParams[f"{profile}_RequestId"])

            if "l3vpn" in profile.lower():
                configType = ""
                if "display" in operation:
                    configType = operation.split("-")[2]
                eventType = l3Event
                if "display" in operation:
                    profileName = profile.split("_current")[0].split("_expected")[0]
                    GlobalVar.api_dict['request_bodies'] = update_l3vpn_callback_payload(GlobalVar.api_dict['request_bodies'], GlobalVar.testParams[profileName], GlobalVar.testParams[f"{profile}_RequestId"], eventType, GlobalVar.testParams["customerName"])
                else:
                    GlobalVar.api_dict['request_bodies'] = update_l3vpn_callback_payload(GlobalVar.api_dict['request_bodies'], GlobalVar.testParams[profile], GlobalVar.testParams[f"{profile}_RequestId"], eventType, GlobalVar.testParams["customerName"])

    # print(json.dumps(GlobalVar.api_dict['request_bodies'], indent=4))

    # read user credentials for authentication
    user = context.config.get(f'{entity}_User')
    password = context.config.get(f'{entity}_Pass')

    # Send HTTP request and validate response
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, url,
                                                 GlobalVar.api_dict['request_bodies'], user, password)

    assert ApiTest.validateResponseCode(context, GlobalVar.response,
                                        int(GlobalVar.testParams.get(f'{entity}_{action}_ResponseCode')))
    if action.lower() == "publish":
        assert GlobalVar.response.json().get("routed")


def update_publish_payload(payload, serviceID, requestId, mwrID=None):
    # update correlation-Id in payload
    payload['payload'] = (payload['payload']).replace('req_Id', requestId)

    if sys.argv[1].lower() != "cs":
        # update service Id in payload
        payload['payload'] = (payload['payload']).replace('serviceId', serviceID)
        # update service Id in payload
        if mwrID is not None:
            payload['payload'] = (payload['payload']).replace('mwrId', mwrID)
    return payload


def update_evpn_callback_payload(payload, profileId, requestId):
    # update correlation-Id in payload
    payload['payload'] = (payload['payload']).replace('reqId', requestId)
    # update profile Id in payload
    payload['payload'] = (payload['payload']).replace('profileId', profileId)
    return payload


def update_l3vpn_callback_payload(payload, nodeId, requestId, event, custName):
    # update correlation-Id in payload
    payload['payload'] = (payload['payload']).replace('reqId', requestId)

    # update time
    payload['payload'] = (payload['payload']).replace('currentTime', str(datetime.datetime.utcnow()))

    # generate eventId
    randomId = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    payload['payload'] = (payload['payload']).replace('randomId', randomId)

    # update event
    payload['payload'] = (payload['payload']).replace('l3EventType', event.upper())

    # update node Id in payload
    payload['payload'] = (payload['payload']).replace('nodeId', nodeId)

    # update customerName
    payload['payload'] = (payload['payload']).replace("customerName", custName)

    return payload


@step('"{action}" and validate that the message is consumed by orchestrator from "{entity}" "{queue}" queue')
def rmq(context, action, entity, queue):
    rmq_actions(context, action, '', entity, queue)
    assert not bool(len(GlobalVar.response.json()))


@step('I "{action}" and validate that a "{recordType}" record is "{status}" in orchestrator "{entity}" records')
def action_record_status(context, action, recordType, status, entity):
    retryCount = 0
    time.sleep(10)
    # set service/request Id
    Id = None
    if recordType == "service": Id = GlobalVar.testParams.get("siteId")
    if recordType == "request": Id = GlobalVar.testParams["baseRequestId"]
    if recordType == "csid": Id = GlobalVar.testParams["serviceId"]

    # set request parameters- method, url, body, auth
    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}_{action}_RequestType')
    reqURL = ApiTest.setEndpoint(context, set_url(context, entity), GlobalVar.testParams.get(
        f'{entity}_{action}_{recordType}_EndPoint'))
    print(f"{entity} Url: {reqURL}")

    GlobalVar.api_dict['request_bodies'] = ApiTest.setBody(context, GlobalVar.testParams.get(
        f'{entity}_{action}_{recordType}_RequestBody'), GlobalVar.testComponent[0].lower())
    if recordType == "request":
        GlobalVar.api_dict['request_bodies']['query']['match']['id'] = Id
    if recordType == "csid":
        GlobalVar.api_dict['request_bodies']['query']['match']['csid'] = Id
    if recordType == "service":
        GlobalVar.api_dict['request_bodies']['query']['match']['_id'] = Id

    # send request and store response
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, reqURL, GlobalVar.api_dict[
        'request_bodies'], context.config.get(f"{entity}_User"), context.config.get(f"{entity}_Pass"))

    # validate response code
    assert ApiTest.validateResponseCode(context, GlobalVar.response,
                                        GlobalVar.testParams.get(f'{entity}_{action}_ResponseCode'))

    # validate response values
    if recordType == "request":
        if "not" in status:
            try:
                assert GlobalVar.response.json()["hits"]["total"]["value"] == 0
            except:
                if GlobalVar.response.json()["hits"]["total"]["value"] > 0:
                    assert GlobalVar.response.json()["hits"]["hits"][0]["_id"] != GlobalVar.testParams["baseRequestId"]

        else:
            assert GlobalVar.response.json()["hits"]["total"]["value"] > 0
            assert GlobalVar.response.json()["hits"]["hits"][0]["_id"] == GlobalVar.testParams["baseRequestId"]

            reqState = GlobalVar.response.json()["hits"]["hits"][0]["_source"]["state"]
            if reqState == "submitted" or reqState == "pending":
                tempQueueData = GlobalVar.response.json()["hits"]["hits"][0]["_source"]["temp-queue"]

                if "delete" in GlobalVar.testParams.get("event").lower():
                    for tempData in tempQueueData:
                        if "user_id" in tempData.keys():
                            url = tempData["request-characteristics"]["url"]
                            if "pri" in url.lower():
                                GlobalVar.testParams["primary_l3vpn_node_RequestId"] = tempData["id"]
                                print("primary_l3vpn_node_RequestId",
                                      GlobalVar.testParams["primary_l3vpn_node_RequestId"])

                            elif "sec" in url.lower():
                                GlobalVar.testParams["secondary_l3vpn_node_RequestId"] = tempData["id"]
                                print("secondary_l3vpn_node_RequestId",
                                      GlobalVar.testParams["secondary_l3vpn_node_RequestId"])

                        elif "path" in tempData.keys():
                            pathVal = tempData["path"]
                            if "pri" in pathVal.lower():
                                GlobalVar.testParams["primary_evpn_profile_RequestId"] = tempData["request-id"]
                                print("primary_evpn_profile_RequestId",
                                      GlobalVar.testParams["primary_evpn_profile_RequestId"])

                            elif "sec" in pathVal.lower():
                                GlobalVar.testParams["secondary_evpn_profile_RequestId"] = tempData["request-id"]
                                print("secondary_evpn_profile_RequestId",
                                      GlobalVar.testParams["secondary_evpn_profile_RequestId"])

                elif "config" in GlobalVar.testParams.get("event").lower():
                    for tempData in tempQueueData:
                        if "user_id" in tempData.keys():
                            type = tempData["request-characteristics"]["type"]
                            url = tempData["request-characteristics"]["url"]
                            if "put" in type.lower():
                                if "pri" in url.lower():
                                    GlobalVar.testParams["primary_l3vpn_node_expected_RequestId"] = tempData["id"]
                                    print("primary_l3vpn_node_expected_RequestId",
                                          GlobalVar.testParams["primary_l3vpn_node_expected_RequestId"])

                                if "sec" in url.lower():
                                    GlobalVar.testParams["secondary_l3vpn_node_expected_RequestId"] = tempData["id"]
                                    print("secondary_l3vpn_node_expected_RequestId",
                                          GlobalVar.testParams["secondary_l3vpn_node_expected_RequestId"])

                            if "delete" in type.lower():
                                if "pri" in url.lower():
                                    GlobalVar.testParams["primary_l3vpn_node_current_RequestId"] = tempData["id"]
                                    print("primary_l3vpn_node_current_RequestId",
                                          GlobalVar.testParams["primary_l3vpn_node_current_RequestId"])

                                if "sec" in url.lower():
                                    GlobalVar.testParams["secondary_l3vpn_node_current_RequestId"] = tempData["id"]
                                    print("secondary_l3vpn_node_current_RequestId",
                                          GlobalVar.testParams["secondary_l3vpn_node_current_RequestId"])

                        elif "path" in tempData.keys():
                            path = tempData["path"]
                            type = tempData["type"]
                            if "update" in type.lower():
                                if "pri" in path.lower():
                                    GlobalVar.testParams["primary_evpn_profile_expected_RequestId"] = tempData["request-id"]
                                    print("primary_evpn_profile_expected_RequestId",
                                          GlobalVar.testParams["primary_evpn_profile_expected_RequestId"])

                                elif "sec" in path.lower():
                                    GlobalVar.testParams["secondary_evpn_profile_expected_RequestId"] = tempData["request-id"]
                                    print("secondary_evpn_profile_expected_RequestId",
                                          GlobalVar.testParams["secondary_evpn_profile_expected_RequestId"])

                            if "delete" in type.lower():
                                if "pri" in path.lower():
                                    GlobalVar.testParams["primary_evpn_profile_current_RequestId"] = tempData["request-id"]
                                    print("primary_evpn_profile_current_RequestId",
                                          GlobalVar.testParams["primary_evpn_profile_current_RequestId"])

                                elif "sec" in path.lower():
                                    GlobalVar.testParams["secondary_evpn_profile_current_RequestId"] = tempData["request-id"]
                                    print("secondary_evpn_profile_current_RequestId",
                                          GlobalVar.testParams["secondary_evpn_profile_current_RequestId"])


                else:
                    for tempData in tempQueueData:
                        if "user_id" in tempData.keys():
                            neId = tempData["request-characteristics"]["payload"]["vpn-service"][0]["vpn-nodes"]["vpn-node"][0]["ne-id"]
                            if "pri" in neId.lower():
                                GlobalVar.testParams["primary_l3vpn_node_RequestId"] = tempData["id"]
                                print("primary_l3vpn_node_RequestId",
                                      GlobalVar.testParams["primary_l3vpn_node_RequestId"])

                            elif "sec" in neId.lower():
                                GlobalVar.testParams["secondary_l3vpn_node_RequestId"] = tempData["id"]
                                print("secondary_l3vpn_node_RequestId",
                                      GlobalVar.testParams["secondary_l3vpn_node_RequestId"])

                        elif "path" in tempData.keys():
                            service = tempData["payload"]["service-name"]
                            if "pri" in service.lower():
                                GlobalVar.testParams["primary_evpn_profile_RequestId"] = tempData["request-id"]
                                print("primary_evpn_profile_RequestId",
                                      GlobalVar.testParams["primary_evpn_profile_RequestId"])

                            elif "sec" in service.lower():
                                GlobalVar.testParams["secondary_evpn_profile_RequestId"] = tempData["request-id"]
                                print("secondary_evpn_profile_RequestId",
                                      GlobalVar.testParams["secondary_evpn_profile_RequestId"])


            if reqState == "failed":
                tempQueueData = GlobalVar.response.json()["hits"]["hits"][0]["_source"]["temp-queue"]
                for tempData in tempQueueData:
                    if "user_id" in tempData.keys():
                        url = tempData["request-characteristics"]["url"]
                        if "pri" in url.lower():
                            GlobalVar.testParams["primary_l3vpn_node_RequestId"] = tempData["id"]
                            print("primary_l3vpn_node_RequestId", GlobalVar.testParams["primary_l3vpn_node_RequestId"])

                        elif "sec" in url.lower():
                            GlobalVar.testParams["secondary_l3vpn_node_RequestId"] = tempData["id"]
                            print("secondary_l3vpn_node_RequestId",
                                  GlobalVar.testParams["secondary_l3vpn_node_RequestId"])

                    elif "path" in tempData.keys():
                        pathVal = tempData["path"]
                        if "pri" in pathVal.lower():
                            GlobalVar.testParams["primary_evpn_profile_RequestId"] = tempData["request-id"]
                            print("primary_evpn_profile_RequestId",
                                  GlobalVar.testParams["primary_evpn_profile_RequestId"])

                        elif "sec" in pathVal.lower():
                            GlobalVar.testParams["secondary_evpn_profile_RequestId"] = tempData["request-id"]
                            print("secondary_evpn_profile_RequestId",
                                  GlobalVar.testParams["secondary_evpn_profile_RequestId"])

    if recordType == "service":
        if "not" in status:
            try:
                assert GlobalVar.response.json()["hits"]["total"]["value"] == 0
            except AssertionError:
                assert GlobalVar.testParams["serviceId"] not in \
                       GlobalVar.response.json()["hits"]["hits"][0]["_source"]["sites"]["site"][0][
                           "l3vpn-svc-augment:telus-cust-service-id"]

    if recordType == "csid":
        print(GlobalVar.response.json())


@step('I validate that "{recordType}" record "{field}" value is "{value}"')
def step_impl(context, recordType, field, value):
    print(str(GlobalVar.response.json()["hits"]["hits"][0]["_source"][field]).lower())
    assert str(GlobalVar.response.json()["hits"]["hits"][0]["_source"][field]).lower() == str(value).lower()


@step('I validate that "{recordType}" record is updated with "{field}"')
def step_imp(context, recordType, field):
    print(GlobalVar.response.json()["hits"]["hits"][0]["_source"][field])
    associatedRequests = GlobalVar.response.json()["hits"]["hits"][0]["_source"][field]
    reqList = []
    for associatedRequest in associatedRequests:
        reqList.append(associatedRequest["id"])
    print(reqList)
    if not GlobalVar.testParams["baseRequestId"] in reqList:
        raise AssertionError


@step('"{action}" and validate that a "{operation}" "{message}" message is published in the "{entity}" "{queue}" queue')
def rmq(context, action, operation, message, entity, queue, configType=None):
    global l3Event
    time.sleep(10)
    rmq_actions(context, action, operation, entity, queue)
    publishedMessage = {}
    msgList = []

    # Messages in the queue are returned in a list
    responseList = GlobalVar.response.json()
    responseLen = len(responseList)
    print(f"Messages in queue: {responseLen} at {datetime.datetime.utcnow()}")
    # Extracting required message from the queue
    for response in responseList:
        tempMessage = json.loads(response["payload"])
        if "callback" in queue:
            print(f'Search for request Id in callback message... {GlobalVar.testParams["baseRequestId"]}')
            if "correlationId" in tempMessage.keys():
                if GlobalVar.testParams["baseRequestId"] == tempMessage["correlationId"]:
                    msgList.append(tempMessage)

        elif "publish" in queue:
            if "rollback" in operation:
                if "user_id" in tempMessage.keys():
                    if GlobalVar.testParams[f"{message}_RequestId"] == tempMessage["id"]:
                        print("found", tempMessage["id"])
                        publishedMessage = tempMessage
                        l3Event = publishedMessage["request-characteristics"]["type"]
                        print(l3Event)
                        break

                elif "path" in tempMessage.keys():
                    if GlobalVar.testParams[f"{message}_RequestId"] == tempMessage["request-id"]:
                        print("found", tempMessage["request-id"])
                        publishedMessage = tempMessage
                        break

            else:
                print(f'Search for request Id in published message... {GlobalVar.testParams[f"{message}_RequestId"]}')

                if "user_id" in tempMessage.keys():
                    if GlobalVar.testParams[f"{message}_RequestId"] == tempMessage["id"]:
                        print("found", tempMessage["id"])
                        publishedMessage = tempMessage
                        l3Event = publishedMessage["request-characteristics"]["type"]
                        print(l3Event)
                        break

                elif "path" in tempMessage.keys():
                    if GlobalVar.testParams[f"{message}_RequestId"] == tempMessage["request-id"]:
                        print("found", tempMessage["request-id"])
                        publishedMessage = tempMessage
                        break

            print("=========###+++++++", datetime.datetime.utcnow(), "\n", publishedMessage, "\n")

    # Extract and validate required params
    if "callback" not in message:
        # if "evpn" in message:
        #     GlobalVar.testParams[f"{message}_RequestId"] = publishedMessage["request-id"]
        # if "l3vpn" in message:
        # GlobalVar.testParams[f"{message}_RequestId"] = publishedMessage["id"]
        # l3Event = publishedMessage["request-characteristics"]["type"]
        #     if "mwr" in message:
        #         if "post" not in publishedMessage["request-characteristics"]["type"].lower():
        #             assert GlobalVar.testParams.get(message) in publishedMessage["request-characteristics"]["url"]
        # print(f'{message}_RequestId: {GlobalVar.testParams[f"{message}_RequestId"]}')

        if "rollback" in operation:
            if "evpn" in message:
                if "create" in GlobalVar.testParams.get("event").lower():
                    print(publishedMessage)
                    assert publishedMessage["path"] == GlobalVar.testParams.get(f"{operation}_path").format(GlobalVar.testParams.get(message))
                if "update" in GlobalVar.testParams.get("event").lower():
                    print(publishedMessage)
                    print(publishedMessage["path"])
                    print(GlobalVar.testParams.get(f"{operation}_path").format(GlobalVar.testParams.get(message)))
                    assert publishedMessage["path"] == GlobalVar.testParams.get(f"{operation}_path").format(GlobalVar.testParams.get(message))

            elif "l3vpn" in message:
                assert publishedMessage["request-characteristics"]["url"] == GlobalVar.testParams.get(
                    f"{operation}_url").format(GlobalVar.testParams.get("customerName"),
                                               GlobalVar.testParams.get(message))

    else:
        try:
            for msg in msgList:
                assert msg["correlationId"] == GlobalVar.testParams["baseRequestId"]
                schemaFileName = f"{message}.json"
                if ApiTest.validateResponseSchema(context, msg, schemaFileName, GlobalVar.testComponent[0]):
                    break
        except Exception:
            raise Exception


@step('"{action}" "{operation}" response to "{entity}" "{queue}" queue for "{profile}"')
def publish_mock_message(context, action, operation, entity, queue, profile):
    rmq_actions(context, action, operation, entity, queue, profile)


@step('I send request to "{action}" the "{recordType}" record in "{entity}" database')
def action_record_status(context, action, recordType, entity):
    # set service/request Id
    Id = None
    requestRecordType = None
    if recordType == "service": Id = GlobalVar.testParams.get("siteId")
    if recordType == "csid": Id = GlobalVar.testParams["serviceId"]
    # if recordType == "request":
    if "request" in recordType:
        requestRecordType = recordType
        recordType = "request"

        if action != "create":
            Id = GlobalVar.testParams["baseRequestId"]

        else:
            if "mwr" in requestRecordType:
                if GlobalVar.testParams["mwrRequestId"] is None:
                    GlobalVar.testParams["mwrRequestId"] = payloadGenerator.generate_reqId(context)
                    Id = GlobalVar.testParams["mwrRequestId"]
            else:
                if GlobalVar.testParams["requestId"] is None:
                    GlobalVar.testParams["requestId"] = payloadGenerator.generate_reqId(context)
                    Id = GlobalVar.testParams["requestId"]

    # set request parameters- method, url, body, auth
    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}_{action}_RequestType')
    reqURL = ApiTest.setEndpoint(context, set_url(context, entity), GlobalVar.testParams.get(
        f'{entity}_{action}_{recordType}_EndPoint')).format(Id)
    print(f"{entity} Url: {reqURL}")

    # Update request body
    if recordType == "request" and action == "create":
        recordType = requestRecordType
    payloadFile = GlobalVar.testParams.get(f'{entity}_{action}_{recordType}_RequestBody')
    if bool(payloadFile):
        GlobalVar.api_dict['request_bodies'] = ApiTest.setBody(context, payloadFile, GlobalVar.testComponent[0].lower())
    else:
        GlobalVar.api_dict['request_bodies'] = None

    if "request" in recordType: recordType = "request"
    if recordType == "request" and action == "create":
        if "mwr" in requestRecordType:
            GlobalVar.api_dict['request_bodies']['id'] = GlobalVar.testParams["mwrRequestId"]
        else:
            GlobalVar.api_dict['request_bodies']['id'] = GlobalVar.testParams["requestId"]

    if recordType == "csid" and action == "create":
        if GlobalVar.testParams["requestId"] is not None:
            GlobalVar.api_dict['request_bodies']["associated-requests"] = [{"id": GlobalVar.testParams["requestId"]}]
            if GlobalVar.testParams["mwrRequestId"] is not None:
                GlobalVar.api_dict['request_bodies']["associated-requests"].append(
                    {"id": GlobalVar.testParams["mwrRequestId"]})
    # print(GlobalVar.api_dict['request_bodies'])

    # send request and store response
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, reqURL, GlobalVar.api_dict[
        'request_bodies'], context.config.get(f"{entity}_User"), context.config.get(f"{entity}_Pass"))
    print(GlobalVar.response.status_code, GlobalVar.response.text)

    # validate response code
    assert ApiTest.validateResponseCode(context, GlobalVar.response,
                                        GlobalVar.testParams.get(f'{entity}_{action}_ResponseCode'))


@step('Read the "{precedence}" values for associated "{param}" values')
def read_service_params(context, precedence, param):
    global prefix, speed
    if param == "prefix":
        prefixesList = \
            GlobalVar.response.json()["hits"]["hits"][0]["_source"]["sites"]["site"][0]["vpn-policies"]["vpn-policy"][
                0][
                "entries"]
        for i in range(len(prefixesList)):
            prefix[precedence].update(
                {prefixesList[i]["id"]: prefixesList[i]["filters"]["filter"][0]["ipv4-lan-prefix"]})
        serviceParams.update({param: prefix})

    if param == "speed":
        speedList = \
            GlobalVar.response.json()["hits"]["hits"][0]["_source"]["sites"]["site"][0]["site-network-accesses"][
                "site-network-access"]
        for i in range(len(speedList)):
            speed[precedence].update({f"site-network-access-id-{str(i + 1)}": {
                "svc-output-bandwidth": speedList[i]["service"]["svc-output-bandwidth"],
                "svc-input-bandwidth": speedList[i]["service"]["svc-input-bandwidth"]}})
        serviceParams.update({param: speed})


@step('Validate that the "{before}" and "{after}" values for "{param}" is "{status}"')
def validate_update_params(context, before, after, param, status):
    if status == "same":
        assert serviceParams[param][before] == serviceParams[param][after]
    else:
        assert serviceParams[param][before] != serviceParams[param][after]


@step('Validate that a "{node}" is "{state}" the "{recordType}" record')
def step_impl(context, node, state, recordType):
    nodeList = GlobalVar.response.json()["hits"]["hits"][0]["_source"]["node-id"]
    print(f"Current Nodes List: {nodeList}")
    if "added" in state:
        assert GlobalVar.testParams[node] in nodeList
    else:
        assert GlobalVar.testParams[node] not in nodeList


@step('I validate that the "{recordType}" record has "{value}" "{field}" records for "{serviceType}"')
def step_impl(context, recordType, value, field, serviceType):
    siteList = GlobalVar.response.json()["hits"]["hits"][0]["_source"]["sites"]["site"][0]["site-network-accesses"][
        field]
    print(f"Current Nodes: {len(siteList)}")
    assert len(siteList) == int(value)
