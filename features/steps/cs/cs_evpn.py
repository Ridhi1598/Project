import requests
from behave import *
import sys
import uuid
import time
import random
from typing import List

from common.util.common_util import PayloadUtil, common_globals_cs_evpn, common_globals_cs_orch
from common.util.es import EsUtilsL3
from common.util.rmq import RmqActions
from behave import step
import jsonschema
import json
import os

from features.steps.bi_clm.bi_clm_l3vpn import find_status
from features.steps.globalVar import GlobalVar
from common.util.rmqv2 import RmqActions, CS

RmqAct = RmqActions()
RmqAct.EXCHANGE = CS.EXCHANGE
RmqAct.BASE_URL = CS.API_BASE_URL
CsEvpnPayloadUtil = PayloadUtil.CS.EVPN()
CommonPayloadUtil = PayloadUtil()

max_retries = 7
retry_delay = 10


def check_if_request_exist_by_id_and_status(data_list, request_id, status: str = None):
    for item in data_list:
        try:
            payload = item['payload']
            payload_data = json.loads(payload)
            if payload_data['request-id'] == request_id:
                if not status:
                    return payload_data
                if payload_data['status'] == status:
                    return payload_data
            print(f'Callback found but not in expected state, '
                  f'Found in {payload_data["status"]}, Retrying...')
        except (json.JSONDecodeError, KeyError):
            continue
    return False


# common
def get_feature_filename(context):
    return context.split('/')


external_Request_tracker = {
    "id": "690fe158-e549-40ef-9981-1f8b08456b26",
    "state": "COMPLETED",
    "parent_request_tracker_id": "70d8d02a-a3d2-4221-a37d-748bc2640262",  # Request_id
    "external_id": "c4f5182b8dc512e7a0b6e6c1c175bdbb"
}

evpn_bsaf_request_tracker = {
    "result": [
        {
            "id": "70d8d02a-a3d2-4221-a37d-748bc2640262",  # request_id
            "state": "PENDING CONFIRMATION"  # this is success for dry run
        }
    ],
    "message": "Data fetch successfully"
}


# evpn_Service table me dekhna
def execute_select_query(table_name: str = None, col_names=['*'], where_conditions=None):
    col_name_str = ', '.join(f'{col}' for col in col_names)
    # external_Request_tracker.id = parent_request_tracker_id
    # Construct the SQL query
    if where_conditions:
        where_clause = ' AND '.join(f"{key} = '{value}'" for key, value in where_conditions.items())
        query_prepared = f"SELECT {col_name_str} FROM {table_name} WHERE {where_clause};"
    else:
        query_prepared = f"SELECT {col_name_str} FROM {table_name};"
    url = "https://bi-mocking-server.qa.app01.toll6.tinaa.tlabs.ca/query-v2"
    payload = json.dumps({
        "query": query_prepared,
        "controller_name": "orchestrator"  # credential works for all component, so no need to change for evpn,bng etc
    })
    print("Qeury*******************")
    print(query_prepared)
    headers = {
        'Content-Type': 'application/json'
    }

    print("url*******************")
    print(url)

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    print("Response*******************")
    print(response)

    return response.json()


# @step("Publishing payload to RMQ")
# def publish_to_rmq(context):
#     fn = context.feature.filename
#     payload_prepared = CommonPayloadUtil.prepare_payload(feature_name=fn, app_name=common_globals_cs_evpn.app)
#     common_globals_cs_evpn.requestId = payload_prepared['request-id-generated']
#     print(common_globals_cs_evpn.requestId)
#     RmqAct.ROUTING_KEY = CS.RoutingKeys.PUBLISH_TO_EVPN
#     RmqAct.PAYLOAD_PUBLISH = payload_prepared['payload']
#     # RmqAct.publish_message()
#     time.sleep(5)

# def get_request_id_from_common_globals():
#     if common_globals_cs_evpn.requestId:
#         return common_globals_cs_evpn.requestId
#     elif common_globals_cs_orch
def get_validator_column_name_and_value(table):
    validator_col_identifier = 'id'
    if 'orch' in table:
        validator_col_value = common_globals_cs_orch.requestId  # '69569f30-e590-4fe0-ac75-f0a7c84d76d9'
    if 'evpn' in table:
        validator_col_value = common_globals_cs_evpn.requestId
    # where id = 'req_id'
    if '_external_request_tracker' in table:
        validator_col_identifier = 'parent_request_tracker_id'
    if table == 'evpn_service' or table == 'interface':
        validator_col_identifier = 'service_name'
        validator_col_value = GlobalVar.testParams.get('service_name')
    return validator_col_identifier, validator_col_value


