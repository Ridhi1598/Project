import base64
import calendar
from datetime import datetime
from os.path import dirname, abspath

# import tornado.web
from cryptography.fernet import Fernet
from flask_jwt_extended import set_refresh_cookies

from features.steps.globalVar import GlobalVar
from features.steps.bi.bi_restApis import *
from features.steps.api_steps_general import *
from behave import given, when, then, step
from requests.auth import HTTPBasicAuth
# from features.steps import refreshTokenTornado

#declared variables
from features.steps.globalVar import GlobalVar
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
updated_payload = None
body = {}
testParams = {}
sdwanFunTCs = {}
session = None
cookie_value = None
from features.steps.globalVar import GlobalVar


@step(u'I set SDWAN functional "{apiType}" url')
def set_API_type(context, apiType):
    global api_url
    url = 'sdwanFunctionalURL_' + sys.argv[2]
    api_url = context.config.get(url)
    GlobalVar.api_url = api_url
    return api_url


@step("I generate access token for the authorization of SDWAN Functional Tcs")
def generate_access_token(context):
    global body
    global access_token
    sdwan_set_endpoint(context)
    set_header_request(context, 'Content-Type', 'application/x-www-form-urlencoded')
    filepath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + '/resources/payload/sdwan/sdwan_AccessToken.json'
    f = open(filepath)
    body = json.load(f)
    GlobalVar.api_dict['request_bodies'] = body
    responseCode = sdwan_post_request_authorization(context)
    sdwan_validate_response_code(context, int(responseCode), context.config.get('authorizationAPIResponse'))
    accessToken = sdwan_get_access_token(context)
    return access_token


@step("I generate access token for the authorization for Portal TCs")
def generate_access_token(context):
    global body
    global access_token
    sdwan_set_endpoint(context)
    set_header_request(context, 'Content-Type', 'application/x-www-form-urlencoded')
    filepath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) + '/resources/payload/sdwan/sdwan_AccessToken_portal.json'
    f = open(filepath)
    body = json.load(f)
    GlobalVar.api_dict['request_bodies'] = body
    responseCode = sdwan_post_request_authorization_portal(context)
    sdwan_validate_response_code(context, int(responseCode), context.config.get('authorizationAPIResponse'))
    accessToken = sdwan_get_access_token(context)
    return access_token


@step(u'I Set HEADER param request "{header}" as "{header_content_type}" for SDWAN Functional Tcs')
def set_header_request(context, header, header_content_type):
    global request_headers
    if header == 'Authorization':
        header_content_type = 'Bearer ' + access_token
    request_headers[header] = header_content_type
    GlobalVar.api_dict['request_header'] = request_headers


@step(u'I Set POST posts api endpoint for authorization of SDWAN Functional TCs')
def sdwan_set_endpoint(context):
    api_url = GlobalVar.api_url
    api_endpoints['POST_URL'] = context.config.get('sdwanFunctionalAccessToken_preprod')
    GlobalVar.api_dict['api_endpoint_post_url'] = api_endpoints['POST_URL']


@step('I extract response value of access_token for sdwan Functional TCs')
def sdwan_get_access_token(context):
    global access_token
    for key in response_json:
        if key == 'POST':
            for key_nested in response_json[key]:
                if key_nested == 'access_token':
                    access_token = response_json[key][key_nested]
                    return access_token
        else:
            print("Access Token Not Found")

@step('I receive valid HTTP response code "{actual_response_code}" as "{expected_response_code}" for sdwan Functional Tcs')
def sdwan_validate_response_code(context, actual_response_code, expected_response_code):
    time.sleep(3)
    assert actual_response_code == expected_response_code


@step(u'I set POST api endpoint "{enpoint_param}" for SDWAN Functional Tcs')
def step_impl(context, enpoint_param):
    api_url = GlobalVar.api_url
    api_endpoints['POST_URL'] = api_url + enpoint_param
    # print('url :' + api_endpoints['GET_URL'])


@step(u'Response BODY "{request_name}" is non-empty of SDWAN Functional Tcs')
def step_impl(context, request_name):
    print(response_texts[request_name])
    assert response_texts[request_name] is not None


@step(u'I receive valid HTTP response code 200 for "{request_name}" of SDWAN Functional Tcs')
def step_impl(context, request_name):
    time.sleep(3)
    # print("Request Name :-" + request_name)
    # print(GlobalVar.response_codes.get(request_name))
    print(response_codes.get(request_name))
    assert response_codes.get(request_name) == 200


