@controller @clearQueue @rmq @preSetup @demo
Feature: Clear the queue of its contents
  This feature clears all the messages from the test queue before the tests are executed

  Scenario: Clear all the messages from the test queue
    Given I set l3vpn "RMQ" url
    And I set api endpoint "api/queues/%2F/tinaa-callbacks-tests/contents" for "DELETE"
    When I send "DELETE" request
    And I validate expected response code "204" for "DELETE"
    Then I set api endpoint "api/queues/%2F/tinaa-callbacks-tests/get" for "POST"
    And I Set POST request Body "rmq_get_message.json" for "tinaa-callbacks-tests"
    And I send "POST" request
    And I validate expected response code "200" for "POST"
    And Validate that the queue is empty