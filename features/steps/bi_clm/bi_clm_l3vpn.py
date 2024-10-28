from behave import *
import sys
import uuid
import time
import random
from typing import List
from common.util.es import EsUtilsL3
from common.util.rmq import RmqActions
from behave import step
import jsonschema
import json
import os
from common.util.common_util import common_globals_cs_evpn  #for cs-evpn
# common_globals_cs_evpn = CommonGlobals()    #for cs-evpn


from features.steps.globalVar import GlobalVar


class Req():
    requestId: str = None
    mock_server_callback: dict = {}
    es_service_rec_response: dict = {}
    es_request_rec_response: dict = {}
    tc_name: str = None


req = Req()
ES = EsUtilsL3()
RMQ = RmqActions()


def get_json_as_dict(path: str = None):
    with open(path) as f:
        data = json.load(f)
    return data


def check_if_str_in_mock_cb_err_msg(response, str):
    err_msg = response['event']['service']['statusChangeReason'][0]
    if str.lower().replace("'", "") in err_msg.lower().replace("'", ""):
        return True
    assert False, f'expected error msg :{str} but got {err_msg}'


def set_audit_flag(payload, flag):
    if payload["request-characteristics"]["url-query-parameters"][0]['name'] == 'audit':
        payload["request-characteristics"]["url-query-parameters"][0]['value'] = flag
    return payload


def prepare_update_payload(data, flag):
    data = set_audit_flag(data, flag)
    req_char = data["request-characteristics"]
    req_char['payload']['vpn-service'][0]['vpn-nodes']['vpn-node'][0]['vpn-network-accesses']['vpn-network-access'][
        0]['service']['ce-to-pe-bandwidth'] = GlobalVar.testParams.get(
        'bandwidth')
    req_char['payload']['vpn-service'][0]['vpn-nodes']['vpn-node'][0]['vpn-network-accesses']['vpn-network-access'][
        0]['service']['pe-to-ce-bandwidth'] = GlobalVar.testParams.get(
        'bandwidth')
    data["request-characteristics"] = req_char
    return data


def verify_if_key_matches_given_value(source_data, key_to_match, expected_value: str):
    if key_to_match == 'bandwidth':
        bandwidths = get_bandwidth(source_data)
        if bandwidths[0] != expected_value or bandwidths[1] != expected_value:
            return False
        return True


