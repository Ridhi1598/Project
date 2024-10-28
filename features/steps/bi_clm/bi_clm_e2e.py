from behave import *
from features.steps.bi_clm.bi_clm_ingestion import *
from common.util.api_test import ApiTest
from common.util.ymlReader import ReadYMLFile
from common.util.config import ConfigReader
from common.util.deviceConnect import DeviceConnect
from datetime import timedelta
from behave import *
import os

# Declared Variables
deviceInfo = {}
Id = None
# End of Declared Variables


@step('I "{action}" that the request "{status}" is "{requestStatus}"')
def fetch_req_status(context, action, status, requestStatus):
    if "display" in GlobalVar.scenario: action = "display"
    GlobalVar.requestType = GlobalVar.testParams.get(f'{action}RequestType')
    reqEndpoint = GlobalVar.testParams.get(f'{action}EndPoint')
    generate_access_token(context)
    headers = set_header_request(context, 'Authorization', access_token)
    url = set_url(context, action)
    waitTime = GlobalVar.testParams.get('Wait-Time')
    endpoint = ApiTest.setEndpoint(context, url, reqEndpoint.format(GlobalVar.requestId))
    param = ApiTest.setParams(context, GlobalVar.testParams.get(f"QueryParams_{action}"), GlobalVar.testComponent[0])
    print(f"waiting for {str(waitTime)} seconds")
    time.sleep(int(waitTime))
    GlobalVar.response = ApiTest.sendRequest(context, GlobalVar.requestType, endpoint, param, headers)
    assert ApiTest.validateResponseCode(context, GlobalVar.response, GlobalVar.testParams.get(f'{action}ResponseCode'))

    if "display" not in GlobalVar.scenario:
        if GlobalVar.response.json().get(status) != requestStatus:
            if GlobalVar.response.json().get(status) == "submitted":
                if datetime.datetime.now() <= actionEndTime:
                    fetch_req_status(context, action, status, requestStatus)
            else:
                # wait for the rollback operations to go ahead in case of failure/timeout
                print(GlobalVar.response.text)
                print("Waiting for rollback operations to be completed")
                time.sleep(300)
                raise AssertionError
    else:
        status = GlobalVar.response.json()["event"]["service"]["status"]
        if status != "success":
            if status == "in-progress":
                if datetime.datetime.now() <= actionEndTime:
                    fetch_req_status(context, action, status, requestStatus)
            else:
                raise AssertionError


@step('I prepare "{source}" connection information for "{type}"')
def device_info(context, source, type):
    global deviceInfo
    # read and load the device info file
    deviceInfoFile = GlobalVar.testParams.get(f'{source}Info')
    deviceInfo = ConfigReader.configFileReader(context, deviceInfoFile)

    # update the device parameter info
    deviceInfo["username"] = ReadYMLFile.readEnvVar(context).get('TestUserName')
    deviceInfo["password"] = ReadYMLFile.readEnvVar(context).get('TestUserPass')
    deviceInfo["device_type"] = GlobalVar.testParams.get(f'{source}Type')
    deviceInfo["host"] = GlobalVar.testParams.get(type)


@step('I create "{connType}" connection with "{source}"')
def create_conn(context, connType, source):
    # call method to establish ssh connection
    if connType == "ssh":
        GlobalVar.connection = DeviceConnect.connect(context, deviceInfo, GlobalVar.testParams.get(source))
    elif connType == "sftp":
        GlobalVar.connection = DeviceConnect.sftp(context, deviceInfo)
    return GlobalVar.connection


@step('I close "{connType}" connection with "{source}"')
def close_conn(context, connType, source):
    DeviceConnect.stop(context, GlobalVar.connection, connType)


@step('I download device "{config}" for "{scenario}" scenario for "{type}" for "{action}" service')
def fetch_config(context, config, scenario, type, action):
    GlobalVar.testParams[GlobalVar.test_case][f'{scenario}_{config}_{type}_{action}'] = \
        DeviceConnect.fetch_config(context, GlobalVar.connection, scenario, GlobalVar.test_case, type, GlobalVar.testParams.get(type), action)

