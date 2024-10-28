@reject @TC34
Feature: Validate orchestrator response for delete service request
  This features validates orchestrator response for delete invalid service request

  Scenario: Update Service request which gets rejected
    Given I read test data for testcase
    When "Publish" "delete" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then I "read" and validate that a "csid" record is "not created" in orchestrator "ES" records
    Then I "read" and validate that a "service" record is "not created" in orchestrator "ES" records
    Then "Read" and validate that a "delete" "exception_callback" message is published in the "RMQ" "orchestrator-callback" queue