def inject_to_payload(data, payload_for='l3queue', action_type='add', request_state=None, audit_flag=False,
                      vpn_node_selector='primary'):
    #
    reqId = str(uuid.uuid4())
    req.requestId = reqId
    l2vpn_id = GlobalVar.testParams.get('l2vpn-id')
    node_service_id = GlobalVar.testParams.get('node_service_id')

    vpn_service_name = GlobalVar.testParams.get('vpn_service_name') + '-BI_CLM'
    if payload_for == 'l3esdb':
        vpn_node_id = GlobalVar.testParams.get('vpn_nid_to_add_to_es')
        ne_id = vpn_node_id.split('-')[0]
        # href_url = '/'.join(data['href'].split('/')[:-1]) + '/vpn-nodes=' + vpn_node_id

        if action_type == 'add':
            url = data['href']
            parts = url.split('=')
            href_url = url.replace(parts[1].split('/')[0], vpn_service_name).replace(parts[2], vpn_node_id) if len(
                parts) == 3 else url.replace(parts[1].split('/')[0], vpn_service_name)
            data['id'] = vpn_node_id

            if request_state:
                data['state'] = request_state
            if request_state == 'in_progress':
                data['in_progress'] = True

            data['href'] = href_url
            data['vpn-id'] = vpn_service_name
            data["network-payload"]['config']['vpn-service'][0]['vpn-nodes']['vpn-node'][0]['vpn-node-id'] = vpn_node_id
            data['network-payload']['config']['vpn-service'][0]['vpn-nodes']['vpn-node'][0][
                'ne-id'] = ne_id
            data['network-payload']['config']['vpn-service'][0]['vpn-name'] = vpn_service_name
            data['network-payload']['config']['vpn-service'][0]['vpn-id'] = vpn_service_name
            data['network-payload']["config"]["vpn-service"][0]["vpn-nodes"]["vpn-node"][0][
                "vpn-network-accesses"]["vpn-network-access"][0]["connection"]["l2vpn-id"] = l2vpn_id
            data['network-payload']["config"]["vpn-service"][0]["vpn-nodes"]["vpn-node"][0][
                "vpn-network-accesses"][
                "vpn-network-access"][0]["tinaa-l3vpn-ntw-augment:telus-network-access-info"][
                "node-service-id"] = node_service_id
        if action_type == 'delete-mwr':
            url = data["request-characteristics"]["url"]
            parts = url.split('=')
            href_url = url.replace(parts[1].split('/')[0], vpn_service_name).replace(parts[2], vpn_node_id) if len(
                parts) == 3 else url.replace(parts[1].split('/')[0], vpn_service_name)
            data["request-characteristics"]["url"] = href_url
            data["request-characteristics"]["response"]["requestId"] = data["id"] = reqId

            if data["request-characteristics"]["url-query-parameters"][0]['name'] == 'audit':
                data["request-characteristics"]["url-query-parameters"][0]['value'] = audit_flag

    else:
        vpn_node_id = GlobalVar.testParams.get('vpn_node_id')

        url = data["request-characteristics"]["url"]
        parts = url.split('=')
        href_url = url.replace(parts[1].split('/')[0], vpn_service_name).replace(parts[2], vpn_node_id) if len(
            parts) == 3 else url.replace(parts[1].split('/')[0], vpn_service_name)
        # href_url = '/'.join(data["request-characteristics"]["url"].split('/')[
        #                     :-1]) + '/vpn-nodes=' + vpn_node_id if vpn_node_id else '/'.join(data["request-characteristics"]["url"].split('/')[:-1])
        data["request-characteristics"]["url"] = href_url

        if action_type == 'add':
            req.requestId = data['request-characteristics']['response']['requestId'] = data['id'] = reqId
            #
            ne_id = vpn_node_id.split('-')[0]
            data['request-characteristics']['payload']['vpn-service'][0]['vpn-nodes']['vpn-node'][0]['ne-id'] = ne_id
            data['request-characteristics']['payload']['vpn-service'][0]['vpn-nodes']['vpn-node'][0][
                'vpn-node-id'] = vpn_node_id
            #
            node_service_id = GlobalVar.testParams.get('node_service_id')
            data["request-characteristics"]["payload"]['vpn-service'][0]['vpn-name'] = vpn_service_name
            data["request-characteristics"]["payload"]['vpn-service'][0]['vpn-id'] = vpn_service_name
            data["request-characteristics"]["payload"]["vpn-service"][0]["vpn-nodes"]["vpn-node"][0][
                "vpn-network-accesses"]["vpn-network-access"][0]["connection"]["l2vpn-id"] = l2vpn_id
            data["request-characteristics"]["payload"]["vpn-service"][0]["vpn-nodes"]["vpn-node"][0][
                "vpn-network-accesses"][
                "vpn-network-access"][0]["tinaa-l3vpn-ntw-augment:telus-network-access-info"][
                "node-service-id"] = node_service_id
            #
        if action_type == 'delete':
            if vpn_node_selector == 'secondary':
                vpn_node_id = GlobalVar.testParams.get('vpn_nid_to_add_to_es')
            url = data["request-characteristics"]["url"]
            parts = url.split('=')
            href_url = url.replace(parts[1].split('/')[0], vpn_service_name).replace(parts[2], vpn_node_id) if len(
                parts) == 3 else url.replace(parts[1].split('/')[0], vpn_service_name)
            data["request-characteristics"]["url"] = href_url
            data["request-characteristics"]["response"]["requestId"] = data["id"] = reqId

            if data["request-characteristics"]["url-query-parameters"][0]['name'] == 'audit':
                data["request-characteristics"]["url-query-parameters"][0]['value'] = audit_flag

    return data


def validate_schema(payload, schema):
    jsonschema.validate(payload, schema)
    return True


def get_hit_by_id(id, data):
    hits = data['hits']['hits']
    for hit in hits:
        if hit['_id'] == id:
            return hit
    return None


# def find_status(correlation_id, value, json_obj):
#     found_unmatched = False
#     for obj in json_obj:
#         payload = json.loads(obj['payload'])
#         if payload['correlationId'] == correlation_id:
#             found_unmatched = True
#             req.mock_server_callback = payload
#             if payload['event']['service']['status'] == value:
#                 print(f'state of request with id: {correlation_id} is {value}')
#                 return payload
#             else:
#                 pass
#     if found_unmatched:
#         assert False, f"state not matched of request with id: {correlation_id} state is {payload['event']['service']['status']} but expected {value}"
#     assert False, 'Empty response from Queue'

