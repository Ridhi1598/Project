@orchestrator @createQueue @rmq @preSetup @demo
Feature: Clear the queue of its contents
  This feature clears all the messages from the test queue before the tests are executed

  Scenario: Check if callback queue exists
    Given I set BI "RMQ" url
    And I set api endpoint "/api/queues/%2F/tinaa-callbacks-tests" for "GET"
    When I send "GET" request
    Then I extract the response code value
    And I validate "tinaa-callbacks-tests" queue is binded to "bi-ctrl" exchange
    Given I validate bind status from the previous step
    And I set api endpoint "/api/queues/%2F/tinaa-callbacks-tests" for "PUT"
    And I Set PUT request Body "rmq_create_queue.json" for "tinaa-callbacks-tests"
    Then I send "PUT" request
    When I validate expected response code "201" or "204" for "PUT"
    Given I set api endpoint "/api/bindings/%2F/e/bi-ctrl/q/tinaa-callbacks-tests" for "POST"
    And I Set POST request Body "bindQueue.json" for "tinaa-bi-request-callbacks"
    When I send "POST" request
    And I validate expected response code "201" for "POST"
    And Validate response header "location" for "tinaa-callbacks-tests/tinaa-bi-request-callbacks"
    And I set api endpoint "/api/exchanges/%2F/bi-ctrl/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "tinaa-callbacks-tests" queue "has" "bi-ctrl" exchange as source