@step(u'I Set POST posts api endpoint for "{endpoint}" API of sdwan Functional')
def step_impl(context, endpoint):
    api_url = GlobalVar.api_url
    if endpoint == "/tinaa-sdwan-services/{service-id}/vpns":
        api_endpoints['POST_URL'] = api_url + endpoint.replace('{service-id}', sdwanFunTCs.get('service-id'))
    elif endpoint == "/tinaa-sdwan-services/{service-id}/sites":
        api_endpoints['POST_URL'] = api_url + endpoint.replace('{service-id}', sdwanFunTCs.get('service-id'))
    else:
        api_endpoints['POST_URL'] = api_url + endpoint
    GlobalVar.api_dict['api_endpoint_post_url'] = api_endpoints['POST_URL']
    print(api_endpoints['POST_URL'])


@step(u'Set request Body for SDWAN Functional TCs')
def step_impl(context):
    global request_bodies
    global payload

    requestType = testParams.get('Request-Type')
    print("Request Type: ", requestType)

    if requestType == 'DELETE':
        pass

    elif requestType == 'POST' or 'PUT' or 'PATCH':
        filename = testParams.get('payload')
        rootPath = dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) \
                   + '/resources/payload/sdwan/' + filename
        f = open(rootPath, 'rb')
        payload = json.load(f)
        GlobalVar.api_dict['payload'] = payload


#GET Method for SDWAN Functional Testcases

@step(u'I set GET api endpoint "{endpoint_param}" for SDWAN Functional TCs')
def step_impl(context, endpoint_param):
    global api_endpoints
    api_url = GlobalVar.api_url
    if endpoint_param == "/tinaa-sdwan-services":
        api_endpoints['GET_URL'] = api_url + endpoint_param

    elif endpoint_param == "/tinaa-sdwan-services/{service-id}":
        api_endpoints['GET_URL'] = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))

    elif endpoint_param == "/tinaa-sdwan-services/{service-id}/vpns":
        api_endpoints['GET_URL'] = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))

    elif endpoint_param == "/tinaa-sdwan-services/{service-id}/vpns/{vpn-id}":
        api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
        api_endpoints['GET_URL'] = api_url1.replace('{vpn-id}', sdwanFunTCs.get('vpn-id'))

    elif endpoint_param == "/tinaa-sdwan-services/{service-id}/sites":
        api_endpoints['GET_URL'] = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))

    elif endpoint_param == "/tinaa-sdwan-services/{service-id}/sites/{site-id}":
        api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
        api_endpoints['GET_URL'] = api_url1.replace('{site-id}', sdwanFunTCs.get('site-id'))

    elif endpoint_param == "/bsaf-telus-ext-customer":
         api_endpoints['GET_URL'] = api_url + endpoint_param

    elif endpoint_param == "/bsaf-telus-ext-customer/{cust-id}":
        api_endpoints['GET_URL'] = api_url + endpoint_param.replace('{cust-id}', sdwanFunTCs.get('Create_customer_id'))

    elif endpoint_param == "/bsaf-sdwan-device-licenses":
         api_endpoints['GET_URL'] = api_url + endpoint_param

    elif endpoint_param == "/bsaf-sdwan-templates":
         api_endpoints['GET_URL'] = api_url + endpoint_param

    elif endpoint_param == '/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/wan-access':
         api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
         api_url2 = api_url1.replace('{site-id}', sdwanFunTCs.get('site-id'))
         api_endpoints['GET_URL'] = api_url2.replace('{device-id}', sdwanFunTCs.get('device-id'))

    elif endpoint_param == '/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/wan-access/{name}':
         api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
         api_url2 = api_url1.replace('{site-id}', sdwanFunTCs.get('site-id'))
         api_url3 = api_url2.replace('{device-id}', sdwanFunTCs.get('device-id'))
         api_endpoints['GET_URL'] = api_url3.replace('{name}', sdwanFunTCs.get('wan-name'))

    elif endpoint_param == '/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/lan-access':
         api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
         api_url2 = api_url1.replace('{site-id}', sdwanFunTCs.get('site-id'))
         api_endpoints['GET_URL'] = api_url2.replace('{device-id}', sdwanFunTCs.get('device-id'))

    elif endpoint_param == '/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/lan-access/{name}':
         api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
         api_url2 = api_url1.replace('{site-id}', sdwanFunTCs.get('site-id'))
         api_url3 = api_url2.replace('{device-id}', sdwanFunTCs.get('device-id'))
         api_endpoints['GET_URL'] = api_url3.replace('{name}', sdwanFunTCs.get('lan-name'))

    GlobalVar.api_dict['api_endpoint_get_url'] = api_endpoints['GET_URL']


