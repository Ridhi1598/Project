Feature: Validate evpn response for delete service request
  This features validates evpn response for successful delete service request

  Scenario: Delete Service request with success response
    Given I read test data for testcase
    When "Publish" "delete" evpn message to "RMQ" "evpn-publish" queue
    Then "Read" and validate that the message is consumed by evpn from "RMQ" "evpn-publish" queue
    When Validate a record is "created" in "evpn_bsaf_request_tracker" table in "postgres" db for "delete"
    Then Validate that the request state is "in progress" for "evpn_bsaf_request_tracker" table
    When Validate a record is "created" in "evpn_external_request_tracker" table in "postgres" db for "delete"
    Then Validate that the request state is "in progress" for "evpn_external_request_tracker" table
    And Wait for expected request processing duration
    Then "Read" and validate that a "delete" "success_callback" response is published in the "RMQ" "orchestrator-callback" queue
    And Validate that "success_callback" response has "status" as "completed"
    When Validate a record is "created" in "evpn_bsaf_request_tracker" table in "postgres" db for "delete"
    Then Validate that the request state is "completed" for "evpn_bsaf_request_tracker" table
    When Validate a record is "created" in "evpn_external_request_tracker" table in "postgres" db for "delete"
    Then Validate "1" entries are found for "evpn_external_request_tracker" table for "create"
    Then Validate that the request state is "completed" for "evpn_external_request_tracker" table
    When Validate a record is "not created" in "evpn_service" table in "postgres" db for "delete"
