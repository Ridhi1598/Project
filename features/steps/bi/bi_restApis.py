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

import urllib3
from behave import given, when, then, step
from jsonschema import validate
from requests import HTTPError
from features.steps.globalVar import GlobalVar
from features.steps.bi.bi_uiFunctional import *
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
from common.util.fileCompare import FileCompare
from features.steps.globalVar import GlobalVar

# declared variables
api_endpoints = {}
request_headers = {}
response_codes = {}
response_texts = {}
response_json = {}
request_bodies = {}
responseVar = None
payload = {}
access_token = None
testParams = {}
executedTestCases = []
request_Id = {}
configFiles = {}
requestState = None
serviceState = []
testScenario = None
testcase = None
ESRequestType = 'GET'
serviceId = None


# end of declared variables


@step('I read service id for test case sequence')
def read_service_id(context):
    global serviceId
    featureTest = str(context.feature).split('"')[1].split(' ')
    GlobalVar.baseTest = featureTest[0].split('_')[1]
    serviceId = context.csvRead[int(GlobalVar.baseTest) - 1].get('telus-cust-service-id')


@step('I read test data for "{testCaseNumber}"')
def read_test_data(context, testCaseNumber):
    GlobalVar.testParams = context.csvRead[int(testCaseNumber) - 1]


@step('I generate access token for authorization')
def generate_access_token(context):
    set_endpoint(context)
    GlobalVar.api_dict['request_header'] = set_header_request(context, 'Content-Type', GlobalVar.testParams.get("authContentType"))
    fileName = GlobalVar.testParams.get("authPayload")
    GlobalVar.api_dict['request_bodies'] = payloadGenerator.load_payload_message(context, GlobalVar.testComponent[0], fileName)
    for retry in range(5):
        if int(post_request_authorization(context)) != context.config.get('authorizationAPIResponse'):
            print(f"Generating Access token failed. Retry {str(retry + 1)} after 5 seconds")
            time.sleep(5)
        else: break
    GlobalVar.access_token = get_access_token(context)
    return GlobalVar.access_token


@step(u'I Set POST posts api endpoint for authorization')
def set_endpoint(context):
    GlobalVar.api_dict['api_endpoint_post_url'] = context.config.get('tinaa_auth_url')


@step(u'Send POST HTTP request for authorization')
def post_request_authorization(context):
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(url=GlobalVar.api_dict['api_endpoint_post_url'],
                                 data=GlobalVar.api_dict['request_bodies'], verify=False)

        response_codes['POST'] = response.status_code
        response_json['POST'] = response.json()
        return response_codes['POST']

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I extract response value of access_token')
def get_access_token(context):
    return response_json['POST']['access_token']


@step('I set BI "{apiType}" url')
def set_API_type(context, apiType):
    url = None
    if apiType == 'REST':
        url = '{}APIURL_{}'.format(sys.argv[1], sys.argv[2])
    elif apiType == 'controller':
        url = '{}ControllerURL_{}'.format(sys.argv[1], sys.argv[2])
    elif apiType == 'RMQ':
        url = '{}_RMQ_{}'.format(sys.argv[1], sys.argv[2])
    elif apiType == 'ES':
        url = 'ES_{}'.format(sys.argv[2])
    GlobalVar.api_url = context.config.get(url)
    return GlobalVar.api_url


@step('I Set "{requestType}" api endpoint for testcase "{testCase}"')
def set_API_endpoint(context, requestType, testCase):
    global testcase, serviceId

    # read test data from the global dictionary
    testcase = GlobalVar.testParams.get('Testcase')
    rollbackTestcase = GlobalVar.testParams.get('rollbackTestcase')
    assert testcase == testCase

    requestType = GlobalVar.testParams.get('Request-Type')
    endpoint = GlobalVar.testParams.get('Endpoint')

    if "delete" in requestType.lower():
        if bool(GlobalVar.testParams.get('telus-cust-service-id')):
            if serviceId != GlobalVar.testParams.get('telus-cust-service-id'):
                serviceId = GlobalVar.testParams.get('telus-cust-service-id')

    # set API endpoint wrt the test scenario
    if endpoint == '/bi/mpls/v1/service':
        api_endpoints[requestType + '_URL'] = GlobalVar.api_url + endpoint

    if endpoint == '/bi/mpls/v1/service/{}' or endpoint == '/bi/mpls/v1/service/{}/activate':
        api_endpoints[requestType + '_URL'] = GlobalVar.api_url + endpoint.format(serviceId)

    if endpoint == '/bi/mpls/v1/service/{0}/mwr/{1}':
        api_endpoints[requestType + '_URL'] = GlobalVar.api_url + endpoint.format(
            serviceId, GlobalVar.testParams.get("mwrId"))

    if endpoint == '/bi/mpls/v1/requests/request/{}/rollback':
        api_endpoints[requestType + '_URL'] = GlobalVar.api_url + endpoint.format(
            request_Id[GlobalVar.baseTest][rollbackTestcase])

    # save API URL in another global dictionary
    GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = api_endpoints[requestType + '_URL']
    print("Request URL: {}".format(GlobalVar.api_dict['api_endpoint_' + requestType + '_url']))


