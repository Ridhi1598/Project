import json
import time
import os

import jsonschema as jsonschema
import requests
from behave import given, when, then, step
from jsonschema import validate
from requests import HTTPError
from features.steps.api_steps_general import *

#declared variables
from features.steps.globalVar import GlobalVar

api_endpoints = {}
request_headers = {}
response_codes = {}
response_texts = {}
response_json = {}
request_bodies = {}
api_url = {}
responseVar = None
payload = {}
cookie_value = None


@step(u'I set LCD "{apiType}" url')
def step_impl(context, apiType):
    global api_url
    api_url = context.csvReadAPI[0].get("baseURL")
    GlobalVar.api_url = api_url
    print(api_url)


# START POST Scenario

@step(u'Set request Body for "{endpoint}"')
def step_impl(context, endpoint):
    global request_bodies
    global payload
    if endpoint.lower() == 'get_system_setting':
        payload = context.csvReadAPI[0].get(endpoint)
        print(payload)
    if endpoint.lower() == 'get_trans':
        payload = context.csvReadAPI[0].get(endpoint)
    if endpoint.lower() == 'new_trans':
        payload = context.csvReadAPI[0].get(endpoint)
    if endpoint.lower() == 'start_query':
        payloadVal = context.csvReadAPI[0].get(endpoint)
        payload = str(payloadVal).replace('1', str(responseVar))
    if endpoint.lower() == 'get_value':
        payloadVal = context.csvReadAPI[0].get(endpoint)
        payload = str(payloadVal).replace('1', str(responseVar))
    if endpoint.lower() == 'run_query':
        payloadVal = context.csvReadAPI[0].get(endpoint)
        payload = str(payloadVal).replace('6672', str(responseVar))
    if endpoint.lower() == 'stop_query':
        payloadVal = context.csvReadAPI[0].get(endpoint)
        payload = str(payloadVal).replace('6672', str(responseVar))
    if endpoint.lower() == 'login':
        payload = context.csvReadAPI[0].get(endpoint)
    if endpoint.lower() == 'given_enterprise':
        payload = context.csvReadAPI[0].get(endpoint)
    if endpoint.lower() == 'blankBody':
        payload = context.csvReadAPI[0].get(endpoint)
    if endpoint.lower() == 'get_given_enterprises':
        payload = context.csvReadAPI[0].get(endpoint)
    if endpoint.lower() == 'read_all_segment_under_an_enterprise':
        payload = context.csvReadAPI[0].get(endpoint)
    if endpoint.lower() == 'get_all_edges_under_an_enterprise':
        payload = context.csvReadAPI[0].get(endpoint)
    if endpoint.lower() == 'get_a_given_edge':
        payload = context.csvReadAPI[0].get(endpoint)
    if endpoint.lower() == 'get_edge_configuration_stack':
        payload = context.csvReadAPI[0].get(endpoint)
    GlobalVar.api_dict["payload"]= payload

@step(u'I receive valid HTTP response code 201')
def step_impl(context):
    print('Post rep code ;' + str(response_codes['POST']))
    assert response_codes['POST'] == 201


# END POST Scenario

# START GET Scenario
@step(u'I set GET api endpoint "{enpoint_param}"')
def step_impl(context, enpoint_param):
    api_endpoints['GET_URL'] = api_url + enpoint_param
    print('url :' + api_endpoints['GET_URL'])


@step(u'Send GET HTTP request')
def step_impl(context):
    # sending get request and saving response as response object
    try:
        response = requests.get(url=api_endpoints['GET_URL'],
                                headers=request_headers)  # https://jsonplaceholder.typicode.com/posts
        response.raise_for_status()
        # extracting response text
        response_texts['GET'] = response.text
        # extracting response json
        response_json['GET'] = response.json()
        # extracting response status_code
        statuscode = response.status_code
        response_codes['GET'] = statuscode


    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')

@step(u'Response BODY "{request_name}" is non-empty')
def step_impl(context, request_name):
    print('request_name: ' + request_name)
    print(response_texts)
    assert response_texts[request_name] is not None


@step(u'Response BODY for v1/health should have "{response_data_key}" as "{response_data_value}"')
def step_impl(context, response_data_key, response_data_value):
        print("Validating key-value pair from JSON response")
        # print(respon se_json['GET'])
        assert response_json[', response_data_key, '] == response_data_value


@step('I extract response value of "{data_key}"')
def step_impl(context, data_key):
    global responseVar
    # print(response_json['POST']['result'][data_key])
    for key in response_json:
        if key == 'POST':
            for key_nested in response_json[key]:
                if key_nested == 'result':
                    for key_nested2 in response_json[key][key_nested]:
                        if key_nested2 == data_key:
                            responseVar = response_json[key][key_nested][key_nested2]
                        # print(responseVar)
        else:
            print("Not Found")


@step(u'Response BODY should have "{response_data_key}" as "{response_data_value}"')
def step_impl(context, response_data_key, response_data_value):
    print(response_json.items())
    print(response_json['POST']['result']['th'])
    for key, value in response_json.items():
        print("Validating key-value pair from JSON response")
        print(response_data_key, ":", key)
        print(response_data_value, ":", value)
        print(key, ":", value)
        if key == response_data_key:
            print("Validating Key :", key)
        elif value == response_data_value:
            print("Validating value :", value)
        else:
            print("Error appearing ")


# END GET Scenario

# START PUT/UPDATE
@step(u'I Set PUT posts api endpoint for "{id}"')
def step_impl(context, id):
    api_endpoints['PUT_URL'] = api_url + '/posts/' + id
    print('url :' + api_endpoints['PUT_URL'])


@step(u'I Set Update request Body')
def step_impl(context):
    request_bodies['PUT'] = {"title": "foo", "body": "bar", "userId": "1", "id": "1"}


@step(u'Send PUT HTTP request')
def step_impl(context):
    # sending get request and saving response as response object  # response = requests.post(url=api_endpoints['POST_URL'], headers=request_headers) #https://jsonplaceholder.typicode.com/posts
    response = requests.put(url=api_endpoints['PUT_URL'], json=request_bodies['PUT'], headers=request_headers)
    # extracting response text
    response_texts['PUT'] = response.text
    print("update response :" + response.text)
    # extracting response status_code
    statuscode = response.status_code
    response_codes['PUT'] = statuscode


# END PUT/UPDATE

# START DELETE
@step(u'I Set DELETE posts api endpoint for "{id}"')
def step_impl(context, id):
    api_endpoints['DELETE_URL'] = api_url + '/posts/' + id
    print('url :' + api_endpoints['DELETE_URL'])


@step(u'Send DELETE HTTP request')
def step_impl(context):
    # sending get request and saving response as response object
    response = requests.delete(url=api_endpoints['DELETE_URL'])
    # response = requests.post(url=api_endpoints['POST_URL'], headers=request_headers) #https://jsonplaceholder.typicode.com/posts
    # extracting response text
    response_texts['DELETE'] = response.text
    print("DELETE response :" + response.text)
    # extracting response status_code
    statuscode = response.status_code
    response_codes['DELETE'] = statuscode
# END DELETE
