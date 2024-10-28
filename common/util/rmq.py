import json
from typing import List

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ies unique
class Exchanges:
    BI_CLM: str = "com.telus.tinaa.bsaf.clm.bi"


class Components:
    ORCH: str = 'orchestrator'
    ING: str = 'ingestion'


class RmqActions:
    def __int__(self):
        pass

    EXCHANGE: str = Exchanges.BI_CLM
    COMPONENT: str = Components.ORCH
    ROUTING_KEY: str = None
    QUEUE_NAME: str = None
    PAYLOAD_PUBLISH: dict = {}
    TINAA_TEST_CALLBACKS: str = "tinaa-callbacks-tests"
    TINAA_TEST_REQUESTS: str = "tinaa-requests-tests"

    base_url: str = "https://bi-rabbitmq.qa.app01.toll6.tinaa.tlabs.ca/api"
    bool_ack_requeue: bool = "ack_requeue_true"  # false will delete the message
    get_result_count: int = 4000

    payload_consume: dict = json.dumps({
        "count": get_result_count,
        "ackmode": bool_ack_requeue,
        "encoding": "auto",
        "truncate": 50000
    })
    headers = {
        'Authorization': 'Basic Z3Vlc3Q6Z3Vlc3Q=',
        'Content-Type': 'application/json'
    }


    def __send_request(self, url: str = None, r_type: str = None, payload_publish: dict = {}):
        try:
            final_publish_payload = None
            if r_type == 'publish':
                sub_payload_json = json.dumps(self.PAYLOAD_PUBLISH)
                actual_publish_payload = {
                    "properties": {
                        "delivery_mode": 1,
                        "headers": {}
                    },
                    "routing_key": self.ROUTING_KEY,
                    "payload": sub_payload_json,
                    "payload_encoding": "string"
                }
                final_publish_payload = json.dumps(actual_publish_payload)
            payload = self.payload_consume if r_type == 'consume' else final_publish_payload
            response = requests.post(url, headers=self.headers, data=payload, verify=False)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error while making request to {url}: {e}")
            return None

    def __publish_message(self):
        http_url = f'{self.base_url}/exchanges/%2F/{self.EXCHANGE}/publish'
        self.__send_request(url=http_url, r_type='publish', payload_publish={"tests-tinaa": "tests"})

    def __consume_message(self):
        http_url = f'{self.base_url}/queues/%2F/{self.QUEUE_NAME}/get'
        response = self.__send_request(url=http_url, r_type='consume')
        if response:
            return response
        else:
            assert False

    def orch_req_publish(self):
        self.ROUTING_KEY = f'{self.EXCHANGE}.{self.COMPONENT}.request'
        self.__publish_message()

    # below method will be modified, method name are correct
    def orch_req_get(self):
        self.QUEUE_NAME = f'{self.EXCHANGE}.{self.COMPONENT}.request'
        self.__consume_message()

    #
    def orch_res_publish(self):
        self.ROUTING_KEY = f'{self.EXCHANGE}.{self.COMPONENT}.response'
        self.__publish_message()

    #
    def orch_res_get(self):
        self.QUEUE_NAME = f'{self.EXCHANGE}.{self.COMPONENT}.response'
        self.__consume_message()

    def orch_res_test_cb_get(self):
        self.QUEUE_NAME = 'tinaa-orch-callbacks-tests'

        return self.__consume_message()


    def tinaa_tests_cb_publish(self):
        self.ROUTING_KEY = "com.telus.tinaa.bsaf.clm.bi.ingestion.response"
        self.__publish_message()

    def tinaa_tests_cb_get(self):
        self.QUEUE_NAME = self.TINAA_TEST_CALLBACKS
        self.__consume_message()
