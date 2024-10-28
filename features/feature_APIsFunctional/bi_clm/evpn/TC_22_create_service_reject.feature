Feature: Validate evpn response for create service request
  This features validates evpn response for successful create service request

  Scenario: Create Service request with reject response
    Given I read test data for testcase
    When "Publish" "create" evpn message to "RMQ" "evpn-publish" queue
    Then "Read" and validate that the message is consumed by evpn from "RMQ" "evpn-publish" queue
    And Wait for expected request processing duration
    Then "Read" and validate that a "create" "failed_callback" response is published in the "RMQ" "orchestrator-callback" queue
    And Validate that "failed_callback" response has "status" as "failed"