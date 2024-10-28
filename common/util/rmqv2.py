import json

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BiClM:
    EXCHANGE: str = "com.telus.tinaa.bsaf.clm.bi"
    API_BASE_URL: str = "https://bi-rabbitmq.qa.app01.toll6.tinaa.tlabs.ca/api"

    class RoutingKeys:
        L3VPN: str = None
        PUBLISH_TO_L2VPN: str = "com.telus.tinaa.bsaf.clm.bi.orchestrator.l2vpn.controller.request"
        READ_FROM_L2VPN: str = "tinaa-orch-callbacks-tests"


class CS:
    EXCHANGE: str = "consumer_rabbit_exchange"
    API_BASE_URL: str = "https://consumer-rabbitmq.qa.app01.toll6.tinaa.tlabs.ca/api"

    class RoutingKeys:
        PUBLISH_TO_EVPN: str = 'evpn_svc_controller_queue'
        READ_FROM_EVPN: str = 'cs_orchestrator_queue_test'
        READ_FROM_L2_TOPOLOGY: str = 'l2_topology_engine_queue_test'


class RmqActions:
    def __int__(self):
        pass

    EXCHANGE: str = None
    ROUTING_KEY: str = None
    BASE_URL: str = None
    QUEUE_NAME: str = None
    PAYLOAD_PUBLISH: dict = {}
    TINAA_TEST_CALLBACKS: str = "tinaa-callbacks-tests"
    TINAA_TEST_REQUESTS: str = "tinaa-requests-tests"

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

    def publish_message(self):
        http_url = f'{self.BASE_URL}/exchanges/%2F/{self.EXCHANGE}/publish'
        self.__send_request(url=http_url, r_type='publish', payload_publish={"tests-tinaa": "tests"})

    def consume_message(self):
        http_url = f'{self.BASE_URL}/queues/%2F/{self.ROUTING_KEY}/get'
        response = self.__send_request(url=http_url, r_type='consume')
        if response:
            return response
        else:
            return False
