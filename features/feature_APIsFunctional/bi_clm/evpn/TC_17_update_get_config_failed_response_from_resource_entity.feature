Feature: Validate evpn response for create service request
  This features validates evpn response for failed create service request

  Scenario: Create Service request with failure response from resource entity
    Given I read test data for testcase
    When "Publish" "update-audit" evpn message to "RMQ" "evpn-publish" queue
    Then "Read" and validate that the message is consumed by evpn from "RMQ" "evpn-publish" queue
    When Validate a record is "created" in "evpn_bsaf_request_tracker" table in "postgres" db for "update-audit"
    Then Validate that the request state is "submitted" for "evpn_bsaf_request_tracker" table
    When Validate a record is "created" in "evpn_external_request_tracker" table in "postgres" db for "update-audit"
    Then Validate that the request state is "in progress" for "evpn_external_request_tracker" table
    And Wait for expected request processing duration
    Then "Read" and validate that a "update-audit" "failed_callback" response is published in the "RMQ" "orchestrator-callback" queue
    And Validate that "failed_callback" response has "status" as "failed"
    When Validate a record is "not created" in "evpn_service" table in "postgres" db for "update-audit"
    When Validate a record is "created" in "evpn_bsaf_request_tracker" table in "postgres" db for "update-audit"
    Then Validate that the request state is "failed" for "evpn_bsaf_request_tracker" table
    When Validate a record is "created" in "evpn_external_request_tracker" table in "postgres" db for "update-audit"
    Then Validate "1" entries are found for "evpn_external_request_tracker" table for "create"
    Then Validate that the request state is "completed" for "evpn_external_request_tracker" table
    When Validate a record is "created" in "evpn_service" table in "postgres" db for "update-audit"