# def find_status(correlation_id, value, json_obj):
#     not_found = True
#     for obj in json_obj:
#         payload = json.loads(obj['payload'])
#         if 'correlationId' in payload:
#             if payload.get('correlationId') == correlation_id and payload['event']['service']['status'] == value:
#                 not_found = False
#                 print(f'state of request with id: {correlation_id} is {value}')
#                 req.mock_server_callback = payload
#                 return payload
#     if not_found:
#         return False, f"request with id: {correlation_id} not found"
#     else:
#         return False, f"state not matched of request with id: {correlation_id} state is {payload['event']['service']['status']} but expected {value}"


# def find_status(correlation_id, value, max_attempts=3, timeout=10):
#     return next((payload for _ in range(max_attempts) for obj in RMQ.orch_res_test_cb_get() if
#                  'correlationId' in (payload := json.loads(obj['payload'])) and payload[
#                      'correlationId'] == correlation_id and payload['event']['service']['status'] == value and (
#                              time.sleep(timeout) or True)), False)


def find_status(correlation_id, state, max_attempts=10, timeout=5, check_if_config_key_present=False,
                is_a_timeout_res=False, expected_error_msg_string_match=None):
    for attempt in range(max_attempts):
        rmq_cbs = RMQ.orch_res_test_cb_get()

        for obj in rmq_cbs:
            payload = json.loads(obj['payload'])
            if 'correlationId' in payload and payload['correlationId'] == correlation_id and \
                    payload['event']['service']['status'] == state:
                if 'statusChangeReason' in payload['event']['service']:
                    status_change_reason = payload['event']['service']['statusChangeReason'][0]
                    print(f"statusChangeReason value: {status_change_reason}")
                if check_if_config_key_present and state.lower() == 'success':
                    if "configs" not in payload["event"]["service"]:
                        if 'success' in Req.tc_name.lower():
                            assert False, f"Callback does not contains configs key: Received response {payload['event']['service']}"
                        else:
                            print("Config not found: Failed scenario")

                if is_a_timeout_res:
                    if 'timeout' not in payload['event']['service']['statusChangeReason'][0].lower():
                        assert False, f"Expected a Timeout error but got {payload['event']['service']['statusChangeReason']}"
                if expected_error_msg_string_match:
                    if expected_error_msg_string_match.lower() not in payload['event']['service']['statusChangeReason'][
                        0].lower():
                        assert False, f"Expected a {expected_error_msg_string_match.lower()} msg but got {payload['event']['service']['statusChangeReason'][0]}"
                print(f'state of request with id: {correlation_id} is {state}')
                req.mock_server_callback = payload
                return payload
        time.sleep(timeout)
    assert False, f"Request failed after {max_attempts} attempts."


def __get_external_request_tracker(json_obj, doc_id):
    data = [hit['_source']['external-request-tracker'] for hit in json_obj.get('hits', {}).get('hits', []) if
            hit['_id'] == doc_id]
    return data[0] if data else False


def __get_callback_info_from_request_record(json_obj, doc_id):
    data = [hit['_source']['callback-info'] for hit in json_obj.get('hits', {}).get('hits', []) if
            hit['_id'] == doc_id]
    return data[0] if data else False


def __get_resource_validator_data_from_req_tracker_res(ext_req_trackers: List = []):
    return next((dt['request-characteristics'] for dt in ext_req_trackers if
                 dt.get('request-characteristics', {}).get('request_type') == 'CREATE_NODE.VALIDATE_RESOURCES'), False)


def get_bandwidth(data):
    pe_to_ce_bandwidth = \
        data['hits']['hits'][0]['_source']['network-payload']['config']['vpn-service'][0]['vpn-nodes']['vpn-node'][0][
            'vpn-network-accesses']['vpn-network-access'][0]['service']['pe-to-ce-bandwidth']
    ce_to_pe_bandwidth = \
        data['hits']['hits'][0]['_source']['network-payload']['config']['vpn-service'][0]['vpn-nodes']['vpn-node'][0][
            'vpn-network-accesses']['vpn-network-access'][0]['service']['ce-to-pe-bandwidth']
    return ce_to_pe_bandwidth, pe_to_ce_bandwidth


