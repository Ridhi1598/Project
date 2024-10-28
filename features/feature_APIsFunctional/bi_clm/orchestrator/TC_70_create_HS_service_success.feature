@HS @TC70
Feature: Validate orchestrator response for create HS service request
  This features validates orchestrator response for successful create service request - HS

  Scenario: Create HS service request with success response from l2vpn and l3vpn controllers
    Given I read test data for testcase
    When "Publish" "createHS" service message to "RMQ" "orchestrator-publish" queue
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "orchestrator-publish" queue
    Then I "read" and validate that a "request" record is "created" in orchestrator "ES" records
    And I validate that "request" record "state" value is "submitted"
    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
    And I validate that "csid" record "in_progress" value is "true"
    Then "Read" and validate that a "create" "in-process_callback" message is published in the "RMQ" "orchestrator-callback" queue


#    Then "Read" and validate that a "create" "secondary_l2vpn_node" message is published in the "RMQ" "l2vpn-publish" queue
#    When "Publish" "l2vpn-in-process-callback" response to "RMQ" "l2vpn-callback" queue for "secondary_l2vpn_node"
#    When "Publish" "l2vpn-create-success-callback" response to "RMQ" "l2vpn-callback" queue for "secondary_l2vpn_node"
#    Then "Read" and validate that a "create" "primary_l2vpn_node" message is published in the "RMQ" "l2vpn-publish" queue
#    When "Publish" "l2vpn-in-process-callback" response to "RMQ" "l2vpn-callback" queue for "primary_l2vpn_node"
#    When "Publish" "l2vpn-create-success-callback" response to "RMQ" "l2vpn-callback" queue for "primary_l2vpn_node"
#
#
#    Then "Read" and validate that a "create" "secondary_l3vpn_node" message is published in the "RMQ" "l3vpn-publish" queue
#    When "Publish" "l3vpn-in-process-callback" response to "RMQ" "l3vpn-callback" queue for "secondary_l3vpn_node"
#    When "Publish" "l3vpn-create-success-callback" response to "RMQ" "l3vpn-callback" queue for "secondary_l3vpn_node"
#    Then "Read" and validate that a "create" "primary_l3vpn_node" message is published in the "RMQ" "l3vpn-publish" queue
#    When "Publish" "l3vpn-in-process-callback" response to "RMQ" "l3vpn-callback" queue for "primary_l3vpn_node"
#    When "Publish" "l3vpn-create-success-callback" response to "RMQ" "l3vpn-callback" queue for "primary_l3vpn_node"
#
#
#    Then I "read" and validate that a "csid" record is "created" in orchestrator "ES" records
#    And I validate that "csid" record "in_progress" value is "false"
##    step for l2 node validation
#    Then I "read" and validate that a "service" record is "created" in orchestrator "ES" records
#    Then "Read" and validate that a "create" "success_callback" message is published in the "RMQ" "orchestrator-callback" queue
#
#  Scenario: Delete the created service record from ES database
#    Given I read test data for testcase
#    When I send request to "delete" the "csid" record in "ES" database
#    Then I "read" and validate that a "csid" record is "deleted" in orchestrator "ES" records
#    When I send request to "delete" the "service" record in "ES" database
#    Then I "read" and validate that a "service" record is "deleted" in orchestrator "ES" records
