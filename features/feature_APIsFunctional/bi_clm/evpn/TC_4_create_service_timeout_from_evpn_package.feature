Feature: Validate evpn response for create service request
  This features validates evpn response for timed out create service request

  Scenario: Create Service request with no response from evpn package
    Given I read test data for testcase
    When "Publish" "create" evpn message to "RMQ" "evpn-publish" queue
    Then "Read" and validate that the message is consumed by evpn from "RMQ" "evpn-publish" queue
    When Validate a record is "created" in "evpn_bsaf_request_tracker" table in "postgres" db for "create"
    Then Validate that the request state is "submitted" for "evpn_bsaf_request_tracker" table
    When Validate a record is "created" in "evpn_external_request_tracker" table in "postgres" db for "create"
    Then Validate that the request state is "in progress" for "evpn_external_request_tracker" table
    When I "start" zookeeper connectivity for node validation
    When I fetch "evpn" node data from zookeeper for "create"
    And Validate a "create" node is "created" in zookeeper for "evpn"
    And I "stop" zookeeper connectivity for node validation
    And Wait for expected request processing duration
    When Validate a record is "created" in "evpn_bsaf_request_tracker" table in "postgres" db for "create"
    Then Validate that the request state is "timeout" for "evpn_bsaf_request_tracker" table
    When Validate a record is "created" in "evpn_external_request_tracker" table in "postgres" db for "create"
    Then Validate "4" entries are found for "evpn_external_request_tracker" table for "create"
    Then Validate that the request state is "in progress" for "evpn_external_request_tracker" table
    Then "Read" and validate that a "create" "timeout_callback" response is published in the "RMQ" "orchestrator-callback" queue
    And Validate that "timeout_callback" response has "status" as "timeout"
    When I "start" zookeeper connectivity for node validation
    And Validate a "create" node is "deleted" in zookeeper for "evpn"
    When I fetch "evpn" node data from zookeeper for "create"
    And Validate a "rollback" node is "created" in zookeeper for "evpn"
    And I "stop" zookeeper connectivity for node validation
    And Wait for expected request processing duration
    When I "start" zookeeper connectivity for node validation
    And Validate a "rollback" node is "deleted" in zookeeper for "evpn"
    And I "stop" zookeeper connectivity for node validation
    When Validate a record is "not created" in "evpn_service" table in "postgres" db for "create"