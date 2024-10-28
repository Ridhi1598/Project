Feature: Validate evpn response for create service request
  This features validates evpn response for successful create service request

  Scenario: Create Service request with success response
    Given I read test data for testcase
    When Validate a record is "created" in "qos_service_bi_clm" table in "postgres" db for "update"
    Then Read the input and output value for "bandwidth" in "qos_service_bi_clm" table for "before"
    When "Publish" "update" evpn message to "RMQ" "evpn-publish" queue
    Then "Read" and validate that the message is consumed by evpn from "RMQ" "evpn-publish" queue
    When Validate a record is "created" in "evpn_bsaf_request_tracker" table in "postgres" db for "update"
    Then Validate that the request state is "submitted" for "evpn_bsaf_request_tracker" table
    When Validate a record is "created" in "evpn_external_request_tracker" table in "postgres" db for "update"
    Then Validate that the request state is "in progress" for "evpn_external_request_tracker" table
    And Wait for expected request processing duration
    Then "Read" and validate that a "update" "success_callback" response is published in the "RMQ" "orchestrator-callback" queue
    And Validate that "success_callback" response has "status" as "completed"
    When Validate a record is "created" in "evpn_bsaf_request_tracker" table in "postgres" db for "update"
    Then Validate that the request state is "completed" for "evpn_bsaf_request_tracker" table
    When Validate a record is "created" in "evpn_external_request_tracker" table in "postgres" db for "update"
    Then Validate "3" entries are found for "evpn_external_request_tracker" table for "create"
    Then Validate that the request state is "completed" for "evpn_external_request_tracker" table
    When Validate a record is "created" in "evpn_service" table in "postgres" db for "update"
    When Validate a record is "created" in "qos_service_bi_clm" table in "postgres" db for "update"
    Then Read the input and output value for "bandwidth" in "qos_service_bi_clm" table for "after"
    Then Validate that the "before" and "after" values for "bandwidth" are "updated"