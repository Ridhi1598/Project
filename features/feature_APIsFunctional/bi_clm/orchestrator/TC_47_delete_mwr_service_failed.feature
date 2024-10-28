@deletemwr @TC47
Feature: Validate orchestrator response for delete mwr service request
  This features validates orchestrator response for failed delete mwr service request

  Scenario: Create a temporary service record in ES database
    Given I read test data for testcase
    When I send request to "create" the "base_service_request" record in "ES" database
    When I send request to "create" the "mwr_service_request" record in "ES" database
    When I send request to "create" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "created" in orchestrator "ES" records
    When I send request to "create" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records

  Scenario: Delete Mwr Service request with failed response for secondary node
    When "Publish" "delete_mwr" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then I "read" and validate that a "request" record is "created" in orchestrator "ES" records
    And I validate that "request" record "state" value is "submitted"
    Then "Read" and validate that a "update" "in-process_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then "Read" and validate that a "update" "primary_l3vpn_node" message is published in the "RMQ" "l3vpn-publish" queue
    When "Publish" "l3vpn-in-process-callback" response to "RMQ" "l3vpn-callback" queue for "primary_l3vpn_node"
    When "Publish" "l3vpn-update-success-callback" response to "RMQ" "l3vpn-callback" queue for "primary_l3vpn_node"
    Then "Read" and validate that a "update" "secondary_l3vpn_node" message is published in the "RMQ" "l3vpn-publish" queue
    When "Publish" "l3vpn-in-process-callback" response to "RMQ" "l3vpn-callback" queue for "secondary_l3vpn_node"
    When "Publish" "l3vpn-update-failed-callback" response to "RMQ" "l3vpn-callback" queue for "secondary_l3vpn_node"
    Then I "read" and validate that a "service" record is "created" in orchestrator "ES" records
    Then I validate that the "service" record has "3" "site-network-access" records for "mwr_service"
    Then "Read" and validate that a "delete" "failed_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then "Read" and validate that a "update" "primary_l3vpn_node" message is published in the "RMQ" "l3vpn-publish" queue
    When "Publish" "l3vpn-in-process-callback" response to "RMQ" "l3vpn-callback" queue for "primary_l3vpn_node"
    When "Publish" "l3vpn-update-success-callback" response to "RMQ" "l3vpn-callback" queue for "primary_l3vpn_node"
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "false"
    And Validate that a "mwr_l3vpn_node" is "added to" the "csid" record

  Scenario: Delete the created service record from ES database
    When I send request to "delete" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "deleted" in orchestrator "ES" records
    When I send request to "delete" the "service" record in "ES" database
    Then I "read" and validate that a "service" record is "deleted" in orchestrator "ES" records