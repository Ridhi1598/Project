@delete @TC13
Feature: Validate orchestrator response for delete service request
  This features validates orchestrator response for failed delete service request

  Background: Read test data
    Given I read test data for testcase

  Scenario: Create a temporary service record in ES database
    When I send request to "create" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "created" in orchestrator "ES" records
    And Read the "before" values for associated "prefix" values
    And Read the "before" values for associated "speed" values
    When I send request to "create" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records

  Scenario: Delete Service request with failure response from l3vpn controller for secondary node
    When "Publish" "delete" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then I "read" and validate that a "request" record is "created" in orchestrator "ES" records
    And I validate that "request" record "state" value is "submitted"
    Then "Read" and validate that a "delete" "in-process_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then "Read" and validate that a "delete" "secondary_evpn_profile" message is published in the "RMQ" "evpn-publish" queue
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "true"
    When "Publish" "evpn-delete-success-callback" response to "RMQ" "evpn-callback" queue for "secondary_evpn_profile"
    Then "Read" and validate that a "delete" "primary_evpn_profile" message is published in the "RMQ" "evpn-publish" queue
    When "Publish" "evpn-delete-success-callback" response to "RMQ" "evpn-callback" queue for "primary_evpn_profile"
    Then "Read" and validate that a "delete" "secondary_l3vpn_node" message is published in the "RMQ" "l3vpn-publish" queue
    When "Publish" "l3vpn-in-process-callback" response to "RMQ" "l3vpn-callback" queue for "secondary_l3vpn_node"
    When "Publish" "l3vpn-delete-failed-callback" response to "RMQ" "l3vpn-callback" queue for "secondary_l3vpn_node"
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "false"
    Then I "read" and validate that a "request" record is "created" in orchestrator "ES" records
    And I validate that "request" record "state" value is "failed"
    Then I "read" and validate that a "service" record is "created" in orchestrator "ES" records
    Then "Read" and validate that a "delete" "failed_l3vpn_callback" message is published in the "RMQ" "orchestrator-callback" queue

  Scenario: Delete the created service record from ES database
    When I send request to "delete" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "deleted" in orchestrator "ES" records
    When I send request to "delete" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "deleted" in orchestrator "ES" records