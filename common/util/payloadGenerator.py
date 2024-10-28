import os
import sys
import json
import uuid


class payloadGenerator:
    def __init__(self):
        print("initialized")

    def generate_reqId(self):
        reqId = uuid.uuid4()
        return str(reqId)

    def load_payload_message(self, component, fileName):
        filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + '/resources/payload/' + \
                   sys.argv[1] + '/' + component.lower() + '/' + fileName

        with open(filePath) as messageFile:
            data = json.load(messageFile)
            return data

    def load_schema_message(self, component, fileName):
        filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + '/resources/schema/' + \
                   sys.argv[1] + '/' + component.lower() + '/' + fileName

        with open(filePath) as messageFile:
            data = json.load(messageFile)
            return data

    def update_payload_message(self, payload, testParams):
        # update service Id
        global expectedValue
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-network-resource-id"] = testParams["serviceId"]
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-service-id"] = testParams["serviceId"]
        payload["supportingService"][0]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-service-id"] = testParams["serviceId"]
        payload["supportingService"][1]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-service-id"] = testParams["serviceId"]

        if payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["management"] == "provider-managed":
            expectedValue = "telus-pe-ce-network-accesses"
        elif payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["management"] == "customer-managed":
            expectedValue = "site-network-accesses"

        # update base device details
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"][expectedValue]["site-network-access"][0]["telus-pe-device-reference"] = testParams["primary"]
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-pe-devices"]["pe-device"][0]["pe-device-id"] = testParams["primary"]

        # update supporting device details
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"][expectedValue]["site-network-access"][1]["telus-pe-device-reference"] = testParams["secondary"]
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-pe-devices"]["pe-device"][1]["pe-device-id"] = testParams["secondary"]

        # update interface type
        payload["supportingService"][0]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["site-network-accesses"]["site-network-access"][0]["bearer"]["telus-tp-info"]["telus-interface-type"] = testParams["interface"]
        payload["supportingService"][0]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["site-network-accesses"]["site-network-access"][1]["bearer"]["telus-tp-info"]["telus-interface-type"] = testParams["interface"]
        payload["supportingService"][1]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["site-network-accesses"]["site-network-access"][0]["bearer"]["telus-tp-info"]["telus-interface-type"] = testParams["interface"]
        payload["supportingService"][1]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["site-network-accesses"]["site-network-access"][1]["bearer"]["telus-tp-info"]["telus-interface-type"] = testParams["interface"]

        # update interface details
        interface = testParams["interface"]
        payload["supportingService"][0]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["site-network-accesses"]["site-network-access"][0]["bearer"]["telus-tp-info"]["telus-interface"] = testParams[interface]
        payload["supportingService"][0]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["site-network-accesses"]["site-network-access"][1]["bearer"]["telus-tp-info"]["telus-interface"] = testParams[interface]
        payload["supportingService"][1]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["site-network-accesses"]["site-network-access"][0]["bearer"]["telus-tp-info"]["telus-interface"] = testParams[interface]
        payload["supportingService"][1]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["site-network-accesses"]["site-network-access"][1]["bearer"]["telus-tp-info"]["telus-interface"] = testParams[interface]

        # update user details
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-info"]["cust-id"] = int(testParams["custId"])
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-info"]["cust-shortname"] = testParams["custShortName"]
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-info"]["cust-descr"] = testParams["custDesc"]
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-info"]["cust-email-address"] = testParams["custEmail"]

        return payload

    def update_serviceId(self, payload, testParams):
        # update service Id
        if "mwr" in testParams.get("EndPoint"):
            payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-network-resource-id"] = testParams["mwrId"]
            payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-service-id"] = testParams["mwrId"]
        else:
            payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-network-resource-id"] = testParams["serviceId"]
            payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-service-id"] = testParams["serviceId"]
            payload["supportingService"][0]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-service-id"] = testParams["serviceId"]
            payload["supportingService"][1]["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-service-id"] = testParams["serviceId"]
        return payload

    def update_mwr_payload_message(self, payload, testParams):
        # update service Id
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-network-resource-id"] = testParams["serviceId"]
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-service-id"] = testParams["serviceId"]

        global expectedValue
        if payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["management"] == "provider-managed":
            expectedValue = "telus-pe-ce-network-accesses"
        elif payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["management"] == "customer-managed":
            expectedValue = "site-network-accesses"

        # update base device details
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"][expectedValue]["site-network-access"][0]["telus-pe-device-reference"] = testParams["mwr"]
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-pe-devices"]["pe-device"][0]["pe-device-id"] = testParams["mwr"]

        # update user details
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-info"]["cust-id"] = int(testParams["custId"])
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-info"]["cust-shortname"] = testParams["custShortName"]
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-info"]["cust-descr"] = testParams["custDesc"]
        payload["serviceCharacteristic"][0]["value"]["telus-network-resource"]["telus-cust-info"]["cust-email-address"] = testParams["custEmail"]

        return payload