def __get_ntwrk_package_data_from_req_tracker_res(ext_req_trackers: List = []):
    return next((dt['request-characteristics'] for dt in ext_req_trackers if
                 dt.get('request-characteristics', {}).get('request_type') == 'CREATE_NODE.NODE'), False)


def __get_create_profile_data_from_req_tracker_res(ext_req_trackers: List = []):
    return next((dt['request-characteristics'] for dt in ext_req_trackers if
                 dt.get('request-characteristics', {}).get('request_type') == 'CREATE_NODE.CREATE_PROFILES'), False)


def __get_timeout_data_from_req_tracker_res(ext_req_trackers: List = []):
    return next((dt['request-characteristics'] for dt in ext_req_trackers if
                 dt.get('request-characteristics', {}).get('request_type') == 'CREATE_NODE.TIMEOUT'), False)


def __get_request_record_final_state(json_obj):
    status = json_obj['hits']['hits'][0]['_source']['state']
    # status = json_obj['hits']['hits'][0]['_source']['callback-info']['response']['event']['service']['status']
    return status


def get_service_in_progress_state(expected_state, timeout=120, service_id: str = None):
    if not service_id:
        ES.SEARCH_STR = GlobalVar.testParams.get('vpn_node_id')
    else:
        ES.SEARCH_STR = service_id
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        time.sleep(10)
        service_data = ES.query_service_index()
        service_state = service_data['hits']['hits'][0]['_source']['in_progress']
        if service_state == expected_state:
            return True
    else:
        # Timeout was reached, raise an exception or log an error
        raise TimeoutError(f'Timed out, expected status {expected_state} but got {service_state}')


def mediation_mock_cb(expected_req_type, expected_state):
    timeout = 50  # Timeout in seconds
    start_time = time.time()
    req_cb_info = None  # Initialize to None before the loop
    found = 0
    while (time.time() - start_time) < timeout:
        time.sleep(10)  # Wait for 10 seconds before retrying
        req.es_request_rec_response = check_if_index_found_in_es('request-record', req.requestId)
        available_hits = req.es_request_rec_response['hits']['hits']
        for hits in available_hits:
            if hits['_id'] == req.requestId:
                external_requests_trackers = hits['_source']['external-request-tracker']
                for i in range(len(external_requests_trackers)):
                    # for _i in range(found):
                    #     del external_requests_trackers[0]
                    _request = external_requests_trackers[i]
                    req_char = _request['request-characteristics']
                    try:
                        req_cb_info = _request['callback-info']
                        # if callback-info received then we will remove that dict before next iteration
                        req_type = req_char['request_type']
                        req_state = req_cb_info['payload']['state'].lower()
                        if req_type == f'CREATE_NODE.{expected_req_type}' and req_state == expected_state:
                            print(f'Passed:- Request type: {req_type} and State received: {req_state}')
                            return True
                        else:
                            err_msg = req_cb_info['payload']['errors'][0]['category']
                            print(req_cb_info['payload']['errors'])
                            if req_type == 'CREATE_NODE.CREATE_PROFILES' and err_msg == 'RESOURCE_EXIST':
                                print(f'Passed:- Request type: {req_type} and message: {err_msg}')
                                return True
                            return False, f'FAILED: {req_type} {req_state}'
                    except KeyError:
                        # 'callback-info' field not found, continue with next hit
                        pass
        # If the 'callback-info' field was found, break out of the loop
        if req_cb_info is not None:
            break
    else:
        # Timeout was reached, raise an exception or log an error
        raise TimeoutError('Timed out waiting for callback-info field.')


# def check_if_index_found_in_es(record_type, doc_id, expected_state: str = None):
#     time.sleep(10)
#     ES.SEARCH_STR = doc_id
#     response = ES.query_service_index() if record_type.lower() == 'service-record' else ES.query_request_index()
#     print(response)
#     pass_flag = False
#     if isinstance(response, dict) and 'hits' in response:
#         total_found = response['hits']['total']['value']
#         found_list = response['hits']['hits']
#         if len(found_list) > 0:
#             # something found
#             # validate if service with our id found or not
#             for each in found_list:
#                 if each['_id'] == doc_id:
#                     if not expected_state:
#                         print(f'Given document: {doc_id} found in {record_type}')
#                         return response
#                     pass_flag = True
#                     if each['_source']['state'] == expected_state:
#                         print(f'Given document: {doc_id} found in {record_type} with state: {expected_state}')
#                         return response
#                     else:
#                         assert False, f"Doc Found in state {each['_source']['state']} but expected state was {expected_state}"
#
#         if len(found_list) != total_found:
#             print(f'Response json verification failed, total found:{total_found} but hits list contains : {found_list}')
#     else:
#         assert False, f"ES Response is not a dictionary or does not contain 'hits'. Response received: {response}"
#     return pass_flag