@step('I Set HEADER param request "{header}" as "{header_content_type}" for BI')
def set_header_request(context, header, header_content_type):
    if header == 'Authorization':
        if GlobalVar.testParams.get('Authorization') == 'Bearer Token':
            header_content_type = 'Bearer ' + GlobalVar.access_token
        else:
            header_content_type = GlobalVar.testParams.get('Authorization')
    request_headers[header] = header_content_type
    GlobalVar.api_dict['request_header'] = request_headers
    return GlobalVar.api_dict['request_header']


@step('Send HTTP request for BI')
def send_HTTP_request(context):
    global serviceState, request_Id, testScenario

    requestType = GlobalVar.testParams.get('Request-Type')
    testScenario = GlobalVar.testParams['Scenario Type']
    print("Sending ", requestType, " request")

    try:
        response = None
        urllib3.disable_warnings(InsecureRequestWarning)
        if requestType == 'POST':
            # in case of rollback scenario previous request state should be completed
            if testScenario == 'rollback' and requestState == 'completed':
                response = requests.post(
                    url=GlobalVar.api_dict.get("api_endpoint_" + GlobalVar.testParams['Request-Type'] + "_url"),
                    headers=GlobalVar.api_dict.get("request_header"),
                    json=GlobalVar.api_dict.get("payload"), verify=False)
            else:
                response = requests.post(
                    url=GlobalVar.api_dict.get("api_endpoint_" + GlobalVar.testParams['Request-Type'] + "_url"),
                    headers=GlobalVar.api_dict.get("request_header"),
                    json=GlobalVar.api_dict.get("payload"), verify=False)
        if requestType == 'PUT':
            # Check if service exist
            serviceState = check_service_state(context, serviceId)
            if serviceState[0]:
                response = requests.put(
                    url=GlobalVar.api_dict.get("api_endpoint_" + GlobalVar.testParams['Request-Type'] + "_url"),
                    headers=GlobalVar.api_dict.get("request_header"),
                    json=GlobalVar.api_dict.get("payload"), verify=False)
        if requestType == 'DELETE':
            # Check if service exist
            sendReq = False
            serviceState = check_service_state(context, serviceId)
            if testScenario == 'delete service' and serviceState[0]: sendReq = True
            if testScenario == 'Remove_MWR' and serviceState[0] and serviceState[1] is not None: sendReq = True
            if sendReq:
                response = requests.delete(
                    url=GlobalVar.api_dict.get("api_endpoint_" + GlobalVar.testParams['Request-Type'] + "_url"),
                    headers=GlobalVar.api_dict.get("request_header"), verify=False)

        print("Request response text: {}".format(response.text))

        # extract response and validate response code
        response_codes[requestType] = response.status_code
        response_json[requestType] = response.json()

        print("Request response json: {}".format(response_json[requestType]))

        responseCodeVar = '{0}_{1}_Response'.format(sys.argv[1], requestType)
        validate_response_code(context, int(response_codes[requestType]), context.config.get(responseCodeVar))

        # extract request id for asynchronous response tracking
        if request_Id == {}:
            request_Id = {GlobalVar.baseTest: {testcase: response_json[requestType]['requestId']}}
        else:
            if GlobalVar.baseTest not in request_Id:
                request_Id[GlobalVar.baseTest] = {testcase: response_json[requestType]['requestId']}
            else:
                request_Id[GlobalVar.baseTest][testcase] = response_json[requestType]['requestId']

        print("Request Id for testcase {} : {}".format(testcase, request_Id[GlobalVar.baseTest][testcase]))

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


