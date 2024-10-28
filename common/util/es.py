import requests
import json


class EsUtilsL3:
    base_url: str = "https://bi-elasticsearch.qa.app01.toll6.tinaa.tlabs.ca"
    CLM_L3_REQUESTS_EP = "/clm-l3vpn-controller-requests"
    CLM_L3_SERVICES_EP = "/clm-l3vpn-controller-services"

    CLM_L3_REQUESTS_SEARCH_EP = f"{CLM_L3_REQUESTS_EP}/_search"
    CLM_L3_SERVICES_SEARCH_EP = f"{CLM_L3_SERVICES_EP}/_search"  # vpn-node-id EDTNABTFSE52-CLGRAB21-TST0040-1234740
    CLM_L3_SERVICES_ADD_EP = f"{CLM_L3_SERVICES_EP}/_doc"
    SEARCH_STR: str = None

    headers = {
        'Authorization': 'Basic ZWxhc3RpYzplbGFzdGlj',
        'Content-Type': 'application/json'
    }

    def __init__(self):
        pass

    def gen_payload_for_get(self):
        if not self.SEARCH_STR:
            return "search id not provided"
        payload = json.dumps({
            "query": {
                "match": {
                    "_id": self.SEARCH_STR
                }
            }
        })
        return payload

    # def gen_payload_for_post(self):

    def send_request(self, url, method, payload=None, match_all=False):
        if not payload and not match_all:
            payload = self.gen_payload_for_get()
        if match_all:
            payload = json.dumps({
                "query": {
                    "match_all": {}
                }
            })
        response = requests.request(method, url, headers=self.headers, data=payload, verify=False)
        return response.json()

    def query_request_index(self):
        return self.send_request(self.base_url + self.CLM_L3_REQUESTS_SEARCH_EP, "GET")

    def query_service_index(self):
        return self.send_request(self.base_url + self.CLM_L3_SERVICES_SEARCH_EP, "GET")

    def query_service_index_match_all(self):
        return self.send_request(self.base_url + self.CLM_L3_SERVICES_SEARCH_EP, "GET", match_all=True)

    # def update_es_record(self,index_name, doc_id):
    #     # post
    #     url = "https://bi-elasticsearch.develop.app01.toll6.tinaa.tlabs.ca/{indexName}/_doc/{docId}/_update"
    #     body =  {
    #       "doc" : {
    #         "key": "value"
    #       }
    #     }
    #
    def create_es_service(self, doc_id, payload):
        return self.send_request(f"{self.base_url}{self.CLM_L3_SERVICES_ADD_EP}/{doc_id}", "POST", payload)

    #
    def delete_es_record(self, service_id):
        return self.send_request(f'{self.base_url}{self.CLM_L3_SERVICES_EP}/_doc/{service_id}', "DELETE",
                                 payload=False)
