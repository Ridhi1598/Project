@L2TopologyEngine @unbindQueue @rmq
Feature: This feature to Update the nodes 1 for L2 Topology with invalid request payload

   Background: Clearing the queue as a Test Prerequisite
     Given I configure the Consumer Nodes "InvalidNode1 , InvalidNode2"
    Given I set Consumer "RMQ" url
    And I set CS api endpoint "/api/queues/%2F/l2_topology_engine_queue_test/contents" for "DELETE"
    When I send CS "DELETE" request
    And I validate consumer expected response code "204" for "DELETE"
    And I set CS api endpoint "/api/queues/%2F/l2_topology_engine_queue_test/get" for "POST"
    And I Set POST Consumer request Body "rmq_get_message.json" for "l2_topology_engine_queue_test"
    When I send CS "POST" request
    And I validate consumer expected response code "200" for "POST"
    And Validate that the queue is empty for Consumer
    And I set CS api endpoint "/api/queues/%2F/cs_portal_queue_test/contents" for "DELETE"
    When I send CS "DELETE" request
    And I validate consumer expected response code "204" for "DELETE"
    And I set CS api endpoint "/api/queues/%2F/cs_portal_queue_test/get" for "POST"
    And I Set POST Consumer request Body "rmq_get_message.json" for "cs_portal_queue_test"
    When I send CS "POST" request
    And I validate consumer expected response code "200" for "POST"
    And Validate that the queue is empty for Consumer

  Scenario: TC21 Verify the L2 Topology Update node 1 with invalid request payload
    When I set CS api endpoint "/api/exchanges/%2F/{exchange_Name}/publish" for "POST" to publish the message
    When I Set Consumer POST "TC21_UpdateNodesInvalid.json" request Body to publish the message
    When I send CS "POST" request
    And I validate consumer expected response code "200" for "POST"
    And I set CS api endpoint "/api/queues/%2F/cs_portal_queue_test/get" for "POST"
    And I Set POST Consumer request Body "cs_portal_queue_test_getmessage.json" for "cs_portal_queue_test"
    When I send CS "POST" request
    And I validate consumer expected response code "200" for "POST"
    And I validate the consumer response body contains the request id
    And I validate the consumer response body contains "error"
    And I validate the consumer response body contains "Node does not exist in L2 Topology Database - Details: Node EDTNABTFNG09 does not exist in L2 Topology Database"