@step('I validate the controller response as "{expectedValue}"')
def validate_controller_response(context, expectedValue):
    global requestState, ESRequestType
    # try:
        # Validate if request Id exists and request is valid
    if request_Id[GlobalVar.baseTest][testcase] is not None:
        if not (requestType == 'DELETE' and not serviceState[0]):
            print("Finding controller response for : {}".format(testScenario))
            # Waiting for Controller Response
            waitTime = GlobalVar.testParams['Wait-Time']
            print("Waiting for {} seconds...".format(waitTime))
            time.sleep(int(waitTime))

            # Define params for Monitor API
            generate_access_token(context)

            url_monitor = 'monitorAPIURL_{}'.format(sys.argv[2])
            url = context.config.get(url_monitor) + request_Id[GlobalVar.baseTest][testcase]

            print("Monitor API URL: {}".format(url))
            set_header_request(context, 'Authorization', access_token)

            # Send API Request After Required Wait
            urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.request(method=ESRequestType, url=url,
                                        headers=GlobalVar.api_dict.get("request_header"), verify=False)

            # Extracting Response from Monitor API
            response_codes[ESRequestType] = response.status_code
            response_json[ESRequestType] = response.json()

            # Validate Response Code
            validate_response_code(context, int(response_codes[ESRequestType]),
                                   context.config.get('monitorAPIResponse'))
            requestState = response_json[ESRequestType]['state']
            print('BI Service Request State: ', requestState)

            if requestState == 'submitted':
                validate_controller_response(context, expectedValue)
                # If Delete fails exit the process

            else:
                if requestType == 'DELETE':
                    if requestState == 'failed' or requestState == 'timeout':
                        context.feature.skip(reason='Reason: delete request failure')
                        sys.exit("Delete Failed...Exiting Process Now")
                else:
                    assert requestState == expectedValue

        else:
            print("Service does not exist")
    else:
        print("Request does not exist")

    # except AssertionError:
    #     raise AssertionError
    #
    # except HTTPError as http_err:
    #     print(f'Failing test case at request completion: {str(testcase)}')
    #     print(f'HTTP error occurred: {http_err}')
    #     raise http_err
    #
    # except Exception as err:
    #     print(f'Other error occurred: {err}')
    #     raise err


@step('Set request Body for BI')
def set_request_body(context):
    global requestType
    requestType = GlobalVar.testParams.get('Request-Type')

    # set request body for post and put request
    if requestType == 'DELETE':
        GlobalVar.api_dict['payload'] = None

    elif requestType == 'POST' or 'PUT':
        filename = GlobalVar.testParams.get('Payload')
        if bool(filename):
            GlobalVar.api_dict['payload'] = payloadGenerator.load_payload_message(
                context, GlobalVar.testComponent[0], filename)
            # GlobalVar.api_dict['payload'] = payloadGenerator.update_payload_message(
            #     context, GlobalVar.api_dict['payload'], GlobalVar.testParams)
        else:
            GlobalVar.api_dict['payload'] = None