def check_if_index_found_in_es(record_type, doc_id, request_state: str = None, in_progress_state: bool = None,
                               max_retries=12, timeout=5):
    retries = 0
    pass_flag = False

    while retries < max_retries:
        try:
            ES.SEARCH_STR = doc_id
            response = ES.query_service_index() if record_type.lower() == 'service-record' else ES.query_request_index()
            if isinstance(response, dict) and len(response['hits']['hits']) > 0:
                total_found = response['hits']['total']['value']
                found_list = response['hits']['hits']

                if len(found_list) > 0:
                    # something found
                    # validate if service with our id found or not
                    for each in found_list:
                        if each['_id'] == doc_id:
                            if in_progress_state is not None:

                                if each['_source']['in_progress'] == in_progress_state:
                                    print(
                                        f'Given document: {doc_id} in-progress state is {each["_source"]["in_progress"]}')
                                    return response
                                else:
                                    assert False, f'Expected "in_progress": {in_progress_state} but got "in_progress": {each["_source"]["in_progress"]}'

                            if not request_state:
                                print(f'Given document: {doc_id} found in {record_type}')
                                return response
                            pass_flag = True
                            if each['_source']['state'] == request_state:
                                print(
                                    f'Given document: {doc_id} found in {record_type} with state: {request_state}')
                                return response
                            else:
                                assert False, f"Doc Found in state {each['_source']['state']} but expected state was {request_state}"

                if len(found_list) != total_found:
                    print(
                        f'Response json verification failed, total found:{total_found} but hits list contains: {found_list}')
            # else:
            #     print(
            #         f"Service not found\nResponse received: {response}")
            #     # return pass_flag
            retries += 1
            print(f"Retrying... ({retries}/{max_retries})")
            time.sleep(timeout)


        except Exception as e:
            retries += 1
            time.sleep(timeout)
            print(f"Error occurred: {e}")
            # Retry after a delay
            print(f"Retrying... ({retries}/{max_retries})")

    print(f"Service or the expected state not found. Reached maximum number of retries ({max_retries})")

    return pass_flag


def get_feature_number_from_feature_file(filename):
    return '_'.join(filename.split('_')[:2])


# def extract_ids(elasticsearch_response):
#     hits = elasticsearch_response["hits"]["hits"]
#     id_list = [hit["_id"] for hit in hits if "TST0040-12347" in hit["_id"]]
#     return id_list


# all_service = ES.query_service_index_match_all()
# list_of_service_ids_created_by_us = extract_ids(all_service)
# # delete all these services
# for id in list_of_service_ids_created_by_us:
#     ES.delete_es_record(id)


#
# Below function shorter and more concise version of the above function
# but it is not yet tested properly
#
# def check_if_index_found_in_es(record_type, doc_id):
#     ES.SEARCH_STR = doc_id
#     response = ES.query_service_index() if record_type.lower() == 'service-record' else ES.query_request_index()
#     found_list = [hit for hit in response.get('hits', {}).get('hits', []) if hit['_id'] == doc_id]
#     if found_list:
#         print(f'Given document found in {record_type}')
#         return response
#     else:
#         print(f'Given document not found in {record_type}')
#         if response.get('hits', {}).get('total', {}).get('value', 0) != len(found_list):
#             print(f"Response json verification failed, total found:{response['hits']['total']['value']} but hits list contains: {found_list}")
#         return False
@step("I will add one more in-progress service before sending the actual CRUD request")
@step("Sending a new service (CRUD) request but before that I will make sure it is not already in DB")
def step_skip(context):
    pass


@step("Sending create-service payload to L3VPN via RMQ")
@step("Sending create-node payload to L3VPN via RMQ")
def step_impl(context):
    context.es_service_id = GlobalVar.testParams.get('vpn_node_id')
    project_dir_from_here = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    file_path = os.path.join(project_dir_from_here, "resources", "payload", "bi_clm", "l3vpn", "create.json")
    data = get_json_as_dict(file_path)
    RMQ.PAYLOAD_PUBLISH = inject_to_payload(data)
    RMQ.orch_req_publish()
    time.sleep(5)