@step('I create "{connType}" connection with "{deviceType}" "{source}" and download "{scenario}" "{config}" for "{action}" scenario')
def device_config(context, connType, deviceType, source, scenario, config, action):
    fileDiffFlag = False
    if "mwr" not in str(context.feature.filename).lower():
        if "execute" in action:
            fileDiffFlag = True
    else:
        if "execute" in action:
            if "mwr" in deviceType:
                if "create" not in action:
                    fileDiffFlag = True
            else:
                fileDiffFlag = True
        elif "mwr" in action:
            fileDiffFlag = True

    if fileDiffFlag:
            device_info(context, source, deviceType)
            create_conn(context, connType, source)
            fetch_config(context, config, scenario, deviceType, action)
            close_conn(context, connType, source)
    else:
        print("INFO: Skip step: Download config not required")


@step('I find the diff between the "{before}" and "{after}" config for "{type}" for "{action}" service')
def step_impl(context, before, after, type, action):
    fileDiffFlag = False
    if "mwr" not in str(context.feature.filename).lower():
        if "execute" in action:
            fileDiffFlag = True
    else:
        if "execute" in action:
            if "mwr" in type:
                if "create" not in action:
                    fileDiffFlag = True
            else:
                fileDiffFlag = True
        elif "mwr" in action:
            fileDiffFlag = True

    if fileDiffFlag:
        beforeFile = GlobalVar.testParams[GlobalVar.test_case][f'{before}_config_{type}_{action}']
        afterFile = GlobalVar.testParams[GlobalVar.test_case][f'{after}_config_{type}_{action}']
        GlobalVar.testParams[GlobalVar.test_case][f'configDiff_{type}'] = FileCompare.find_config_diff(
            context, beforeFile, afterFile, GlobalVar.test_case, type, action)
    else:
        print("INFO: Skip step: Action not required")


@step('I validate that the "{actual_diff}" is successfully matched with "{expected_diff}" for "{type}" for "{action}" service')
def step_impl(context, actual_diff, expected_diff, type, action):
    fileDiffFlag = False
    if "mwr" not in str(context.feature.filename).lower():
        if "execute" in action:
            fileDiffFlag = True
    else:
        if "execute" in action:
            if "mwr" in type:
                if "create" not in action:
                    fileDiffFlag = True
            else:
                fileDiffFlag = True
        elif "mwr" in action:
            fileDiffFlag = True

    if fileDiffFlag:
        assert FileCompare.compare_config_diff(context, GlobalVar.testParams[GlobalVar.test_case][f'configDiff_{type}'],
                                               GlobalVar.test_case, type, action)
    else:
        print("INFO: Skip step: Action not required")


@step('I Set "{component}" api endpoint for "{action}" service')
def set_action_endpoint(context, component, action):
    global serviceId, mwrId
    endpoint = ''
    serviceId = GlobalVar.testParams.get('serviceId')
    mwrId = GlobalVar.testParams.get('mwrId')
    GlobalVar.requestType = GlobalVar.testParams.get(f'{action}RequestType')
    if action == "execute" or action == "display":
        endpoint = GlobalVar.testParams.get(f'{action}EndPoint').format(GlobalVar.requestId)
    elif action == "rollback":
        endpoint = GlobalVar.testParams.get(f'{action}EndPoint').format(serviceId, GlobalVar.testParams.get(f'{action}Version'))
    elif "mwr" in action:
        endpoint = GlobalVar.testParams.get(f'{action}EndPoint').format(serviceId, mwrId)
    else:
        endpoint = GlobalVar.testParams.get(f'{action}EndPoint').format(serviceId)
    GlobalVar.api_dict[f'{GlobalVar.requestType}_URL'] = ''.join([GlobalVar.api_url, endpoint])
    print("{} {} request URL: {}".format(component.title(), GlobalVar.requestType.lower(),
                                         GlobalVar.api_dict[f'{GlobalVar.requestType}_URL']))


