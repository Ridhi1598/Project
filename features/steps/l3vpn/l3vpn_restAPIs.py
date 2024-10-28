from behave import given, when, then, step
from features.steps.bi.bi_uiFunctional import *
from features.steps.api_steps_general import *

from features.steps.ui_steps_general import page_title_validation, change_currentPage
from features.steps.globalVar import GlobalVar

@step('I set L3VPN "{apiType}" url')
def set_l3_API_type(context, apiType):
    global api_url
    global url
    if apiType == 'REST':
        url = 'l3vpn_e2e_url_' + sys.argv[2]
    elif apiType == "IngestionEngine":
        url = 'l3vpn_ingestion_engine_url_' + sys.argv[2]
    elif apiType == "RMQ":
        url = 'l3vpn_RMQ_' + sys.argv[2]
    elif apiType == "ES":
        url = 'l3vpn_ES_' + sys.argv[2]
    api_url = context.config.get(url)
    GlobalVar.api_url = api_url
    return GlobalVar.api_url


@step('I Set HEADER param request "{header}" as "{header_content_type}" for L3VPN')
def set_header_request_l3vpn(context, header, header_content_type):
    if header == 'Authorization':
        if GlobalVar.testParams.get('Authorization') == 'Bearer Token':
            header_content_type = 'Bearer ' + GlobalVar.access_token
        else:
            header_content_type = GlobalVar.testParams.get('Authorization')
    request_headers[header] = header_content_type
    GlobalVar.api_dict['request_header'] = request_headers