@step("Validating that {table_name} record {flag_created} created")
@step("Validating that {table_name} record is {action} with {state} state")
def verify_request_in_postgres_db(context, table_name: str = None, flag_created: str = None, action: str = None,
                                  state: str = None):
    retries = 0

    validator_col_identifier, validator_col_value = get_validator_column_name_and_value(table_name)
    # if state.lower() == 'null':
    #     validator_col_value = 'IS NULL'
    while retries < max_retries:
        result = execute_select_query(table_name, where_conditions={validator_col_identifier: validator_col_value})
        if action:
            action = action.lower()
        if action in ['created', 'updated', None]:
            if len(result['result']) != 0:
                if table_name == 'evpn_service':
                    return
                for res in result['result']:
                    actual_state = res['state'].lower()
                    if actual_state == state.lower():
                        print(result)
                        return
                    else:
                        print(
                            f"Record found but is not in expected state, Expected state: {state}, but got {actual_state}, "
                            f"retrying..")
            else:
                if flag_created == 'is-not':
                    print(f"Requested record not found in {table_name}")
                    return
                print(f"Record not created in {table_name}, Retrying..")
        retries += 1
        time.sleep(retry_delay)
    assert False, 'Request not found or is not in given state'


@step("Fetching {column} from {table}")
def fetch_external_id_from_db(context, column, table):
    retries = 0
    validator_col_identifier, validator_col_value = get_validator_column_name_and_value(table)
    while retries < max_retries:
        result = execute_select_query(table, where_conditions={validator_col_identifier: validator_col_value})
        result = result['result']
        if len(result) != 0:
            for _ in result:
                if column == 'external_id':
                    if '-' in _[column]:
                        print(_[column])
                        common_globals_cs_evpn.external_id = _[column]
                        print(common_globals_cs_evpn.external_id)
                        return
                else:
                    common_globals_cs_evpn.external_id = _[column]
                    return
        retries += 1
        time.sleep(retry_delay)


@step("Reading callback published from l2 in {controller} RMQ")
@step("Validating that callback is published in {state_value} state in {controller} RMQ")
def validate_request_in_rmq(context, state_value: str = None, controller: str = None):
    request_id = common_globals_cs_evpn.requestId
    if controller.lower() == 'evpn':
        RmqAct.ROUTING_KEY = CS.RoutingKeys.READ_FROM_EVPN
    if controller.lower() == 'l2 topology':
        RmqAct.ROUTING_KEY = CS.RoutingKeys.READ_FROM_L2_TOPOLOGY
        request_id = common_globals_cs_evpn.external_id
    retries = 0
    while retries < max_retries:
        queue_data = RmqAct.consume_message()
        print(queue_data)
        if queue_data:
            common_globals_cs_evpn.rmq_msg_callback = check_if_request_exist_by_id_and_status(queue_data, request_id,
                                                                                              state_value)
            if common_globals_cs_evpn.rmq_msg_callback:
                print(common_globals_cs_evpn.rmq_msg_callback)
                return
        print('Request not found, retrying...')
        retries += 1
        time.sleep(retry_delay)
    assert False, 'Request not found or is not in given state'


@step("Publishing {flag} callback fetched from l2 topology queue to EVPN RMQ")
@step("Publishing callback fetched from l2 topology queue to EVPN RMQ")
def prepare_final_callback_and_publish_to_evpn_on_behalf_of_l2(context, flag: str = None):
    l2_callback = common_globals_cs_evpn.rmq_msg_callback
    print(l2_callback)
    final_callback = {}
    final_callback["request-id"] = l2_callback["request-id"]
    if 'fail' not in context.feature.filename:
        final_callback["status"] = "success"
        final_callback["response"] = {}
    else:
        final_callback["status"] = "error"
        final_callback["response"] = {"exception": "Sample error message"}
    if flag:
        if flag.lower() == 'success':
            final_callback["status"] = "success"
            final_callback["response"] = {}
    final_callback["callback-url"] = l2_callback["callback-url"]
    RmqAct.ROUTING_KEY = CS.RoutingKeys.PUBLISH_TO_EVPN
    RmqAct.PAYLOAD_PUBLISH = final_callback
    print(RmqAct.PAYLOAD_PUBLISH)
    RmqAct.publish_message()
    time.sleep(5)


@step("Sending a {action_type} {request_type}")
def publish_to_rmq(context, action_type, request_type):
    payload_prepared = {}
    if action_type.lower() == 'create-dry-run':
        # check if service already exists, if exists then delete it before proceeding
        payload_prepared = CsEvpnPayloadUtil.prepare_create_dry_run_payload()
    elif action_type.lower() == 'create-commit':
        payload_prepared = CsEvpnPayloadUtil.prepare_create_commit_payload()
    elif action_type.lower() == 'delete-service':
        if fetch_and_store_values_from_given_table('evpn_service', check_only_existence=True):
            payload_prepared = CsEvpnPayloadUtil.prepare_delete_payload()
        else:
            if request_type.lower() != 'soft-request':
                assert False, 'There is no such service in EVPN db, exiting'
            return

    elif action_type.lower() == 'validate-resource':
        fn = context.feature.filename
        tc_number = fn.split('/')[-1].split('_')[1]
        payload_prepared = CsEvpnPayloadUtil.prepare_validate_resource_payload(tc_number)
    elif action_type.lower() == 'patch-dry-run':
        payload_prepared = CsEvpnPayloadUtil.prepare_patch_dry_run_payload()
    elif action_type.lower() == 'patch-commit':
        payload_prepared = CsEvpnPayloadUtil.prepare_patch_commit_payload()
    elif action_type.lower() in ['get-service', 'get-all-service', 'get-non-existing-service']:
        payload_prepared = CsEvpnPayloadUtil.prepare_get_service_payload(action_type.lower())

    else:
        assert False, f"Wrong request type: {action_type}"

    execute_payload(payload_prepared)


