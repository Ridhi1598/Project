@update @TC7
Feature: Validate orchestrator response for update service request
  This features validates orchestrator response for failed update service request

  Scenario: Create a temporary service record in ES database
    Given I read test data for testcase
    When I send request to "create" the "request" record in "ES" database
    When I send request to "create" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "created" in orchestrator "ES" records
    And Read the "before" values for associated "prefix" values
    And Read the "before" values for associated "speed" values
    When I send request to "create" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records

  Scenario: Update Service request with failure response from evpn controller for primary evpn profile
    When "Publish" "update" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then I "read" and validate that a "request" record is "created" in orchestrator "ES" records
    And I validate that "request" record "state" value is "pending"
    Then "Read" and validate that a "update" "in-process_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then "Read" and validate that a "update" "secondary_evpn_profile" message is published in the "RMQ" "evpn-publish" queue
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "true"
    When "Publish" "evpn-update-success-callback" response to "RMQ" "evpn-callback" queue for "secondary_evpn_profile"
    Then "Read" and validate that a "update" "primary_evpn_profile" message is published in the "RMQ" "evpn-publish" queue
    When "Publish" "evpn-update-failed-callback" response to "RMQ" "evpn-callback" queue for "primary_evpn_profile"
    Then I "read" and validate that a "service" record is "created" in orchestrator "ES" records
    And Read the "after" values for associated "prefix" values
    And Read the "after" values for associated "speed" values
    Then Validate that the "before" and "after" values for "prefix" is "same"
    Then Validate that the "before" and "after" values for "speed" is "same"
    Then I "read" and validate that a "request" record is "created" in orchestrator "ES" records
    And I validate that "request" record "state" value is "failed"
    Then "Read" and validate that a "update" "failed_evpn_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then "Read" and validate that a "rollback-evpn" "secondary_evpn_profile" message is published in the "RMQ" "evpn-publish" queue
    When "Publish" "evpn-update-success-callback" response to "RMQ" "evpn-callback" queue for "secondary_evpn_profile"
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "false"

  Scenario: Delete the created service record from ES database
    When I send request to "delete" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "deleted" in orchestrator "ES" records
    When I send request to "delete" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "deleted" in orchestrator "ES" records