@step('I download config files for testcase "{testcase}"')
def generate_config_files(context, testcase):
    global configFiles, tcFolderName
    if requestState == 'completed':
        # set required parameters for config generation
        baseDeviceType = GlobalVar.testParams['Vendor']
        baseDeviceName = GlobalVar.testParams['Base-Device']
        deviceType = GlobalVar.testParams['Device Type']
        deviceName = GlobalVar.testParams['telus-pe-device-reference']
        accessType = GlobalVar.testParams['Access Type']
        hostName = deviceType.lower() + '_' + deviceName + '_RemoteHost'
        deviceHostname = context.config.get(hostName)
        basehostName = baseDeviceType.lower() + '_' + baseDeviceName + '_RemoteHost'
        basedeviceHostname = context.config.get(basehostName)
        username = context.envReader.get('TestUserName')
        password = context.envReader.get('TestUserPass')
        port = context.config.get('port')
        tcFolderName = 'TC_' + GlobalVar.baseTest
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        # create parent folder for test case
        parentFolder = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + \
                       '/resources/deviceConfigs/' + sys.argv[1] + '/reConfigs/' + tcFolderName
        if not os.path.exists(parentFolder):
            os.mkdir(parentFolder)

        # create sub folders for test cases running in the sequence
        subFolder = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + \
                    '/resources/deviceConfigs/' + sys.argv[1] + '/reConfigs/' + tcFolderName + '/tc_' + str(testcase)
        if not os.path.exists(subFolder):
            os.mkdir(subFolder)
        try:
            # Create SFTP connection and define current working directory for remote location
            with pysftp.Connection(host=deviceHostname, username=username,
                                   password=password, port=port, cnopts=cnopts) as sftp:
                print("SFTP Connection set up successfully")
                remoteWorkingDirectory = context.config.get(deviceType.lower() + '_remoteDirectory')
                sftp.cwd(remoteWorkingDirectory)

                if deviceType == 'Nokia':
                    # download new config file(.cfg) from remote location
                    remoteFilePath_New = context.config.get(deviceType.lower() + '_RemoteFilePathNew')
                    localFilePath_New = subFolder + '/config_tc' + str(testcase) + 'New.cfg'
                    configFiles[testcase + '_New'] = localFilePath_New
                    print("Downloading updated config file...")
                    sftp.get(remoteFilePath_New, localFilePath_New)

                    # download old config file(.cfg.1) from remote location
                    remoteFilePath_Old = context.config.get(deviceType.lower() + '_RemoteFilePathOld')
                    localFilePath_Old = subFolder + '/config_tc' + str(testcase) + 'Old.cfg'
                    configFiles[testcase + '_Old'] = localFilePath_Old
                    sftp.get(remoteFilePath_Old, localFilePath_Old)
                    print("Downloading old config file...")

                    if 'rollback' in testScenario:
                        # download older config file(.cfg.2) from remote location
                        remoteFilePath_Older = context.config.get(deviceType.lower() + '_RemoteFilePathOlder')
                        localFilePath_Older = subFolder + '/config_tc' + str(testcase) + 'Older.cfg'
                        configFiles[testcase + '_Older'] = localFilePath_Older
                        sftp.get(remoteFilePath_Older, localFilePath_Older)
                        print("Downloading older config file...")
                        sftp.get(remoteFilePath_Older, localFilePath_Older)
                        time.sleep(5)

                elif deviceType == 'Juniper':
                    # download new config file zipped folder(.conf.gz) and extract config file(.conf) from remote location
                    remoteFilePath_New = context.config.get(deviceType.lower() + '_RemoteFilePathNew')
                    localFilePath_New = subFolder + '/juniper' + str(testcase) + 'New.conf.gz'
                    print("Downloading updated config file...")
                    sftp.get(remoteFilePath_New, localFilePath_New)

                    extractedFilePath_New = subFolder + '/juniper' + str(testcase) + 'New.conf'
                    configFiles[testcase + '_New'] = extractedFilePath_New

                    with gzip.open(localFilePath_New, 'rb') as f_in:
                        with open(extractedFilePath_New, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)

                    # download old config file zipped folder(conf.gz.1) and extract config file(.conf) from remote location
                    remoteFilePath_Old = context.config.get(deviceType.lower() + '_RemoteFilePathOld')
                    localFilePath_Old = subFolder + '/juniper' + str(testcase) + 'Old.conf.1.gz'
                    print("Downloading old config file...")
                    sftp.get(remoteFilePath_Old, localFilePath_Old)

                    extractedFilePath_Old = subFolder + '/juniper' + str(testcase) + 'Old.conf'
                    configFiles[testcase + '_Old'] = extractedFilePath_Old

                    with gzip.open(localFilePath_Old, 'rb') as f_in:
                        with open(extractedFilePath_Old, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)

                    if 'rollback' in testScenario:
                        # download older config file zipped folder(conf.gz.2) and extract config file(.conf) from remote location
                        remoteFilePath_Older = context.config.get(deviceType.lower() + '_RemoteFilePathOlder')
                        localFilePath_Older = subFolder + '/juniper' + str(testcase) + 'Old.conf.2.gz'
                        print("Downloading older config file...")
                        sftp.get(remoteFilePath_Older, localFilePath_Older)
                        time.sleep(5)

                        extractedFilePath_Older = subFolder + '/juniper' + str(
                            testcase) + 'Older.conf'
                        configFiles[testcase + '_Older'] = extractedFilePath_Older

                        with gzip.open(localFilePath_Older, 'rb') as f_in:
                            with open(extractedFilePath_Older, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)

                # close SFTP connection
                sftp.close()
                print("Files Downloaded, SFTP connection closed")

            # download base device config files in case of MWR scenarios and service is configured on another device
            if accessType == 'MWR' or 'mwr' in testScenario:
                # Create SFTP connection and define current working directory for remote location
                with pysftp.Connection(host=basedeviceHostname, username=username,
                                       password=password, port=port, cnopts=cnopts) as sftp:
                    print("SFTP Connection set up successfully For Base Device")
                    remoteWorkingDirectory = context.config.get(baseDeviceType.lower() + '_remoteDirectory')
                    sftp.cwd(remoteWorkingDirectory)

                    if baseDeviceType == 'Nokia':
                        # download new config file(.cfg) from remote location
                        remoteFilePath_New = context.config.get(baseDeviceType.lower() + '_RemoteFilePathNew')
                        localFilePath_New = dirname(os.path.abspath(
                            os.path.join(os.path.dirname(__file__),
                                         "../.."))) + '/resources/deviceConfigs/bi/reConfigs/' \
                                            + tcFolderName + '/tc_' + str(testcase) + '/BaseDeviceConfig_tc' + str(
                            testcase) + 'New.cfg'
                        configFiles[testcase + '_MWRBase_New'] = localFilePath_New
                        print("Downloading updated base device config file...")
                        sftp.get(remoteFilePath_New, localFilePath_New)
                        time.sleep(5)

                        # download old config file(.cfg.1) from remote location
                        remoteFilePath_Old = context.config.get(baseDeviceType.lower() + '_RemoteFilePathOld')
                        localFilePath_Old = dirname(os.path.abspath(
                            os.path.join(os.path.dirname(__file__),
                                         "../.."))) + '/resources/deviceConfigs/bi/reConfigs/' \
                                            + tcFolderName + '/tc_' + str(testcase) + '/BaseDeviceConfig_tc' + str(
                            testcase) + 'Old.cfg'
                        configFiles[testcase + '_MWRBase_Old'] = localFilePath_Old
                        print("Downloading old base device config file...")
                        sftp.get(remoteFilePath_Old, localFilePath_Old)
                        time.sleep(5)

                        if 'rollback' in testScenario:
                            # download older config file(.cfg.2) from remote location
                            remoteFilePath_Older = context.config.get(baseDeviceType.lower() + '_RemoteFilePathOlder')
                            localFilePath_Older = subFolder + '/BaseDeviceConfig_tc' + str(
                                testcase) + 'Older.cfg'
                            configFiles[testcase + '_MWRBase_Older'] = localFilePath_Older
                            sftp.get(remoteFilePath_Older, localFilePath_Older)
                            print("Downloading older base device config file...")
                            sftp.get(remoteFilePath_Older, localFilePath_Older)
                            time.sleep(5)

                    elif baseDeviceType == 'Juniper':
                        # download new config file zipped folder(conf.gz) and extract config file(.conf) from remote location
                        remoteFilePath_New = context.config.get(baseDeviceType.lower() + '_RemoteFilePathNew')
                        localFilePath_New = subFolder + '/BaseDeviceConfig_tc' + str(testcase) + 'New.conf.gz'
                        print("Downloading updated base device config file...")
                        sftp.get(remoteFilePath_New, localFilePath_New)
                        time.sleep(5)

                        extractedFilePath_New = subFolder + '/BaseDeviceConfig_tc' + str(
                            testcase) + 'New.conf'
                        configFiles[testcase + '_MWRBase_New'] = extractedFilePath_New

                        with gzip.open(localFilePath_New, 'rb') as f_in:
                            with open(extractedFilePath_New, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)

                        # download old config file zipped folder(conf.gz.1) and extract config file(.conf) from remote location
                        remoteFilePath_Old = context.config.get(baseDeviceType.lower() + '_RemoteFilePathOld')
                        localFilePath_Old = subFolder + '/BaseDeviceConfig_tc' + str(testcase) + 'Old.conf.1.gz'
                        print("Downloading old base device config file...")
                        sftp.get(remoteFilePath_Old, localFilePath_Old)
                        time.sleep(5)

                        extractedFilePath_Old = subFolder + '/BaseDeviceConfig_tc' + str(testcase) + 'Old.conf'
                        configFiles[testcase + '_MWRBase_Old'] = extractedFilePath_Old

                        with gzip.open(localFilePath_Old, 'rb') as f_in:
                            with open(extractedFilePath_Old, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)

                        if 'rollback' in testScenario:
                            # download older config file zipped folder(conf.gz.2) and extract config file(.conf) from remote location
                            remoteFilePath_Older = context.config.get(baseDeviceType.lower() + '_RemoteFilePathOlder')
                            localFilePath_Older = subFolder + '/juniper' + str(testcase) + 'Older.conf.2.gz'
                            print("Downloading older base device config file...")
                            sftp.get(remoteFilePath_Older, localFilePath_Older)
                            time.sleep(5)

                            extractedFilePath_Older = subFolder + '/juniper' + str(testcase) + 'Older.conf'
                            configFiles[testcase + '_MWRBase_Older'] = extractedFilePath_Older

                            with gzip.open(localFilePath_Older, 'rb') as f_in:
                                with open(extractedFilePath_Older, 'wb') as f_out:
                                    shutil.copyfileobj(f_in, f_out)

                    # close SFTP connection
                    sftp.close()
                    print("Files Downloaded, SFTP connection closed")

        except Exception as err:
            print(err)
            raise err
    else:
        print("Request state not completed..No files downloaded")


