from hamcrest import assert_that

from common.config.request_config_manager import RequestConfigManager
from behave import given, when, then, step
from features.domain_models.pet import Pet
from common.config.request_constants import RequestConstants
from features.steps.lcd.lcd_restApis import *
from features.steps.sdwan.sdwan_restApis import *
from features.steps.globalVar import GlobalVar


@given(u'Swagger PetStore web application url is set as "{basic_url}"')
def step_impl(context, basic_url):
    """
    BACKGROUND step is called at begin of each scenario before other steps.
    """
    # -- SETUP
    context.pet = Pet()
    context.requestConfigManager = RequestConfigManager()
    context.requestConfigManager.set_basic_url(basic_url)


@when(u'HEADER param request content type is set as "{header_content_type}"')
def step_impl(context, header_content_type):
    context.requestConfigManager.set_http_content_type(header_content_type)


@when(u'HEADER param response accept type is set as "{header_accept_type}"')
def step_impl(context, header_accept_type):
    context.requestConfigManager.set_http_accept_type(header_accept_type)


@step(u'HEADER param api_key is set')
def step_impl(context):
    context.requestConfigManager.set_api_key()


@when(u'"{http_request_type}" HTTP request is raised')
def step_impl(context, http_request_type):
    url_temp = context.requestConfigManager.get_basic_url()
    if RequestConstants.JSON_GET == http_request_type:
        url_temp += context.requestConfigManager.get_endpoint()
        context.requestConfigManager.clear_http_request_body()
        context.requestConfigManager.set_get_response_full(url_temp)
    elif RequestConstants.JSON_FINDBYSTATUS == http_request_type:
        url_temp += context.requestConfigManager.get_endpoint() + context.pet.get_pet_status()
        context.requestConfigManager.clear_http_request_body()
        context.requestConfigManager.set_get_response_full(url_temp)
    elif RequestConstants.JSON_POST == http_request_type:
        url_temp += context.requestConfigManager.get_endpoint()
        #         context.requestConfigManager.clear_http_request_body()
        context.requestConfigManager.set_post_response_full(url_temp)
    elif RequestConstants.JSON_UPLOAD == http_request_type:
        url_temp += context.requestConfigManager.get_endpoint()
        #         context.requestConfigManager.clear_http_request_body()
        context.requestConfigManager.set_post_uploadimage_response_full(url_temp)
    elif RequestConstants.JSON_PUT == http_request_type:
        url_temp += context.requestConfigManager.get_endpoint()
        context.requestConfigManager.set_put_response_full(url_temp)

    elif RequestConstants.JSON_DELETE == http_request_type:
        url_temp += context.requestConfigManager.get_endpoint()
        context.requestConfigManager.set_delete_response_full(url_temp)


@step(u'Valid HTTP response is received')
def step_impl(context):
    if None in context.requestConfigManager.get_response_full():
        assert_that('Null response received')


@step(u'Response http code is {expected_response_code:d}')
def step_impl(context, expected_response_code):
    context.requestConfigManager.set_expected_response_code(expected_response_code)
    actual_response_code = context.requestConfigManager.get_response_full_status_code()
    if str(actual_response_code) not in str(expected_response_code):
        assert_that('***ERROR: Following unexpected error response code received: ' + str(actual_response_code))


@step(u'Response http text is "{expected_response_text}"')
def step_impl(context, expected_response_text):
    actual_response_text = context.requestConfigManager.get_response_full_text()
    if actual_response_text not in expected_response_text:
        assert_that('***ERROR: Following unexpected error response text received: ' + actual_response_text)


@then(u'Response HEADER content type is "{expected_response_content_type}"')
def step_impl(context, expected_response_content_type):
    context.requestConfigManager.set_expected_response_content_type(expected_response_content_type)
    actual_response_content_type = context.requestConfigManager.get_response_full_content_type()
    if expected_response_content_type not in actual_response_content_type:
        assert_that(
            '***ERROR: Following unexpected error response content type received: ' + actual_response_content_type)


@then(u'Response BODY is not null or empty')
def step_impl(context):
    if None in context.requestConfigManager.get_response_full():
        assert_that('***ERROR:  Null or none response body received')


@when(u'HEADER params for request and response are specified')
def step_impl(context):
    context.requestConfigManager.clear_http_request_header()
    context.execute_steps(u''' when HEADER param request content type is set as "application/json"
    and HEADER param response accept type is set as "application/json" ''')

# General Steps

@step(u'I Set POST posts api endpoint for "{endpoint}"')
def step_impl(context, endpoint):
    api_url =  GlobalVar.api_url
    api_endpoints['POST_URL'] = api_url + endpoint
    GlobalVar.api_dict['api_endpoint_post_url'] = api_endpoints['POST_URL']
    print(api_endpoints)

@step(u'Send POST HTTP request')
def step_impl(context):
    # sending get request and saving response as response object
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    print(GlobalVar.api_dict.get("request_header"))
    print(GlobalVar.api_dict.get("payload"))
    print(GlobalVar.api_dict.get("api_endpoint_post_url"))
    response = requests.post(url=GlobalVar.api_dict.get("api_endpoint_post_url"),
                             headers=GlobalVar.api_dict.get("request_header"), data=GlobalVar.api_dict.get("payload"),
                             verify=False)
    # extracting response text
    response_texts['POST'] = response.text
    print(response.text)
    # extracting response status_code
    statuscode = response.status_code
    print(statuscode)
    response_codes['POST'] = statuscode
    response_json['POST'] = response.json()
    print(response_codes['POST'])


@step(u'I Set HEADER param request "{header}" as "{header_content_type}"')
def step_impl(context, header, header_content_type):
    global request_headers
    if header.lower() == 'cookie':
        header_content_type = 'tinaa-cookie="session_mock"'
    request_headers[header] = header_content_type
    GlobalVar.api_dict["request_header"] = request_headers

@step(u'I receive valid HTTP response code 200 for "{request_name}"')
def step_impl(context, request_name):
    time.sleep(3)
    print("Request Name :-" + request_name)
    print('Get rep code for ' + request_name + ':' + str(response_codes[request_name]))
    print(response_codes[request_name])
    assert response_codes[request_name] == 200


@step(u'I validate the response schema with "{schema_file_name}"')
def step_impl(context, schema_file_name):
    schema_file_name = os.getcwd() + '/resources/schema/' + sys.argv[1] + '/' + GlobalVar.testComponent[0].lower() \
                   + '/' + schema_file_name
    with open(schema_file_name, "r") as read_file:
        data = read_file.read()
        schema = json.loads(data)
        try:
            validate(instance=response_json, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as err:
            return False


@step(u'I receive valid HTTP response code "{response_code}" for "{request_name}"')
def validate_reponse_code(context, response_code, request_name):
    response_codes = GlobalVar.response_codes
    assert response_codes[request_name] == int(response_code)


@step(u'I receive valid response code "{response_code1}" or "{response_code2}" for "{request_name}"')
def validate_reponse_code(context, response_code1, response_code2, request_name):
    response_codes = GlobalVar.response_codes
    try:
        assert response_codes[request_name] == int(response_code1)
    except AssertionError:
        assert response_codes[request_name] == int(response_code2)
