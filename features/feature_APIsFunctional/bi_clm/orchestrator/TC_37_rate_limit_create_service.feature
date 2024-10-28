@rateLimit @TC37
Feature: Validate orchestrator response for rate limit request
  This features validates orchestrator response for rejected create service request

  Scenario: Create a temporary csid record in ES database
    Given I read test data for testcase
    When I send request to "create" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    When I send request to "update" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "true"

  Scenario: Create Service request which is rejected by orchestrator
    When "Publish" "create" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
#    Then "Read" and validate that a "create" "in-process_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then "Read" and validate that a "create" "exception_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then I "read" and validate that a "service" record is "not created" in orchestrator "ES" records

  Scenario: Delete the created csid record from ES database
    When I send request to "delete" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "deleted" in orchestrator "ES" records