@step('I validate the generated configurations')
def validate_configurations(context):
    if requestState == 'completed':
        try:
            testcase = GlobalVar.testParams['Testcase']
            file_New = configFiles[testcase + '_New']
            file_Old = configFiles[testcase + '_Old']

            testType = None
            # Identify testType to define baseLineDifference file to be matched against
            if 'E2E' in GlobalVar.featureFilePath:
                testType = 'E2E'
            elif 'NED' in GlobalVar.featureFilePath:
                testType = 'NED'

            # define and create file location for the difference file
            diffFileLocation = dirname(os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../.."))) + '/resources/deviceConfigs/bi/reConfigs/' \
                               + tcFolderName + '/tc_' + str(testcase) + '/config_Diff_' + str(testcase)

            if not os.path.exists(diffFileLocation):
                os.mkdir(diffFileLocation)

            if 'rollback' not in testScenario:
                print("Comparing files..")
                # Finding difference for test run config files
                differenceFile = FileCompare.compare_config_files(context, file_Old, file_New, diffFileLocation,
                                                                  testcase, '')

                # Comparing the difference for test run config files with base config files
                BaselineDifferenceFile = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) \
                                         + '/resources/deviceConfigs/' + sys.argv[
                                             1] + '/reConfigBaseDifferences_' + testType \
                                         + '/config_BaseDifference_' + str(testcase)

                FileCompare.compare_config_files_with_base(context, BaselineDifferenceFile, differenceFile,
                                                           diffFileLocation,
                                                           testcase, '', testScenario)

                # Finding difference for base device config files in case of MWR scenario
                if GlobalVar.testParams.get('Access Type') == 'MWR':
                    file_NewBase = configFiles[testcase + '_MWRBase_New']
                    file_OldBase = configFiles[testcase + '_MWRBase_Old']
                    differenceFile = FileCompare.compare_config_files(context, file_OldBase, file_NewBase,
                                                                      diffFileLocation,
                                                                      testcase, GlobalVar.testParams.get('Access Type'))

                    # Comparing the difference for test run config files with base config files for base device in case of MWR
                    BaselineDifferenceFile = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) \
                                             + '/resources/deviceConfigs/' + sys.argv[
                                                 1] + '/reConfigBaseDifferences_' + testType \
                                             + '/baseConfig_DiffBaseDevice_' + str(testcase)
                    FileCompare.compare_config_files_with_base(context, BaselineDifferenceFile, differenceFile,
                                                               diffFileLocation,
                                                               testcase, GlobalVar.testParams.get('Access Type'),
                                                               testScenario)
            else:
                # Compare new and older file to match completely
                file_Older = configFiles[testcase + '_Older']
                print("Comparing files for Rollback Scenario..")
                FileCompare.compare_config_files_with_base(context, file_Older, file_New, diffFileLocation, testcase,
                                                           '',
                                                           testScenario)
                # Compare new and older file for base device to match completely
                if 'mwr' in testScenario:
                    file_NewBase = configFiles[testcase + '_MWRBase_New']
                    file_OlderBase = configFiles[testcase + '_MWRBase_Older']
                    print("Compare Base Device Files for Rollback Scenario..")
                    FileCompare.compare_config_files_with_base(context, file_OlderBase, file_NewBase, diffFileLocation,
                                                               testcase, 'MWR', testScenario)

        except Exception as err:
            print(f'Failing test case at config validation: {str(testcase)}')
            print(f'Other error occurred: {err}')
            GlobalVar.biFailCounter += 1
            GlobalVar.failTest.append(testcase)
            raise err
    else:
        print("Request state not completed..No files to compare")


