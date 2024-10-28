@controller @clearQueue @rmq @preSetup
Feature: Clear the queue of its contents
  This feature clears all the messages from the test queue before the tests are executed

  Scenario: Clear all the messages from the test queue
    Given I set L3VPN "RMQ" url
    And I set api endpoint "api/queues/%2F/tinaa-callbacks-tests/contents" for "DELETE" for IE
    When I send "DELETE" request for IE
    And Validate expected response code "204" for "DELETE" for IE
    Then I set api endpoint "api/queues/%2F/tinaa-callbacks-tests/get" for "POST" for IE
    And I Set POST request Body "rmq_get_message.json" for "tinaa-callbacks-tests" for IE
    And I send "POST" request for IE
    And Validate expected response code "200" for "POST" for IE
    And Validate that the queue is empty for IE