@step('I extract response value of service-id and cust-id for SDWAN Functional TCs')
def step_impl(context):
    global responseVar
    global sdwanFunTCs
    for key in response_json:
        if key == 'GET':
            for key_nested in response_json[key]:
                if key_nested == 'services':
                    for key_nested2 in response_json[key][key_nested]:
                        if context.csvReadAPI[0].get('sli_service_id') == key_nested2['tinaa-sdwan-services'][0]['service-id']:
                            sdwanFunTCs['service-id'] = key_nested2['tinaa-sdwan-services'][0]['service-id']
                            if context.csvReadAPI[0].get('sli_cust_id') == key_nested2['tinaa-sdwan-services'][0]['cust-id']:
                                sdwanFunTCs['cust-id'] = key_nested2['tinaa-sdwan-services'][0]['cust-id']
                            break
            print(sdwanFunTCs.get('service-id'))
            print(sdwanFunTCs.get('cust-id'))


@step('I extract site-id from list of all Sites for SDWAN Functional TCs')
def extract_siteid_from_all_sites(context):
    global responseVar
    global sdwanFunTCs
    for key in response_json:
        if key == 'GET':
            for key_nested in response_json[key]:
                if key_nested == 'sites':
                    for key_nested2 in response_json[key][key_nested]:
                        sdwanFunTCs['site-id'] = key_nested2['site-id']
                        break
    print(sdwanFunTCs.get("site-id"))
    print(sdwanFunTCs.get('service-id'))

@step('I extract cust-id from the response after creating a customer')
def extract_siteid_from_all_sites(context):
    global responseVar
    global sdwanFunTCs
    print(response_json['POST'])
    sdwanFunTCs['Create_customer_id'] = response_json['POST']['details']['cust-id']
#common methods for SDWAN Functional TCs


@step('I set Test Data for testcase "{testCase}" of SDWAN Functional TCs')
def read_TestData_file(context, testCase):
    global testParams
    index = int(testCase) - 1
    testParams = context.csvReadAPI[index]
    testcase = testParams.get('Testcase')
    assert testcase == testCase


@step('Set the Updated values of payload for create services POST API')
def update_payload_for_create_service_POST_API(context):
    global updated_payload
    updated_payload = GlobalVar.api_dict['payload']
    updated_payload['tinaa-sdwan-services'][0]['service-id'] = sdwanFunTCs.get('service-id')
    updated_payload['tinaa-sdwan-services'][0]['cust-id'] = sdwanFunTCs.get('cust-id')
    GlobalVar.api_dict['payload'] = updated_payload
    # print(GlobalVar.api_dict['payload'])


@step('Set the Updated values of payload for creates a SDWAN VPN')
def updated_payload_create_vpn(context):
    global updated_payload
    updated_payload = GlobalVar.api_dict['payload']
    updated_payload['vpn-id'] = sdwanFunTCs.get('vpn-id')
    GlobalVar.api_dict['payload'] = updated_payload
    print(updated_payload)

@step('Set the Updated values of payload to update a SDWAN VPN')
def update_payload_update_vpn(context):
    global updated_payload
    updated_payload = GlobalVar.api_dict['payload']
    updated_payload['vpn-id'] = sdwanFunTCs.get('vpn-id')
    GlobalVar.api_dict['payload'] = updated_payload
    print(updated_payload)

@step('Set the Updated values of payload for creates a SDWAN site')
def updated_payload_create_vpn(context):
    global updated_payload
    updated_payload = GlobalVar.api_dict['payload']
    updated_payload['site-id'] = sdwanFunTCs.get('site-id')
    GlobalVar.api_dict['payload'] = updated_payload
    print(updated_payload)

@step('Set the Updated values of payload for update a SDWAN site')
def updated_payload_create_vpn(context):
    global updated_payload
    updated_payload = GlobalVar.api_dict['payload']
    updated_payload['site-id'] = sdwanFunTCs.get('site-id')
    GlobalVar.api_dict['payload'] = updated_payload
    print(updated_payload)

@step('Set the Updated values of payload for create a Customer')
def updated_payload_create_vpn(context):
    global updated_payload
    updated_payload = GlobalVar.api_dict['payload']
    updated_payload['bsaf-telus-ext-customer']['cust-id'] = sdwanFunTCs.get('customer-id')
    GlobalVar.api_dict['payload'] = updated_payload
    print(updated_payload)