@step('I Set "{component}" api request body for "{action}" service')
def set_action_body(context, component, action):
    filename = GlobalVar.testParams.get(f'{action}RequestBody').format(sys.argv[2])
    if not bool(filename):
        GlobalVar.api_dict['payload'] = None
    else:
        GlobalVar.api_dict['payload'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], filename)

        if "e2e" in GlobalVar.testComponent[0]:
            if "execute" not in action:
                if "mwr" not in action:
                    GlobalVar.api_dict['payload'] = payloadGenerator.update_payload_message(context, GlobalVar.api_dict['payload'], GlobalVar.testParams)
                else:
                    GlobalVar.api_dict['payload'] = payloadGenerator.update_mwr_payload_message(context, GlobalVar.api_dict['payload'], GlobalVar.testParams)

def set_action_body_tinaa(context, component, action):
    filename = GlobalVar.testParams.get(f'{action}RequestBody').format(sys.argv[2])
    if not bool(filename):
        GlobalVar.api_dict['payload'] = None
    else:
        GlobalVar.api_dict['payload'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], filename)

@step('I fetch "{recordType}" record for "{status}" operation from "{entity}" records')
def fetch_service_status(context, recordType, status, entity):
    # set service/request Id
    if recordType == "service": Id = GlobalVar.testParams.get("serviceId")
    if recordType == "request": Id = GlobalVar.requestId

    # set request parameters- method, url, body, auth
    GlobalVar.requestType = GlobalVar.testParams.get(f'{entity}RequestType')
    reqEndpoint = GlobalVar.testParams.get(f'{entity}EndPoint')
    reqURL = ApiTest.setEndpoint(context, set_url(context, entity), reqEndpoint.format(Id))
    username = context.config.get(f"{entity}_User")
    password = context.config.get(f"{entity}_Pass")
    GlobalVar.api_dict['request_bodies'] = ApiTest.setBody(context, GlobalVar.testParams.get(f'{entity}_RequestBody'), GlobalVar.testComponent[0].lower())

    # add wait for service record update
    time.sleep(12)

    # send request and store response
    GlobalVar.response = ApiTest.sendRequestAuth(context, GlobalVar.requestType, reqURL, GlobalVar.api_dict['request_bodies'], username, password)

    # validate response values
    if GlobalVar.response.json()["found"]:
        GlobalVar.state["state"] = GlobalVar.response.json()["_source"]["state"]
        GlobalVar.state["in-progress"] = GlobalVar.response.json()["_source"]["in-progress"]
        GlobalVar.state["versions"] = GlobalVar.response.json()["_source"]["associated-versions"]
        GlobalVar.state["mwr-state"] = GlobalVar.response.json()["_source"]["mwr-state"]
        return GlobalVar.state


@step('I send request for "{action}" "{recordType}" via "{component}"')
def action_on_service(context, action, recordType, component, value=''):
    global actionEndTime
    if "display" in action: action = "display"
    if "execute" in action: action = "execute"

    # send Http request if service is in expected state
    if currentServiceStateFlag:
        # set request parameters
        set_url(context, component)
        set_controller_headers(context, "Content", "Authorization")
        set_action_endpoint(context, component, action)
        if "-tinaa" in context.feature.filename:
            set_action_body_tinaa(context, component, action)
        else:
            set_action_body(context, component, action)

        if action == "display": set_action_param(context, component, action, value='')
        else: set_action_param(context, component, action, value='')

        GlobalVar.response = ApiTest.sendRequestjson(context, GlobalVar.requestType, GlobalVar.api_dict[f'{GlobalVar.requestType}_URL'], GlobalVar.api_dict['request_header'], GlobalVar.api_dict['request_params'], GlobalVar.api_dict['payload'])
        print(GlobalVar.response.text)

        # validate response schema and status code
        assert ApiTest.validateResponseCode(context, GlobalVar.response, GlobalVar.testParams.get('ResponseCode'))

        if action == "display" or action == "execute":
            schemaFile = GlobalVar.testParams.get(f"{action}SchemaFile")
        else: schemaFile = GlobalVar.testParams.get("SchemaFile")

        assert ApiTest.validateResponseSchema(context, GlobalVar.response, schemaFile, GlobalVar.testComponent[0])

        # convert and store response in json object
        response_json[GlobalVar.requestType] = GlobalVar.response.json()
        actionEndTime = datetime.datetime.now() + timedelta(minutes=int(GlobalVar.testParams.get("timeout")))

    else:
        raise ValueError("Service not in expected state..!!")


