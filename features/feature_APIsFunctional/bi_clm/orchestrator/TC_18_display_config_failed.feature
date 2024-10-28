@display @TC18
Feature: Validate orchestrator response for display config request
  This features validates orchestrator response for failed display config request

  Background: Read test data
    Given I read test data for testcase

  Scenario: Create a temporary service record in ES database
    When I send request to "create" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "created" in orchestrator "ES" records
    And Read the "before" values for associated "prefix" values
    And Read the "before" values for associated "speed" values
    When I send request to "create" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records

  Scenario: Display config request with failed response from l3vpn controller for current secondary l3vpn node
    When "Publish" "display" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then I "read" and validate that a "request" record is "created" in orchestrator "ES" records
    And I validate that "request" record "state" value is "pending"
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "true"
    Then "Read" and validate that a "display" "in-process_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then "Read" and validate that a "display" "secondary_evpn_profile_current" message is published in the "RMQ" "evpn-publish" queue
    When "Publish" "evpn-display-success-callback" response to "RMQ" "evpn-callback" queue for "secondary_evpn_profile_current"
    Then "Read" and validate that a "display" "primary_evpn_profile_current" message is published in the "RMQ" "evpn-publish" queue
    When "Publish" "evpn-display-success-callback" response to "RMQ" "evpn-callback" queue for "primary_evpn_profile_current"
    Then "Read" and validate that a "display" "secondary_l3vpn_node" message is published in the "RMQ" "l3vpn-publish" queue
    When "Publish" "l3vpn-display-current-in-process-callback" response to "RMQ" "l3vpn-callback" queue for "secondary_l3vpn_node"
    When "Publish" "l3vpn-display-current-failed-callback" response to "RMQ" "l3vpn-callback" queue for "secondary_l3vpn_node"
    Then "Read" and validate that a "display" "get-config-failed_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "false"

  Scenario: Delete the created service record from ES database
    When I send request to "delete" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "deleted" in orchestrator "ES" records
    When I send request to "delete" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "deleted" in orchestrator "ES" records