@step('Set the Updated values of payload for update a Customer')
def updated_payload_create_vpn(context):
    global updated_payload
    updated_payload = GlobalVar.api_dict['payload']
    updated_payload['bsaf-telus-ext-customer']['cust-id'] = sdwanFunTCs.get('Create_customer_id')
    GlobalVar.api_dict['payload'] = updated_payload
    print(updated_payload)

#Patch API methods
@step(u'I set Patch api endpoint "{endpoint_param}" for SDWAN Functional TCs')
def step_impl(context, endpoint_param):
    api_url = GlobalVar.api_url
    api_endpoints['PATCH_URL'] = api_url + endpoint_param
    if testParams.get("Endpoint") == endpoint_param:
        api_endpoints['PATCH_URL'] = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
    GlobalVar.api_dict['api_endpoint_patch_url'] = api_endpoints['PATCH_URL']
    print(api_endpoints.get('PATCH_URL'))


@step('I Set the updated fields of payload for Patch Service')
def update_fields_patch_Service_Api(context):
    global updated_payload
    updated_payload = GlobalVar.api_dict['payload']
    updated_payload['tinaa-sdwan-services'][0]['service-id'] = sdwanFunTCs.get('service-id')
    updated_payload['tinaa-sdwan-services'][0]['cust-id'] = sdwanFunTCs.get('cust-id')
    GlobalVar.api_dict['payload'] = updated_payload


#Delete API Methods

@step(u'I set Delete api endpoint "{endpoint_param}" for SDWAN Functional TCs')
def step_impl(context, endpoint_param):
    api_url = GlobalVar.api_url
    if endpoint_param == "/tinaa-sdwan-services/{service-id}":
        api_endpoints['DELETE_URL'] = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
    if endpoint_param == "/tinaa-sdwan-services/{service-id}/vpns/{vpn-id}":
        api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
        api_endpoints['DELETE_URL'] = api_url1.replace('{vpn-id}', sdwanFunTCs.get('vpn-id'))
    elif endpoint_param == "/tinaa-sdwan-services/{service-id}/sites/{site-id}":
        api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
        api_endpoints['DELETE_URL'] = api_url1.replace('{site-id}', sdwanFunTCs.get('site-id'))
    elif endpoint_param == "/bsaf-telus-ext-customer/{cust-id}":
        api_endpoints['DELETE_URL'] = api_url + endpoint_param.replace('{cust-id}', sdwanFunTCs.get('Create_customer_id'))
    GlobalVar.api_dict['api_endpoint_delete_url'] = api_endpoints['DELETE_URL']


@step('I extract the vpn-id from the lists all SDWAN VPNs in given SDWAN service')
def extract_vpn_id(context):
    global responseVar
    global sdwanFunTCs
    for key in response_json:
        if key == 'GET':
            for key_nested in response_json[key]:
                if key_nested == 'vpns':
                    for key_nested2 in response_json[key][key_nested]:
                        sdwanFunTCs['vpn-id'] = key_nested2['vpn-id']
                        break
    print(sdwanFunTCs.get('vpn-id'))


#PUT Method

@step(u'I set PUT api endpoint "{endpoint_param}" for SDWAN Functional TCs')
def step_impl(context, endpoint_param):
    api_url = GlobalVar.api_url
    if endpoint_param == "/tinaa-sdwan-services/{service-id}/vpns/{vpn-id}":
        api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
        api_endpoints['PUT_URL'] = api_url1.replace('{vpn-id}', sdwanFunTCs.get('vpn-id'))

    elif endpoint_param == "/tinaa-sdwan-services/{service-id}/sites/{site-id}":
        api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
        api_endpoints['PUT_URL'] = api_url1.replace('{site-id}', sdwanFunTCs.get('site-id'))

    elif endpoint_param == "/bsaf-telus-ext-customer/{cust-id}":
        api_endpoints['PUT_URL'] = api_url + endpoint_param.replace('{cust-id}', sdwanFunTCs.get('Create_customer_id'))

    elif endpoint_param == '/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/wan-access/{name}':
         api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
         api_url2 = api_url1.replace('{site-id}', sdwanFunTCs.get('site-id'))
         api_url3 = api_url2.replace('{device-id}', sdwanFunTCs.get('device-id'))
         api_endpoints['PUT_URL'] = api_url3.replace('{name}', sdwanFunTCs.get('wan-name'))

    elif endpoint_param == '/tinaa-sdwan-services/{service-id}/sites/{site-id}/devices/device/{device-id}/lan-access/{name}':
         api_url1 = api_url + endpoint_param.replace('{service-id}', sdwanFunTCs.get('service-id'))
         api_url2 = api_url1.replace('{site-id}', sdwanFunTCs.get('site-id'))
         api_url3 = api_url2.replace('{device-id}', sdwanFunTCs.get('device-id'))
         api_endpoints['PUT_URL'] = api_url3.replace('{name}', sdwanFunTCs.get('lan-name'))

    GlobalVar.api_dict['api_endpoint_put_url'] = api_endpoints['PUT_URL']
    print(api_endpoints.get('PUT_URL'))


