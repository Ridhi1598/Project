@reject @TC36
Feature: Validate orchestrator response for update service request
  This features validates orchestrator response for failed update service request for invalid values

  Scenario: Create a temporary service record in ES database
    Given I read test data for testcase
    When I send request to "create" the "request" record in "ES" database
    When I send request to "create" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "created" in orchestrator "ES" records
    When I send request to "create" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records

  Scenario: Update Service request with failure response from evpn controller for invalid values
    When "Publish" "update" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then I "read" and validate that a "request" record is "not created" in orchestrator "ES" records
    Then "Read" and validate that a "update" "exception_callback" message is published in the "RMQ" "orchestrator-callback" queue

  Scenario: Delete the created service record from ES database
    When I send request to "delete" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "deleted" in orchestrator "ES" records
    When I send request to "delete" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "deleted" in orchestrator "ES" records