@step("Sending {req_type} with audit {audit_flag} payload to L3VPN via RMQ")
def step_impl(context, req_type, audit_flag):
    if 'delete' not in req_type.lower():
        payload_filename = req_type.replace('-', '_')
    else:
        payload_filename = 'delete'
    project_dir_from_here = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    file_path = os.path.join(project_dir_from_here, "resources", "payload", "bi_clm", "l3vpn",
                             f"{payload_filename}.json")
    data = get_json_as_dict(file_path)

    if payload_filename == 'delete':
        vpn_node_id = 'primary'
        RMQ.PAYLOAD_PUBLISH = set_audit_flag(data, audit_flag)
        if 'node' in req_type.lower():
            vpn_node_id = 'secondary'
        RMQ.PAYLOAD_PUBLISH = inject_to_payload(data, action_type='delete', vpn_node_selector=vpn_node_id,
                                                audit_flag=audit_flag)
    else:
        RMQ.PAYLOAD_PUBLISH = prepare_update_payload(data, audit_flag)
        RMQ.PAYLOAD_PUBLISH = inject_to_payload(data)

    RMQ.orch_req_publish()


@step("Sending {update_req_type} payload via RMQ")
def step_impl(context, update_req_type: str):
    payload_filename = update_req_type.replace('-', '_')
    project_dir_from_here = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    file_path = os.path.join(project_dir_from_here, "resources", "payload", "bi_clm", "l3vpn",
                             f"{payload_filename}.json")
    data = get_json_as_dict(file_path)
    RMQ.PAYLOAD_PUBLISH = inject_to_payload(data)
    RMQ.PAYLOAD_PUBLISH = prepare_update_payload(RMQ.PAYLOAD_PUBLISH, False)
    RMQ.orch_req_publish()


@step('Sending {event} payload with mwr param to L3VPN via RMQ')
def step_impl(context, event):
    context.es_service_id = GlobalVar.testParams.get('vpn_node_id')
    if check_if_index_found_in_es('service-record', context.es_service_id, max_retries=2,timeout=5):
        print(f'{context.es_service_id} already exists. Deleting...')
        ES.delete_es_record(context.es_service_id)
    project_dir_from_here = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    file_path = os.path.join(project_dir_from_here, "resources", "payload", "bi_clm", "l3vpn", "create_mwr.json")
    data = get_json_as_dict(file_path)
    RMQ.PAYLOAD_PUBLISH = inject_to_payload(data)
    RMQ.orch_req_publish()
    time.sleep(5)


@step("Validating that request-record is in {expected_state} state")
def step_impl(context, expected_state):
    check_if_index_found_in_es('request-record', req.requestId, request_state=expected_state)


@step("Validating that {record_type} is created in ES")
def step_impl(context, record_type):
    req.es_service_rec_response = check_if_index_found_in_es(record_type, context.es_service_id)


@step("Validating that service-record in-progress is set to {given_flag}")
def step_impl(context, given_flag):
    flag = False
    if given_flag.lower() == "true":
        flag = True
    req.es_service_rec_response = check_if_index_found_in_es('service-record', context.es_service_id,
                                                             in_progress_state=flag)
    if not req.es_service_rec_response:
        assert False, 'Unable to fetch service from service-record'
    # flag = False
    # if given_flag.lower() == "true":
    #     flag = True
    # for i in range(12):
    #     req.es_service_rec_response = check_if_index_found_in_es('service-record', context.es_service_id,
    #                                                              in_progress_state=flag)
    #     actual_in_progress_value = req.es_service_rec_response['hits']['hits'][0]['_source']['in_progress']
    #     req.es_service_rec_response = {}
    #     if actual_in_progress_value == flag:
    #         return
    #     time.sleep(5)
    # assert False, f'Expected "in_progress": {given_flag} but got "in_progress": {actual_in_progress_value}'


@step("Validating that {record_type} is not created in ES")
def step_impl(context, record_type):
    max_attempts = 10  # Maximum number of attempts
    attempt = 0
    context.es_service_id = GlobalVar.testParams.get('vpn_node_id')
    if check_if_index_found_in_es('service-record', context.es_service_id, max_retries=2, timeout=3):
        print('Service found in DB')
        while attempt < max_attempts:
            response = ES.delete_es_record(context.es_service_id)
            if response.get("result") == "not_found":
                break
            else:
                print("Service is still in ES, retrying")
                attempt += 1
        else:
            attempt += 1
        time.sleep(5)
        if attempt == max_attempts:
            print("Timeout: Max attempts reached")