@step('Send HTTP request for SDWAN Functional TCs')
def send_HTTP_request(context):
    global requestId
    global response_json
    global response_codes
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    print("Sending ", testParams['Request-Type'], " request")

    if testParams['Request-Type'] == 'POST':
        response = requests.post(url=GlobalVar.api_dict.get("api_endpoint_" + testParams['Request-Type'].lower() + "_url"),
                                 headers=GlobalVar.api_dict.get("request_header"),
                                 json=GlobalVar.api_dict.get("payload"),
                                 verify=False)

    if testParams['Request-Type'] == 'PUT':
        response = requests.put(url=GlobalVar.api_dict.get("api_endpoint_" + testParams['Request-Type'].lower() + "_url"),
                                headers=GlobalVar.api_dict.get("request_header"),
                                json=GlobalVar.api_dict.get("payload"),
                                verify=False)

    if testParams['Request-Type'] == 'PATCH':
        response = requests.patch(url=GlobalVar.api_dict.get("api_endpoint_" + testParams['Request-Type'].lower() + "_url"),
                                headers=GlobalVar.api_dict.get("request_header"),
                                json=GlobalVar.api_dict.get("payload"),
                                verify=False)

    if testParams['Request-Type'] == 'GET':
        response = requests.get(url=GlobalVar.api_dict.get("api_endpoint_" + testParams['Request-Type'].lower() + "_url"),
                                headers=GlobalVar.api_dict.get("request_header"),
                                verify=False)

    if testParams['Request-Type'] == 'DELETE':
        response = requests.delete(url=GlobalVar.api_dict.get("api_endpoint_" + testParams['Request-Type'].lower() + "_url"),
                                   headers=GlobalVar.api_dict.get("request_header"),
                                   verify=False)

    response_texts[testParams['Request-Type']] = response.text
    statuscode = response.status_code
    response_codes[testParams['Request-Type']] = statuscode
    response_json[testParams['Request-Type']] = response.json()
    print(response.json())


@step(u'Send POST HTTP request for authorization of SDWAN Functional Tcs')
def sdwan_post_request_authorization(context):
    global access_token
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.post(url=api_endpoints['POST_URL'],
                             headers=GlobalVar.api_dict.get("request_header"),
                             data=GlobalVar.api_dict.get("request_bodies"),
                             verify=False
                             )
    response_texts['POST'] = response.text
    statuscode = response.status_code
    response_codes['POST'] = statuscode
    response_json['POST'] = response.json()
    return response_codes['POST']


@step('I extract requestId from response of "{apiType}" request for ElasticSearch Database Validation')
def extract_requestId(context, apiType):
    global sdwanFunTCs
    sdwanFunTCs['request_id'] = response_json[apiType]['details']['request-id']


@step('I perform ElasticSearch Database Validation for "{apiType}" request')
def elasticSearch_Database_validation(context, apiType):
    global response_codes
    global response_texts
    global response_json

    print('ElasticSearch validation for '+apiType+' request')
    api_endpoints['GET_URL'] = context.config.get('sdwanFunctionalElasticSearch_develop')

    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    GlobalVar.api_dict['api_endpoint_get_url'] = api_endpoints['GET_URL']+'/'+sdwanFunTCs.get('request_id')

    response = requests.get(api_endpoints['GET_URL']+'/'+sdwanFunTCs.get('request_id'),
                            auth=HTTPBasicAuth(context.csvReadAPI[0].get('ESUserid'), context.csvReadAPI[0].get('ESPassword')),
                            verify=False)
    response_texts[testParams['Request-Type']] = response.text
    statuscode = response.status_code
    response_codes[testParams['Request-Type']] = statuscode
    response_json[testParams['Request-Type']] = response.json()

    assert response.json()['_id'] == sdwanFunTCs.get('request_id')


