
import time

from behave import step

from common.util.common_util import common_globals_clm_l2vpn, PayloadUtil
from common.util.es import EsUtilsL3
from common.util.rmqv2 import BiClM, RmqActions
from common.util.rmqv2 import RmqActions,  BiClM

BiClmL2vpnPayloadUtil = PayloadUtil.BiClm.L2VPN()
RmqAct = RmqActions()
RmqAct.EXCHANGE = BiClM.EXCHANGE
RmqAct.BASE_URL = BiClM.API_BASE_URL
RmqAct.ROUTING_KEY = BiClM.RoutingKeys.READ_FROM_L2VPN
print(RmqAct.EXCHANGE)
print(RmqAct.ROUTING_KEY)

ES = EsUtilsL3()


@step("Sending {action_type} to l2vpn controller")
def publish_to_rmq(context, action_type):
    payload_prepared = {}
    if action_type.lower() == "create-l2vpn-service":
        payload_prepared = BiClmL2vpnPayloadUtil.prepare_create_payload()

    else:
        assert False, f"Wrong request type: {action_type}"
    print(payload_prepared)
    execute_payload(payload_prepared)


def execute_payload(payload_prepared):
    common_globals_clm_l2vpn.requestId = payload_prepared['request-id-generated']
    print(common_globals_clm_l2vpn.requestId)
    RmqAct.ROUTING_KEY = BiClM.RoutingKeys.PUBLISH_TO_L2VPN
    RmqAct.PAYLOAD_PUBLISH = payload_prepared['payload']
    RmqAct.publish_message()
    print(RmqAct.PAYLOAD_PUBLISH)
    time.sleep(5)