def execute_payload(payload_prepared):
    common_globals_cs_evpn.requestId = payload_prepared['request-id-generated']
    print(common_globals_cs_evpn.requestId)
    RmqAct.ROUTING_KEY = CS.RoutingKeys.PUBLISH_TO_EVPN
    RmqAct.PAYLOAD_PUBLISH = payload_prepared['payload']
    RmqAct.publish_message()
    print(RmqAct.PAYLOAD_PUBLISH)
    time.sleep(5)


def fetch_and_store_values_from_given_table(table, check_only_existence: bool = False):
    validator_col_identifier, validator_col_value = get_validator_column_name_and_value(table)
    result = execute_select_query(table, where_conditions={validator_col_identifier: validator_col_value})
    if check_only_existence:
        if len(result['result']) > 0:
            return True
        return False
    if not common_globals_cs_evpn.db_result:
        common_globals_cs_evpn.db_result = result
        return [common_globals_cs_evpn.db_result]
    else:
        if common_globals_cs_evpn.db_result != result:
            return [common_globals_cs_evpn.db_result, result]
        else:
            return [common_globals_cs_evpn.db_result]


@step("Fetch interfaces list from table {table} before sending patch request")
def fetch_interface_from_db(context, table):
    fetch_and_store_values_from_given_table(table)


@step("Validating that new interface {flag} added")
def check_if_new_interface_added(context, flag):
    result_list = fetch_and_store_values_from_given_table('interface')
    common_globals_cs_evpn.db_result = {}  # emptying db_result dict
    if len(result_list['result']) == 1:
        if flag.lower() == 'is-not':
            print('No new interface have been added, Update failed')
            return True
        assert False, f"No new interface found, actual result: {result_list}"
    else:
        print("New interface have been added")
        print(f"List of interfaces before patch request: {result_list[0]}")
        print(f"List of interfaces after patch request: {result_list[1]}")
        return True


@step("Validating {request_type} request callback")
def validate_get_service_response(context, request_type):
    # list of services received from the GET request
    list_of_service_received = common_globals_cs_evpn.rmq_msg_callback['response']
    list_of_service_fetched_from_db = execute_select_query('evpn_service')['result']
    if not list_of_service_received:
        number_of_service_received = [{}]
    else:
        number_of_service_received = len(list_of_service_received)
    if number_of_service_received == 1:
        list_of_service_received = [list_of_service_received]

    print(list_of_service_fetched_from_db)
    print(list_of_service_received)
    if request_type == 'get-all-service':

        number_of_service_fetched_from_db = len(list_of_service_fetched_from_db)
        if number_of_service_received == number_of_service_fetched_from_db:
            print(
                f'Services fetched from DB: {number_of_service_fetched_from_db} and Services in response: '
                f'{number_of_service_received} of GET request are equal')
            return True
        else:
            assert False, (f'Services fetched from DB: {number_of_service_fetched_from_db} and Services in response: '
                           f'{number_of_service_received} of GET request are not equal')

    if request_type in ['get-service', 'get-non-existing-service']:
        service_name_to_count = GlobalVar.testParams.get('service_name')
        count_db = sum(1 for item in list_of_service_fetched_from_db if
                       (item.get('evpn-service', {}).get('service-name') or item.get(
                           'service_name')) == service_name_to_count)
        if list_of_service_received is None or len(list_of_service_received) == 0:
            count_response = 0
        else:
            count_response = sum(1 for item in list_of_service_received if
                                 item.get('evpn-service', {}).get('service-name') == service_name_to_count)

        if request_type == 'get-non-existing-service':
            if count_db == 0 and count_response == 0:
                return
            else:
                print("Expected None but got some services")
                assert False, (f"Number of service by {service_name_to_count} name is {count_db} in DB and "
                               f"{count_response} in response callback of GET request")

        if count_response == count_db:
            print(
                f"Number of service by {service_name_to_count} name is {count_db} in DB and "
                f"{count_response} in response callback of GET request")
        else:
            assert False, (f"Number of service by {service_name_to_count} name is {count_db} in DB and "
                           f"{count_response} in response callback of GET request")