@step('I extract device-id for the corresponding site-id')
def extract_deviceId(context):
    global response_json
    global sdwanFunTCs
    if sdwanFunTCs.get('site-id') == response_json['GET']['sites'][0]['site-id']:
        sdwanFunTCs['device-id'] = response_json['GET']['sites'][0]['devices']['device'][0]['device-id']
    print(sdwanFunTCs.get('device-id'))

@step('I extract name from the list of LAN Interface')
def get_name_from_list_of_LAN_Interface(context):
    global response_json
    global sdwanFunTCs
    for key in response_json:
        if key == "GET":
            for keyNested in response_json['GET']:
                if keyNested == 'lan-access':
                    sdwanFunTCs['lan-name'] = response_json['GET'][keyNested][0]['name']

@step('I extract name from the list of WAN Interface')
def get_name_from_list_of_LAN_Interface(context):
    global response_json
    global sdwanFunTCs
    for key in response_json:
        if key == "GET":
            for keyNested in response_json['GET']:
                if keyNested == 'wan-access':
                    sdwanFunTCs['wan-name'] = response_json['GET'][keyNested][0]['name']
    print(sdwanFunTCs.get('wan-name'))


#FUNCTIONAL TESTCASES FOR PORTAL

@step('I set GET api endpoint "{endpoint_param}" for the Portal testcases')
def step_impl(context, endpoint_param):
    global api_endpoints
    global testParams
    api_url = GlobalVar.api_url
    if endpoint_param == testParams['Endpoint']:
        api_endpoints['GET_URL'] = api_url + endpoint_param
    GlobalVar.api_dict['api_endpoint_get_url'] = api_endpoints['GET_URL']


@step('I set PUT api endpoint "{endpoint_param}" for the Portal testcases')
def step_impl(context, endpoint_param):
    global api_endpoints
    api_url = GlobalVar.api_url
    global api_endpoints
    global testParams
    api_url = GlobalVar.api_url
    if endpoint_param == testParams['Endpoint']:
        api_endpoints['PUT_URL'] = api_url + endpoint_param
    GlobalVar.api_dict['api_endpoint_put_url'] = api_endpoints['PUT_URL']


@step('I set POST api endpoint "{endpoint_param}" for the Portal testcases')
def step_impl(context, endpoint_param):
    global api_endpoints
    api_url = GlobalVar.api_url
    global api_endpoints
    global testParams
    api_url = GlobalVar.api_url
    if endpoint_param == testParams['Endpoint']:
        api_endpoints['POST_URL'] = api_url + endpoint_param
    GlobalVar.api_dict['api_endpoint_post_url'] = api_endpoints['POST_URL']


@step('I set DELETE api endpoint "{endpoint_param}" for the Portal testcases')
def step_impl(context, endpoint_param):
    global api_endpoints
    api_url = GlobalVar.api_url
    global api_endpoints
    global testParams
    api_url = GlobalVar.api_url
    if endpoint_param == testParams['Endpoint']:
        api_endpoints['PUT_URL'] = api_url + endpoint_param
    GlobalVar.api_dict['api_endpoint_put_url'] = api_endpoints['PUT_URL']


@step('Send GET Http request for the functional TCS of SDWAN Portal')
def step_impl(context):
    global access_token
    global session
    global cookie_value
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    session = requests.Session()
    response = session.get(url=api_endpoints.get('GET_URL'),
                            headers=GlobalVar.api_dict.get("request_header"),
                            verify=False)
    response_texts['GET'] = response.text
    statuscode = response.status_code
    response_codes['GET'] = statuscode
    cookie = response.cookies
    cookie_value = cookie['6c5d6af82ca6be5e6ce301f2b4886e86']
    print(cookie_value)

@step(u'Send POST HTTP request for Portal Authentication Token')
def sdwan_post_request_authorization_portal(context):
    global access_token
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # tornado.web.RequestHandler.get_secure_cookie(context)
    # username_get_secure_cookies(context)

    response = requests.post(url=api_endpoints['POST_URL'],
                             headers=GlobalVar.api_dict.get("request_header"),
                             data=GlobalVar.api_dict.get("request_bodies"),
                             verify=False
                             )
    response_texts['POST'] = response.text
    statuscode = response.status_code
    response_codes['POST'] = statuscode
    response_json['POST'] = response.json()
    return response_codes['POST']



"""SCRIPTS SHARED BY ASHUTOSH- REFRESH TOKEN"""