@step("Performing cleanup: {clean_up_type}")
def step_impl(context, clean_up_type):
    vpn_node_id_sec = GlobalVar.testParams.get('vpn_nid_to_add_to_es')
    vpn_node_id_pri = GlobalVar.testParams.get('vpn_node_id')
    vpn_nodes_list = [vpn_node_id_pri, vpn_node_id_sec]
    max_attempts = 10  # Maximum number of attempts
    attempt = 0
    for node in vpn_nodes_list:
        while attempt < max_attempts:
            response = ES.delete_es_record(node)
            if response.get("result") == "not_found":
                break
            else:
                attempt += 1
        else:
            attempt += 1
        time.sleep(5)
        if attempt == max_attempts:
            print("Timeout: Max attempts reached")


@step("Validating that {state} callback is published to orchestrator-response queue")
def step_impl(context, state):
    Req.tc_name = context.feature.filename
    is_timeout_flag = False
    display_config_flag = False
    if state.lower() == 'error':
        if 'timeout' in Req.tc_name.lower():
            is_timeout_flag = True
    if 'audit_true' in Req.tc_name.lower() or 'with_display_config' in Req.tc_name.lower():
        display_config_flag = True
    find_status(req.requestId, state, check_if_config_key_present=display_config_flag, is_a_timeout_res=is_timeout_flag)


@step("validating that service record {key_to_match} is changed")
def step_impl(context, key_to_match):
    get_service_in_progress_state(False)
    ES.SEARCH_STR = GlobalVar.testParams.get('vpn_node_id')
    service_data = ES.query_service_index()
    expected_value = GlobalVar.testParams.get(key_to_match)
    if not verify_if_key_matches_given_value(service_data, key_to_match, expected_value):
        assert False, f'Failed: Expected ({expected_value}) value not found'


@step("validating that service record {key_to_match} is not changed")
def step_impl(context, key_to_match):
    get_service_in_progress_state(False)
    ES.SEARCH_STR = GlobalVar.testParams.get('vpn_node_id')
    service_data = ES.query_service_index()
    expected_value = GlobalVar.testParams.get(key_to_match)
    if verify_if_key_matches_given_value(service_data, key_to_match, expected_value):
        assert False, f'Failed: service record got update with value {expected_value}'


@step("Validating that {state} callback with config is published to orchestrator-response queue")
def step_impl(context, state, check_if_config_key_present=True):
    find_status(req.requestId, state)


@step("Validating that {state} callback message in orchestrator-response queue contains {string} string")
def step_impl(context, state, string=None):
    find_status(req.requestId, state, expected_error_msg_string_match=string)


@step("Validating that service-record is deleted")
def step_impl(context):
    if check_if_index_found_in_es('service-record', GlobalVar.testParams.get('vpn_node_id')):
        assert False, 'service found in service-records'


@step("Validating schema of {state} callback published in {component}")
def step_impl(context, component, state):
    schema_path = None
    if component.lower() == 'orchestrator':
        project_dir_from_here = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        schema_path = os.path.join(project_dir_from_here, "resources", "schema", "bi_clm", "l3vpn", f"{state}.json")
    if component.lower() == 'evpn':
        project_dir_from_here = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        schema_path = os.path.join(project_dir_from_here, "resources", "schema", "cs", "evpn", f"{state}.json")
    schema = get_json_as_dict(schema_path)
    callback_to_validate = req.mock_server_callback
    if not callback_to_validate:
        callback_to_validate = common_globals_cs_evpn.rmq_msg_callback
    if validate_schema(callback_to_validate, schema):
        print('Schema validation passed')


@step("Validating that request-record state is {state}")
def step_impl(context, state):
    time.sleep(50)
    request_state = __get_request_record_final_state(req.es_request_rec_response).lower()
    if request_state != state.lower():
        assert False, f'Expected state {state} but got {request_state}'


