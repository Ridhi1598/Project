@tc24 @bngController
Feature: Commit patch l3vpn dry run request - Success
  This feature validates that functionality related to commit the patch l3vpn dry run request - success

   Scenario Outline: tc_20 : This scenario validate that the functionality related to patch l3vpn service - success
    Given I read test data for BNG controller testcases
    When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "pending confirmation" state
    When I validate that the request record should "exist" in the table "bng_external_request_tracker" by "parent_request_tracker_id"
    Then I validate the "parent_request_tracker_id" from "bng_external_request_tracker" for patch_l3vpn_service
    Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG

    Examples:
     |tc_num  | published                       |  bng_to_portal                      |
     |tc_20   | _patch_l3vpn_service_success    | _patch_l3vpn_bng_to_portal_success  |


   Scenario Outline: tc_24 : This Scenario validates that functionality related to commit the patch l3vpn dry run request - success
     Given I read the testdata for commit the patch l3vpn dry run request
     When "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
     Then Get and verify the "created" request record by "id" from table "bng_bsaf_request_tracker" with "completed" state
#     When I wait for "20" seconds to update the parent request record
     Then I validate that the request record should "exist" in the table "bng_external_request_tracker" by "parent_request_tracker_id"
     When I validate that all the requests state should be "completed" from "bng_external_request_tracker" for commit patch L3VPN dry run request
     Then Get and verify the "committed" request record by "id" from table "bng_bsaf_request_tracker" with "committed" state
     Then "Read" and validate that the "baseRequestId" "<tc_num><bng_to_portal>" message is published in the "RMQ" "orchestrator_test" queue for BNG
     Then I validate that the request record should "exist" in the table "pw_port" by "bng_name"
     Then I validate that the request record should "exist" in the table "vpn_network_access" by "id"

    Examples:
     |tc_num  | published                                   | bng_to_portal                                            |
     |tc_24   | _commit_patch_l3vpn_dry_run_request_success |_commit_patch_l3vpn_dry_run_request_bng_to_portal_success |


#"""Need to check two things that vpn network accesses for the following three ids: EDTNABTFOT39, EDTNABTFOT39-FIXED EDTNABTFOT39-DV are created in the database  check table vpn_network_accesss
#   and need to check if pw ports was created in the table :need to found two entries one for bng 1 and the other for bng 2 that containes the pq port number 300 checkk table pw_port table"""