# username = handler.get_current_username()
# if not username:
#     finish_return(handler, None, 401, 'login again', 'Please wait for a while!')
#     return
# else:
#     if not handler.role_status(role, username):
#         finish_return(handler, None, 403, 'Unauthorized API',
#                       'This API is not authorized for your login!')
#
#
# def get_current_username(self):
#     """
#     Retrieve username cookie from storage if not available then
#     user refresh_token from cookie and fetch updated access token and
#     update username cookie
#     Returns
#     -------
#     str
#         username cookie
#     """
#     username = handler.get_current_username()
#     print(username)
#     username = self.username_get_secure_cookies()
#     if username is None:
#         # call refresh cookies based on refresh token
#         if self.refresh_token_get_secure_cookies() is not None:
#             refresh_flage, username = refresh_token_cookies_upgrade(self,
#                                                                     Fernet(str.encode(self.secret_key)).decrypt(
#                                                                         self.refresh_token_get_secure_cookies()).decode())
#             if refresh_flage:
#                 return username if username else None
#             else:
#                 return None
#     else:
#         refresh_flage, username = refresh_token_cookies_upgrade(self, Fernet(str.encode(self.secret_key)).decrypt(
#             self.refresh_token_get_secure_cookies()).decode(), True)
#         if refresh_flage:
#             return username if username else None
#         else:
#             return None
#
#
# def username_get_secure_cookies(context):
#     """
#     Returns the given signed cookie if it validates, or None
#     Returns
#     -------
#     byte string
#         decoded cookie value
#     """
#
#     # print(context.get_secure_cookie('username'))
#     return context.get_secure_cookie('username')
#
#
#
# def refresh_token_get_secure_cookies(context):
#     """
#     Get the refresh token secure cookies
#     Returns
#     -------
#     byte string
#         The decoded cookie value is returned
#     """
#     # this.context = context
#     return context.get_secure_cookie('refresh_token')
#
#
#
# def refresh_token_cookies_upgrade(self, refresh_token, keycloak_logout_flage=False):
#     """
#     Getting the keycloak cookie details.
#     Parameters
#     ----------
#     refresh_token : str
#         refresh token for keycloak url
#     keycloak_logout_flage : bool
#         keycloak flag set as False default.
#     Returns
#     -------
#     bool
#         True if success, else False
#     json object
#         Returns cookie setup json details
#     """
#     try:
#         access_token_resp = requests.post(self.key_cloak_url, data={'client_id': self.key_client_id,
#                                                                     'client_secret': self.key_client_secret,
#                                                                     'grant_type': 'refresh_token',
#                                                                     'refresh_token': refresh_token},
#                                           verify=False,
#                                           timeout=30)
#         if access_token_resp.json()['access_token']:
#             access_token = access_token_resp.json()['access_token']
#             headers = {'Authorization': 'Bearer ' + access_token,
#                        'refresh_access_token': access_token_resp.json()['refresh_token'],
#                        'expires_in': access_token_resp.json()['expires_in'],
#                        'refresh_expires_in': access_token_resp.json()['refresh_expires_in']}
#             access_token = headers.get("Authorization")
#             refresh_access_token = headers.get("refresh_access_token")
#             self.logger.info(str(self.key_cloak_url + " \n method: GET"))
#             cookies_handler_using_access_token(self, access_token, refresh_access_token, headers.get("expires_in"),
#                                                headers.get("refresh_expires_in"), self.secret_key,
#                                                self.key_client_id)
#             timeduration = datetime.datetime.utcnow() + datetime.timedelta(
#                 seconds=headers.get("expires_in"))  # expire_in
#             cookies_expire = calendar.timegm(timeduration.timetuple())
#             cookies_setup = json.dumps({'code': access_token, 'time_set': str(cookies_expire)})
#             return True, cookies_setup
#         else:
#             self.clear_cookie("username")
#             self.clear_cookie("refresh_token")
#             self.clear_all_cookies()
#             return False
#     except Exception as e:
#         self.clear_cookie("username")
#         self.clear_cookie("refresh_token")
#         self.clear_all_cookies()
#         self.logger.info(str('Failed to refresh access token, Please try again!'))
#         self.logger.info(str(e))
#         return False
#
#
# def cookies_handler_using_access_token(self, code, refresh_access_token, expire_in, refresh_expire_in, key, resource):
#     """
#     Set the cookies access token after login.
#     Parameters
#     ---------
#     code: str
#         decoded access token
#     refresh_access_token: str
#         decoded refresh access token
#     expire_in: str
#         decoded access token expiring time
#     refresh_expire_in: str
#         decoded refresh access token expiring time
#     key: str
#         secret key for encoding and decoding the cookies data
#     resource: str
#         keyclock client id
#     Returns
#     -------
#     str
#         Only set the cookies for user and refresh_token.
#     """
#     try:
#         timeduration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_in)  # expire_in
#         cookies_expire = calendar.timegm(timeduration.timetuple())
#         cookies_setup = json.dumps({'code': code, 'time_set': str(cookies_expire)})
#         self.set_secure_cookie("username", Fernet(str.encode(key)).encrypt(str.encode(str(cookies_setup))).decode(),
#                                expires=cookies_expire)
#         set_refresh_cookies(self, refresh_access_token, refresh_expire_in, key)
#     except Exception as e:
#         self.logger.info(str(e))
#
#
# def role_status(self, access_role, username):
#     """
#     Is user having any role of the application?
#     Parameters
#     ----------
#     access_role : str
#         role name
#     username : str
#         username from cookie
#     Returns
#     -------
#     bool
#         True/False
#         e.g.:
#         True: If user is having the application any role
#         False: If user is not having the application any role
#     """
#     code = json.loads(username)['code']
#     code = json.loads(
#         base64.urlsafe_b64decode(code.replace('Bearer ', '').strip().split('.')[1] + '==').decode('ascii'))
#     auth_roles = code['resource_access'][self.key_client_id]['roles']
#     for i in auth_roles:
#         if i in access_role:
#             return True
#     return False


