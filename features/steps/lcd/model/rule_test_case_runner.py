import time
import json
import requests
import os
import logging

from features.steps.lcd.model.mediation_layer_nso_context import NSOAction
class FunctionalRuleTestRunner(NSOAction):
    
    def __init__(self, context: NSOAction):
        super().__init__(context)
        self.session_uuid = None

    def open(self):
        self._create_testing_session()
        return self

    def close(self):
        if self.session_uuid:
            self._destroy_testing_session()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        pass

    def _create_testing_session(self):
        params = {
            "params": {
                "path": "/lcdcpe-testing-framework:action/create-testing-session",
            }
        }

        response = self.request(params)
        if response['lock-status'] == "false":
            raise RuntimeError("There is a session that is already taking place.")

        self.session_uuid = response['session-uuid']


    def _destroy_testing_session(self):
        params = {
            "params": {
                "path": "/lcdcpe-testing-framework:action/destroy-testing-session",
                "params": {
                    "session-uuid": self.session_uuid,
                }
            }
        }
        
        response = self.request(params)
        if response['result'] == "false":
            raise RuntimeError("Cannot close invalid session")

    def add_device(self, device_inventory, device_model):
        params = {
            "params": {
                "path": "/lcdcpe-testing-framework:action/add-device",
                "params": {
                    "session-uuid": self.session_uuid,
                    "device-inventory": device_inventory,
                    "device-model": device_model,
                }
            }
        }

        response = self.request(params)

        if response != True:
            raise ValueError("Failure to add device")
        

    def delete_device(self, device_inventory, device_model):
        params = {
            "params": {
                "path": "/lcdcpe-testing-framework:action/delete-device",
                "params": {
                    "session-uuid": self.session_uuid,
                    "device-inventory": device_inventory,
                    "device-model": device_model,
                }
            }
        }

        response = self.request(params)

        if response != True:
            raise ValueError("Failure to add device")
        
    def prepare_test(self, inventory, device_model, test_info):
        params = {
            "params": {
                "path": "/lcdcpe-testing-framework:action/prepare-test",
                "params": {
                    "session-uuid": self.session_uuid,
                    "device-model": device_model,
                    "device-inventory": inventory,
                    "test-info": test_info
                }
            }
        }

        response = self.request(params)
        return response['uuid']


    def poll_test_status(self, test_uuid):
        running = True
        output = None
        while running:
            output = self.check_test_status(test_uuid)
            running = output['test-status'] != 'Done'
            time.sleep(1)
            
        return output

    def check_test_status(self, test_uuid):
        try:
            params = {
                "params": {
                    "path": "/lcdcpe-testing-framework:action/check-test-status",
                    "params": {
                        "session-uuid": self.session_uuid,
                        "uuid": test_uuid,
                    }
                }
            }

            response = self.request(params)
            return response

        except Exception as e:
            self.stop_and_delete_test(test_uuid)
            raise e

    def stop_and_delete_test(self, process_id):
        params = {
            "params": {
                "path": "/lcdcpe-testing-framework:action/stop-and-delete-test",
                "params": {
                    "session-uuid": self.session_uuid,
                    "process-id": process_id,
                }
            }
        }

        response = self.request(params)


    def stop_and_delete_all_tests(self,):
        params = {
            "params": {
                "path": "/lcdcpe-testing-framework:action/stop-and-delete-all-tests",
            }
        }

        response = self.request(params)
        logging.debug(response['success'])
        if response['success'] != "true":
            raise NotImplementedError("Could not stop and delete all tests")



    def request_test(self, device_model, inventory, test_info):
        raise NotImplementedError("This methid is deprecated")
        params = {
            "params": {
                "path": "/lcdcpe-testing-framework:action/runtest",
                "params": {
                        "device-model": device_model,
                        "inventory": inventory,
                        "test-info": test_info
                }
            }
        }
        return self.request(params)

