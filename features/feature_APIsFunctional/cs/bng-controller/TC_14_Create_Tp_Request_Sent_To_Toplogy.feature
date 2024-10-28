@tc14 @bngController
Feature: Create Tp Request sent to topology
  This feature validates that functionality related to create Tp Request sent to topology

   Scenario Outline: tc_14: This scenario validate that the functionality related to create Tp Request sent to topology
    Given I read test data for BNG controller testcases
    When "Read" and validate that the "get" "l2_request" message is published in the "RMQ" "l2_topology_test" queue for BNG
    Then "Publish" "<tc_num><published>" request message to "RMQ" "bng_controller" queue for BNG
    Then "Read" and validate that the message is consumed by orchestrator from "RMQ" "bng_controller" queue for BNG

    Examples:
     |tc_num   | published                            |  bng_to_portal                                            |
     |tc_14   | _create_tp_request_sent_to_topology   | _create_tp_request_sent_to_topology_bng_to_portal_success |

