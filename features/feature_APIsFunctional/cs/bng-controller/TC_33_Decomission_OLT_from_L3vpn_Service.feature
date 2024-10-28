@tc33 @bngController
Feature: Decommission OLT from l3vpn service
  This feature validates Decommission OLT request 

   Scenario Outline: tc_33 : Decommission OLT from L3vpn
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "in progress" state
    Then Wait for "30" seconds
    Then I validate that the request record should "exist" in the table "bng_external_request_tracker" by "parent_request_tracker_id"
    When Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
    When I validate that all the requests state should be "completed" from "bng_external_request_tracker" for commit patch L3VPN dry run request
    Then Wait for "15" seconds
    When I validate that the request record should "not exist" in the table "pw_port" by "bng_name"
    Then I validate that the request record should "non-exist" in the table "vpn_network_access" by "id"
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_orchestrator>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num | published                    |  bng_to_orchestrator                           |
     |tc_33   | _decommission_OLT_success   |  _decommission_OLT_bng_to_orchestrator_success |


