import json
import sys
import time
import os

import jsonschema as jsonschema
import requests
from behave import given, when, then, step
from jsonschema import validate
from requests import HTTPError
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



@step(u'I set SDWAN "{apiType}" url')
def step_impl(context, apiType):
    global api_url
    if apiType == "REST":
        url = 'sdwanAPIURL_' + sys.argv[2]
        api_url = context.config.get(url)
    elif apiType == "Functional":
        url = 'sdwanFunctionalURL_' + sys.argv[2]
        api_url = context.config.get(url)
    elif apiType == "Portal":
        url = "sdwanURL_dev"
        api_url = context.config.get(url)
    elif apiType == "Velo":
        url = 'sdwanFunctionalVelo_' + sys.argv[2]
        api_url = context.config.get(url)
    GlobalVar.api_url = api_url


@step(u'I Set HEADER param request "{header}" as "{header_content_type}" for SDWAN')
def step_impl(context, header, header_content_type):
    global request_headers
    if header.lower() == 'sdwancookie':
        header_content_type = 'velocloud.session='+cookie_value
        header = 'Cookie'
    request_headers[header] = header_content_type
    GlobalVar.api_dict['request_header'] = request_headers

@step(u'Set request Body for "{endpoint}" API of SDWAN')
def step_impl(context, endpoint):
    global request_bodies
    global payload
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
    GlobalVar.api_dict['payload'] = payload

@step(u'Send POST HTTP request for Login')
def step_impl(context):
    global cookie_value
    response = requests.post(url=api_endpoints['POST_URL'], json=request_bodies, headers=request_headers, data=payload)
    response_texts['POST'] = response.text
    print("post response :" + response.text)
    # extracting response status_code
    statuscode = response.status_code
    response_codes['POST'] = statuscode
    print(response_codes)
    print(response)
    cookie = response.cookies
    print(cookie['velocloud.session'])
    cookie_value = cookie['velocloud.session']