@step('I validate that "{recordType}" is in expected state for "{action}" operation')
def validate_expected_state(context, recordType, action):
    GlobalVar.scenario = action
    global currentServiceStateFlag
    # currentServiceStateFlag = True
    currentServiceStateFlag = False
    currentServiceState = fetch_service_status(context, recordType, action, "ES")
    print(f"Current Service State: {currentServiceState.get('state')}")
    print(f"In_Progress State: {currentServiceState.get('in-progress')}")
    if action == "create" and currentServiceState.get('state') not in ["active", "inactive"]:
        if not currentServiceState.get('in-progress'):
            currentServiceStateFlag = True
    if action == "delete" or action == "update" or action == "rollback":
        if currentServiceState["state"] in ["active", "inactive"]:
            if not currentServiceState.get('in-progress'):
                currentServiceStateFlag = True
    if "display" in action:
        if currentServiceState.get('in-progress'):
            currentServiceStateFlag = True
    if "execute" in action:
        if currentServiceState.get('in-progress'):
            currentServiceStateFlag = True
    if "add_mwr" in action:
        if currentServiceState["state"] in ["active", "inactive"]:
            if not currentServiceState.get('in-progress'):
                if currentServiceState.get('mwr-state') == "inactive":
                    currentServiceStateFlag = True
    if "delete_mwr" in action:
        if currentServiceState["state"] in ["active", "inactive"]:
            if not currentServiceState.get('in-progress'):
                if currentServiceState.get('mwr-state') == "active":
                    currentServiceStateFlag = True
    print(f"Service in Expected State for {action} operation: {currentServiceStateFlag}")
    assert currentServiceStateFlag


@step('I validate that service record state for "{action}" is as expected')
def validate_service_state(context, action):
    print(f"Current Service State: {GlobalVar.state['state']}")
    if action == "delete-execute":
        assert GlobalVar.state['state'] in ["terminated", None]
        assert GlobalVar.state['mwr-state'] in ["terminated", "inactive"]
    elif action == "delete_mwr":
        assert GlobalVar.state['state'] in ["active", "inactive"]
        assert GlobalVar.state['mwr-state'] in ["terminated", "inactive"]
    elif action == "add_mwr":
        assert GlobalVar.state['state'] in ["active", "inactive"]
        assert GlobalVar.state['mwr-state'] == "active"
    else:
        assert GlobalVar.state['state'] in ["active", "inactive"]


@step('Validate the "{current}" and "{expected}" "{config}" in case of "{action}"')
def validate_display_config(context, current, expected, config, action):
    if action in GlobalVar.scenario:
        config = GlobalVar.response.json()["event"]["service"]["response"]

        dest_Folder = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + f"/resources/deviceConfigs/{sys.argv[1]}/reConfigs/TC_{GlobalVar.test_case}"
        if not os.path.exists(dest_Folder):
            os.mkdir(dest_Folder)

        configFileLoc = dest_Folder + f'/tc{GlobalVar.test_case}_{GlobalVar.scenario}_config_{sys.argv[2]}.json'

        with open(configFileLoc, "w") as f:
            f.write(json.dumps(config, indent=4))

        # config validation
        assert FileCompare.display_config_diff(context, configFileLoc, GlobalVar.test_case)
        print(f"display config matched successfully for testcase {GlobalVar.test_case}")
        context.scenario.skip(reason="no further action required for display scenario")


        # config[current] = GlobalVar.response.json()["event"]["service"]["response"][f"{current}-config"]
        # config[expected] = GlobalVar.response.json()["event"]["service"]["response"][f"{expected}-config"]
        #
        # # config validation
        # assert FileCompare.compare_display_diff(context, config, GlobalVar.test_case, current, str(context.feature.filename).lower())
        # print(f"Current config matched successfully for testcase {GlobalVar.test_case}")
        # assert FileCompare.compare_display_diff(context, config, GlobalVar.test_case, expected, str(context.feature.filename).lower())