@step('I receive valid HTTP response code "{actual_response_code}" as "{expected_response_code}"')
def validate_response_code(context, actual_response_code, expected_response_code):
    try:
        assert actual_response_code == expected_response_code
    except Exception as err:
        raise Exception(err)


@step('Execute the request in case of update')
def execute_request(context):
    scenarioType = GlobalVar.testParams.get("Scenario Type")
    # execute request in case of modify service and rollback scenarios

    if 'modify service' in scenarioType or 'rollback' in scenarioType:
        print("Executing Request for {}".format(scenarioType))
        try:
            # generate access token and set header
            access_token = generate_access_token(context)
            set_header_request(context, 'Authorization', access_token)

            # generate url for the request
            url_Execute = 'executeAPIURL_{}'.format(sys.argv[2])
            GlobalVar.api_dict['executeURL'] = context.config.get(url_Execute).format(
                request_Id[GlobalVar.baseTest][testcase])

            print("Execute API URL: {}".format(GlobalVar.api_dict['executeURL']))

            # set request body for execute api
            payloadFile = GlobalVar.testParams.get('executePayload')

            GlobalVar.api_dict['executePayload'] = payloadGenerator.load_payload_message(
                context, GlobalVar.testComponent[0], payloadFile)

            # send API Request for execution
            urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.post(url=GlobalVar.api_dict['executeURL'],
                                     headers=GlobalVar.api_dict.get("request_header"),
                                     json=GlobalVar.api_dict['executePayload'], verify=False)

            # Extracting Response from Execute API
            response_codes['POST'] = response.status_code
            response_json['POST'] = response.json()

            # Validate Response Code
            validate_response_code(context, int(response_codes['POST']), context.config.get('executeAPIResponse'))

            # extract request execution status from the response
            executeStatus = response_json['POST']['status']
            print('BI Service Request Execute Status: {}'.format(executeStatus))
            assert executeStatus == 'success'

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')

        except Exception as err:
            print(f'Other error occurred: {err}')
            raise Exception(err)

    else:
        print("Execute not required for {}".format(scenarioType))
        pass


