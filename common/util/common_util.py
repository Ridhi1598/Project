import json
import os
import uuid
from typing import Dict

from features.steps.globalVar import GlobalVar


def get_json_as_dict(path: str):
    with open(path) as f:
        data = json.load(f)
    return data


request_type_list = ['create-dry-run', 'create-commit', 'patch-dry-run', 'patch-commit', 'delete', 'validate',
                     'get-service', 'create-l2vpn-service']
request_type_list_2 = ['create_dry_run', 'create_commit', 'patch', 'delete', 'validate']


class CommonMethods:
    request_id: str = None

    @staticmethod
    def detect_payload_operation_type(request_list, file_path_str):
        return [operation_type for operation_type in request_list if
                operation_type.lower() in file_path_str.lower()][0]

    @staticmethod
    def create_request_id():
        CommonMethods.request_id = str(uuid.uuid4())
        return CommonMethods.request_id

    @staticmethod
    def get_project_root():
        current_dir = os.path.abspath(os.path.dirname(__file__))
        while True:
            if os.path.isfile(os.path.join(current_dir, 'Test_Runner.py')):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:  # Reached the top of the filesystem tree
                raise Exception("Project root not found. Make sure 'settings.py' exists in your project.")
            current_dir = parent_dir

    @staticmethod
    def __inject_for_create_dry_run(payload_data):
        payload_data['payload']['service-name'] = GlobalVar.testParams.get('service_name')
        return payload_data

    @staticmethod
    def __inject_for_create_service_l2vpn(payload_data):
        # vpn-node-name
        payload_data['request-characteristics']['payload']['vpn-service'][0]['vpn-nodes']['vpn-node'][0][
            'vpn-node-id'] = f"{GlobalVar.testParams.get('service_name')}-{GlobalVar.testParams.get('node_service_id')}"

        # ne-id
        payload_data['request-characteristics']['payload']['vpn-service'][0]['vpn-nodes']['vpn-node'][0][
            'ne-id'] = GlobalVar.testParams.get('service_name')

        # node-service-id
        payload_data['request-characteristics']['payload']['vpn-service'][0]['vpn-nodes']['vpn-node'][0]['tinaa-l2vpn-ntw-augment:telus-node-info'][
            'node-service-id'] = GlobalVar.testParams.get(
            'node_service_id')

        payload_url_qry_param = payload_data['request-characteristics']['url-query-parameters']
        for i in range(len(payload_url_qry_param)):
            if payload_url_qry_param[i]['name'] == 'audit':
                payload_url_qry_param[i]['value'] = GlobalVar.testParams.get('audit_flag').lower()
        payload_data['request-characteristics']['url-query-parameters'] = payload_url_qry_param
        return payload_data

    @staticmethod
    def __inject_for_common_commit(payload_data):
        payload_data['path'] = f'/request/request-id={CommonMethods.request_id}'
        return payload_data

    @staticmethod
    def __inject_for_delete(payload_data):
        payload_data['path'] = f'/evpn-services/evpn-service={GlobalVar.testParams.get("service_name")}'
        return payload_data

    @staticmethod
    def __inject_for_validate(payload_data):
        return payload_data

    @staticmethod
    def __inject_for_patch_dry_run(payload_data):
        payload_data[
            'path'] = f'/evpn-service={GlobalVar.testParams.get("service_name")}/evpn-instances/evpn-instance=CMCS_MCAST_L2/interface'
        return payload_data

    @staticmethod
    def __inject_for_get_service(payload_data, request_type):
        if request_type in ['get-service', 'get-non-existing-service']:
            payload_data['path'] = f'evpn-services/evpn-service={GlobalVar.testParams.get("service_name")}'
        return payload_data

    @staticmethod
    def inject_to_payload(specified_json_path, type_request=None):
        #
        payload = get_json_as_dict(specified_json_path)
        request_id = CommonMethods.create_request_id()
        if 'request-id' in payload:
            req_id_key = 'request-id'
            payload['request-id'] = request_id
        else:
            req_id_key = 'id'
            payload['id'] = request_id
        print(request_id)
        final_payload: Dict = {}
        inject_for = CommonMethods().detect_payload_operation_type(request_list=request_type_list,
                                                                   file_path_str=specified_json_path)
        if inject_for == 'create-l2vpn-service':
            final_payload = CommonMethods.__inject_for_create_service_l2vpn(payload)

        if inject_for == 'create-dry-run':
            final_payload = CommonMethods.__inject_for_create_dry_run(payload)

        if inject_for == 'create-commit':
            final_payload = CommonMethods.__inject_for_common_commit(payload)

        if inject_for == 'delete':
            final_payload = CommonMethods.__inject_for_delete(payload)

        if inject_for == 'validate':
            final_payload = CommonMethods.__inject_for_validate(payload)

        if inject_for == 'patch-dry-run':
            final_payload = CommonMethods.__inject_for_patch_dry_run(payload)

        if inject_for == 'patch-commit':
            final_payload = CommonMethods.__inject_for_common_commit(payload)

        if inject_for == 'get-service':
            final_payload = CommonMethods.__inject_for_get_service(payload, type_request)

        return {'request-id-generated': final_payload[req_id_key], 'payload': final_payload}


