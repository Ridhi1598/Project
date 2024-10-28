from behave import given, when, then, step
from features.steps.bi.bi_restApis import *
from features.steps.api_steps_general import *
from features.steps.ui_steps_general import page_title_validation, change_currentPage
from features.steps.globalVar import GlobalVar
from requests.packages.urllib3.exceptions import InsecureRequestWarning


@step('I set data values against scenario "{scenario}" for API Gateway')
def set_params(context, scenario):
    global testParams, scenarioVal

    for index in range(0, 6):
        testParams = context.csvReadAPI[index]
        scenarioVal = testParams.get("Scenario")
        print(scenarioVal)
        if scenarioVal == scenario:
            break

# @step('I Set "{requestType}" api endpoint for "{endpoint}" for L3VPN')
# def set_endpoint_for_L3VPN(context, requestType, endpoint):
#     GlobalVar.api_dict['api_endpoint_' + requestType + '_url'] = GlobalVar.api_url + endpoint
#     print(GlobalVar.api_dict['api_endpoint_' + requestType + '_url'])
#     return GlobalVar.api_dict['api_endpoint_' + requestType + '_url']


@step('Send "{requestType}" HTTP request for API Gateway')
def send_HTTP_request(context, requestType):

    global response_texts, response, response_json
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    if requestType == 'POST':
        response = requests.post(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                 headers=GlobalVar.api_dict.get("request_header"),
                                 data=GlobalVar.api_dict.get("payload"),
                                 verify=False)
    if requestType == 'GET':
        response = requests.get(url=GlobalVar.api_dict.get("api_endpoint_" + requestType + "_url"),
                                headers=GlobalVar.api_dict.get("request_header"),
                                params=GlobalVar.api_dict.get('request_params'),
                                verify=False)

    # extracting response status_code
    response_codes[requestType] = response.status_code
    GlobalVar.response_codes = response_codes
    if scenarioVal == 'Health API':
        response_texts[requestType] = response.text
        pass
    else:
        response_json[requestType] = response.json()


@step('I validate the response value of API Gateway for "{scenario}"')
def validate_response(context, scenario):
    if scenario == 'Health API':
        responseVal = (testParams.get("Response Assertion-1")).split('"')
        assert responseVal[1] in response_texts['GET']


@step(u'Set request Body for API of L3VPN')
def step_impl(context):
    GlobalVar.api_dict['payload'] = testParams.get("Request Body")

@step('I validate the response value for expected message of API Gateway')
def validate_error_message(context):
    for key in response_json:
        if key == 'POST':
            if scenarioVal == 'Routing service validation-1':
                value = response_json[key]['reason'][0]
                assert value in testParams.get("Response Assertion-1")

            elif scenarioVal == 'Keycloack certificate validation':
                try:
                    value = response_json[key]['reason']
                    assert value[0] in testParams.get("Response Assertion-1")
                except:
                    value = response_json[key]['reason'][0]
                    assert value[0] in testParams.get("Response Assertion-2")

            else:
                value = response_json[key]['reason']
                assert value in testParams.get("Response Assertion-1")


@step('I Set HEADER param request "{header}" for "{scenario}" for API Gateway')
def set_token_value(context, header, scenario):
    global request_headers
    auth = testParams.get(header)
    if auth == 'Bearer Token':
        access_token = generate_access_token(context)
        request_headers[header] = 'Bearer ' + access_token
    else:
        request_headers[header] = 'Bearer ' + auth
    GlobalVar.api_dict['request_header'] = request_headers


@step('Set request Body for api gateway APIs of L3VPN')
def set_request_body_api_gateway(context):
    global payload
    GlobalVar.api_dict['payload'] = testParams.get("Request Body")