#VELO Functional TCs

@step('I generate access token for the authorization for Velo TCs')
def auth_token(context):
    global body
    global access_token
    sdwan_set_endpoint(context)
    set_header_request(context, 'Content-Type', 'application/x-www-form-urlencoded')
    filepath = dirname(os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../.."))) + '/resources/payload/sdwan/sdwan_AccessToken_Velo.json'
    f = open(filepath)
    body = json.load(f)
    GlobalVar.api_dict['request_bodies'] = body
    responseCode = sdwan_post_request_authorization(context)
    sdwan_validate_response_code(context, int(responseCode), context.config.get('authorizationAPIResponse'))
    accessToken = sdwan_get_access_token(context)
    return access_token


@step('I set GET api endpoint "{endpoint_param}" for the Velo testcases')
def step_impl(context, endpoint_param):
    global api_endpoints
    global testParams
    api_url = GlobalVar.api_url
    if endpoint_param == testParams['Endpoint']:
       api_endpoints['GET_URL'] = api_url + endpoint_param
    GlobalVar.api_dict['api_endpoint_get_url'] = api_endpoints['GET_URL']


@step(u'I validate HTTP response code 404 for "{request_name}" of SDWAN Functional Tcs')
def step_impl(context, request_name):
    time.sleep(3)
    print("Request Name :-" + request_name)
    assert response_codes.get(request_name) == 404


@step('I set POST api endpoint "{endpoint_param}" for the Velo testcases')
def set_POST_endpoint(context, endpoint_param):
    global api_endpoints
    global testParams
    api_url = GlobalVar.api_url
    if endpoint_param == testParams['Endpoint']:
        api_endpoints['POST_URL'] = api_url + endpoint_param
    GlobalVar.api_dict['api_endpoint_post_url'] = api_endpoints['POST_URL']

@step('I set PUT api endpoint "{endpoint_param}" for the Velo testcases')
def set_POST_endpoint(context, endpoint_param):
    global api_endpoints
    global testParams
    api_url = GlobalVar.api_url
    if endpoint_param == testParams.get('Endpoint'):
        api_endpoints['PUT_URL'] = api_url + endpoint_param
    GlobalVar.api_dict['api_endpoint_put_url'] = api_endpoints.get('PUT_URL')


@step('I set DELETE api endpoint "{endpoint_param}" for the Velo testcases')
def set_POST_endpoint(context, endpoint_param):
    global api_endpoints
    global testParams
    api_url = GlobalVar.api_url
    if endpoint_param == testParams['Endpoint']:
        api_endpoints['DELETE_URL'] = api_url + endpoint_param
    GlobalVar.api_dict['api_endpoint_delete_url'] = api_endpoints['DELETE_URL']


@step(u'I validate the response schema with "{schema_file_name}" for sdwan functional')
def step_impl(context, schema_file_name):
    schema_file_name = os.getcwd() + '/resources/schema/' + sys.argv[1] + '/'+ schema_file_name
    with open(schema_file_name, "r") as read_file:
        data = read_file.read()
        schema = json.loads(data)
        try:
            validate(instance=response_json, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True