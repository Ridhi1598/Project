@controller @createQueue @rmq @preSetup
Feature: Clear the queue of its contents
  This feature clears all the messages from the test queue before the tests are executed

  Scenario: Check if callback queue exists
    Given I set L3VPN "RMQ" url
    When I set api endpoint "api/queues/%2F/tinaa-requests-tests" for "GET" for IE
    Then I send "GET" request for IE
    Then I extract the response code value for IE
    And I validate "tinaa-requests-tests" queue is binded to "l3vpn-ingestion" exchange for IE
    When I validate bind status from the previous step for IE
    And I set api endpoint "api/queues/%2F/tinaa-requests-tests" for "PUT" for IE
    And I Set PUT request Body "rmq_create_queue.json" for "tinaa-requests-tests" for IE
    Then I send "PUT" request for IE
    When I validate expected response code "201" or "204" for "PUT" for IE
    Then I set api endpoint "api/bindings/%2F/e/l3vpn-ingestion/q/tinaa-requests-tests" for "POST" for IE
    And I Set POST request Body "bindQueue.json" for "tinaa-requests-tests" for IE
    When I send "POST" request for IE
    Then Validate expected response code "201" for "POST" for IE
    And Validate response header "location" for "tinaa-requests-tests/tinaa-l3vpn-requests" for IE
    And I set api endpoint "api/exchanges/%2F/l3vpn-ingestion/bindings/source" for "GET" for IE
    When I send "GET" request for IE
    And Validate expected response code "200" for "GET" for IE
    And Validate that "tinaa-requests-tests" queue "has" "l3vpn-ingestion" exchange as source for IE