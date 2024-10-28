@rollbackTimeout @TC26
Feature: Validate orchestrator response for rollback create service request
  This features validates orchestrator response for rollback create service request

  Scenario: Create Service request record to rollback secondary and primary evpn profile
    Given I read test data for testcase
    When "Publish" "create" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then I "read" and validate that a "request" record is "created" in orchestrator "ES" records
    And I validate that "request" record "state" value is "submitted"
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "true"
    Then "Read" and validate that a "create" "in-process_callback" message is published in the "RMQ" "orchestrator-callback" queue
    Then "Read" and validate that a "create" "secondary_evpn_profile" message is published in the "RMQ" "evpn-publish" queue
    When "Publish" "evpn-create-success-callback" response to "RMQ" "evpn-callback" queue for "secondary_evpn_profile"
    Then "Read" and validate that a "create" "primary_evpn_profile" message is published in the "RMQ" "evpn-publish" queue
    When "Publish" "evpn-create-success-callback" response to "RMQ" "evpn-callback" queue for "primary_evpn_profile"
    Then "Read" and validate that a "create" "secondary_l3vpn_node" message is published in the "RMQ" "l3vpn-publish" queue

  Scenario: Rollback create service request to rollback secondary and primary evpn profile
    When "Publish" "rollback" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that a "delete" "primary_evpn_profile" message is published in the "RMQ" "evpn-publish" queue
    When "Publish" "evpn-delete-success-callback" response to "RMQ" "evpn-callback" queue for "primary_evpn_profile"
    Then "Read" and validate that a "delete" "secondary_evpn_profile" message is published in the "RMQ" "evpn-publish" queue
    When "Publish" "evpn-delete-success-callback" response to "RMQ" "evpn-callback" queue for "secondary_evpn_profile"
    Then I "read" and validate that a "service" record is "not created" in orchestrator "ES" records
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "false"

  Scenario: Delete the created service record from ES database
    When I send request to "delete" the "csid" record in "ES" database
    Then I "read" and validate that a "csid" record is "deleted" in orchestrator "ES" records