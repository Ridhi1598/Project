@reject @TC35
Feature: Validate orchestrator response for create service request
  This features validates orchestrator response for rejected create service request

  Scenario: Create service request which is rejected
    Given I read test data for testcase
    When I send request to "create" the "csid" record in "ES" database
    When I send request to "update" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "true"
    When "Publish" "create" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that a "create" "exception_callback" message is published in the "RMQ" "orchestrator-callback" queue
    When I send request to "delete" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "deleted" in orchestrator "ES" records