def mock_server_callback_reader(expected_req_type, expected_state, reqId, timeout=60):
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout period of {timeout} seconds has expired.")
        time.sleep(5)
        ES.SEARCH_STR = reqId
        req.es_request_rec_response = ES.query_request_index()
        ext_tr = __get_external_request_tracker(req.es_request_rec_response, reqId)
        if expected_req_type == 'VALIDATE_RESOURCES':
            data = __get_resource_validator_data_from_req_tracker_res(ext_tr)
            request_status = data['state']
        elif expected_req_type == 'CREATE_PROFILES':
            data = __get_create_profile_data_from_req_tracker_res(ext_tr)
            if not data:
                return False
            request_status = data['state']
            if request_status.lower() == 'failed':
                return True
        elif expected_req_type == 'TIMEOUT':
            data = __get_timeout_data_from_req_tracker_res(ext_tr)
            if not data:
                return False
            request_status = data['state']
        elif expected_req_type == 'NODE':
            data = __get_ntwrk_package_data_from_req_tracker_res(ext_tr)
            if not data:
                return False
            request_status = data['state']
            if request_status.lower() == expected_state.lower():
                return True
        else:
            assert False, f'{expected_req_type} not supported'

        if request_status.lower() == expected_state.lower():
            return True
        elif request_status.lower() == 'in-progress':
            time.sleep(10)
        else:
            assert False, f'Expected state for {expected_req_type} is {expected_state}/in-progress but got {request_status}'


@step("Validating that callback is received for {expected_req_type} in {expected_state} state")
def step_impl(context, expected_req_type, expected_state):
    data = mock_server_callback_reader(expected_req_type, expected_state, req.requestId)
    if not data:
        assert False, 'Expected callback not found'


@step("Validating that callback response contains {expected_string} error message")
def step_impl(context, expected_string):
    cb_info = __get_callback_info_from_request_record(req.es_request_rec_response, ES.SEARCH_STR)
    check_if_str_in_mock_cb_err_msg(cb_info['response'], expected_string)


@step("I am Adding a service to L3VPN es-record")
@step("I am Adding a {request_state} service to L3VPN es-record")
@step("Adding service to L3VPN es-record")
@step("Adding {request_state} service to L3VPN es-record")
def step_impl(context, request_state=None):
    if request_state:
        request_state = request_state.replace('-', '_')
    payload_filename = 'payload_add_ser_to_l3_es.json'
    tc_name = context.feature.filename
    if 'mwr' in tc_name.lower():
        payload_filename = 'payload_add_mwr_ser_to_l3_es.json'
    context.es_service_id = GlobalVar.testParams.get('vpn_nid_to_add_to_es')
    # if 'rate' in tc_name.lower():
    #     # Replace the last two zeroes with the random integer
    #     context.es_service_id = GlobalVar.testParams.get('vpn_nid_to_add_to_es')[:-8] + str(random.randint(10, 99999999))

    project_dir_from_here = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    # tc_name = get_feature_number_from_feature_file(context.config.feature_file)
    file_path = os.path.join(project_dir_from_here, "resources", "payload", "bi_clm", "l3vpn",
                             payload_filename)
    ES.delete_es_record(context.es_service_id)
    data = inject_to_payload(get_json_as_dict(file_path), payload_for='l3esdb', action_type='add',
                             request_state=request_state)
    service_request = ES.create_es_service(context.es_service_id, json.dumps(data))
    if service_request['result'] != 'created':
        assert False, f'Service request failed, result: {service_request["result"]}'
    # context.created_services.append(context.es_service_id)


@step("Sending delete-node payload to L3VPN via RMQ")
@step("Sending delete-service payload to L3VPN via RMQ")
def step_impl(context):
    project_dir_from_here = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    file_path = os.path.join(project_dir_from_here, "resources", "payload", "bi_clm", "l3vpn",
                             "delete.json")
    RMQ.PAYLOAD_PUBLISH = inject_to_payload(get_json_as_dict(file_path), payload_for='l3queue', action_type='delete')
    # exit()
    RMQ.orch_req_publish()
    time.sleep(5)


# todo some issue with below step
@step("Sending delete-mwr-node payload to L3VPN via RMQ")
def step_impl(context):
    project_dir_from_here = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    file_path = os.path.join(project_dir_from_here, "resources", "payload", "bi_clm", "l3vpn",
                             "delete.json")
    RMQ.PAYLOAD_PUBLISH = inject_to_payload(get_json_as_dict(file_path), payload_for='l3esdb', action_type='delete-mwr')
    # exit()
    RMQ.orch_req_publish()
    time.sleep(5)