# create, commit, patch, delete, validate
class PayloadUtil:
    def prepare_payload(self, feature_name, app_name):
        feature_name_list = feature_name.split('/')
        comp_name = feature_name_list[3].lower()  # evpn, bng etc
        inject_for = CommonMethods().detect_payload_operation_type(request_list=request_type_list_2,
                                                                   file_path_str=feature_name)
        json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", app_name.lower(),
                                         comp_name, f"{inject_for}.json")
        return CommonMethods.inject_to_payload(json_payload_path)

    class CS:
        class EVPN:
            @staticmethod
            def prepare_create_dry_run_payload():
                json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", "cs",
                                                 "evpn", "create-dry-run.json")
                return CommonMethods.inject_to_payload(json_payload_path)

            @staticmethod
            def prepare_create_service_payload():
                json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", "cs",
                                                 "evpn", "create-dry-run.json")
                return CommonMethods.inject_to_payload(json_payload_path)

            def prepare_create_commit_payload(self):
                json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", "cs",
                                                 "evpn", "create-commit.json")
                return CommonMethods.inject_to_payload(json_payload_path)

            def prepare_delete_payload(self):
                json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", "cs",
                                                 "evpn", "delete.json")
                return CommonMethods.inject_to_payload(json_payload_path)

            def prepare_validate_resource_payload(self, tc_number):
                json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", "cs",
                                                 "evpn", f"validate_{tc_number}.json")
                return CommonMethods.inject_to_payload(json_payload_path)

            def prepare_patch_dry_run_payload(self):
                json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", "cs",
                                                 "evpn", "patch-dry-run.json")
                return CommonMethods.inject_to_payload(json_payload_path)

            def prepare_patch_commit_payload(self):
                json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", "cs",
                                                 "evpn", "patch-commit.json")
                return CommonMethods.inject_to_payload(json_payload_path)

            def prepare_get_service_payload(self, type_request):
                json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", "cs",
                                                 "evpn", "get-service.json")
                return CommonMethods.inject_to_payload(json_payload_path, type_request)

    class BiClm:
        class L3VPN:
            pass

        class L2VPN:
            @staticmethod
            def prepare_create_payload():
                json_payload_path = os.path.join(CommonMethods.get_project_root(), "resources", "payload", "bi_clm", "l2vpn", "create-l2vpn-service.json")
                return CommonMethods.inject_to_payload(json_payload_path)


class CommonGlobals():
    requestId: str = None
    rmq_msg_callback: dict = {}
    es_service_rec_response: dict = {}
    es_request_rec_response: dict = {}
    external_id: str = None
    db_result: dict = {}


common_globals_cs_evpn = CommonGlobals()
common_globals_cs_orch = CommonGlobals()
common_globals_clm_l2vpn = CommonGlobals()
