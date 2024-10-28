@bngDecommission @rmq @dev
Feature: Decommission the BNG devices on Dev env
  This features to Decommission the devices on Dev env

  Scenario: Clear the portal queue test on dev env
    When I set the Dev RMQ URL
    When I set api endpoint "/api/queues/%2F/cs_portal_queue_test/contents" for "DELETE"
    Then I Set Consumer POST request Body "ClearPortalQueue.json"
    When I send "DELETE" request
    Then I extract the response code value

  Scenario: Check the status of BNG devices on Dev and decommission it
    When I set the Dev RMQ URL
    And I set api endpoint "/api/exchanges/%2F/consumer_rabbit_exchange/publish" for "POST"
    And I Set Consumer POST request Body "getActiveBNGDevices.json" for decommission
    When I send CS "POST" request
    When I wait for "20" seconds for request to be timed out
    When I set api endpoint "/api/queues/%2F/cs_portal_queue_test/get" for "POST"
    Then I Set Consumer POST request Body "GetPortalQueueMessage.json"
    When I send CS "POST" request
    And I validate consumer expected response code "200" for "POST"
    Then I Decommission the BNG devices if the devices are onboarded
    And I print the response