@step('Validate the error message coming from "{entity}"')
def validate_error(context, entity):
    expectedErrorCode = GlobalVar.testParams.get('expectedErrorCode')
    expectedErrorMessage1 = GlobalVar.testParams.get('expectedErrorMessage1')
    expectedErrorMessage2 = GlobalVar.testParams.get('expectedErrorMessage2')

    try:
        # Validate error code
        errorCode = response_json[ESRequestType]['errorCode']
        assert errorCode == expectedErrorCode

        # Validate error message
        errorMessage = response_json[ESRequestType]['message']
        try:
            assert expectedErrorMessage1 in errorMessage
        except AssertionError:
            assert expectedErrorMessage2 in errorMessage

    except Exception as err:
        raise err


@step('Validate the "{serviceId}" state')
def check_service_state(context, serviceId):
    global ESRequestType
    url_ES = '{0}_service_ES_{1}'.format(sys.argv[1], sys.argv[2])
    url = context.config.get(url_ES) + serviceId
    print("ES API URL: {}".format(url))
    auth = context.config.get('ES_basicAuth')

    # Send API Request to validate service state
    try:
        urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.request(method=ESRequestType, url=url, auth=HTTPBasicAuth(auth, auth), verify=False)

        # Extracting Response from ES API
        response_codes[ESRequestType] = response.status_code
        response_json[ESRequestType] = response.json()

        # Validate Response Code
        validate_response_code(context, int(response_codes[ESRequestType]), context.config.get('ES_APIResponse'))
        srState = response_json[ESRequestType]['_source']['state']
        inProgressState = response_json[ESRequestType]['_source']['in_progress']
        print('BI Service State: {}'.format(srState))

        if srState == 'active' or srState == 'inactive':
            if not inProgressState:
                return True, response_json[ESRequestType]['_source']['mwr_id']

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
