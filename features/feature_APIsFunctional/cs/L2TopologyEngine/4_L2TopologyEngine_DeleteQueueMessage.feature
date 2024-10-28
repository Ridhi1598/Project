@L2TopologyEngine @controller @csunbindQueue @rmq @preSetup
Feature: Validate to delete all the messages from RMQ queue
  This feature to delete the messages from RMQ queue

   Scenario: Validate to delete the messages from the RMQ
    Given I set CS "RMQ" url
    When I set api endpoint "/api/queues/%2F/cs_portal_queue_ta/contents" for "DELETE"
    Then I Set Consumer POST request Body "DeleteQueueMessage.json"
    When I send "DELETE" request
    Then I extract the response code value

