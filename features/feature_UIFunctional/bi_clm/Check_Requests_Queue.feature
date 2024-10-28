@ingestion @createQueue @rmq @preSetup
Feature: Clear the queue of its contents
  This feature clears all the messages from the test queue before the tests are executed

  Scenario: Check if callback queue exists
    Given I set "RMQ" url
    And I set api endpoint "/api/queues/%2F/tinaa-requests-tests" for "GET"
    When I send "GET" request
    Then I extract the response code value
    And I validate "tinaa-requests-tests" queue is binded to "com.telus.tinaa.bsaf.clm.bi" exchange
    Given I validate bind status from the previous step
    And I set api endpoint "/api/queues/%2F/tinaa-requests-tests" for "PUT"
    And I Set PUT request Body "rmq_create_queue.json" for "com.telus.tinaa.bsaf.clm.bi.ingestion.request"
    Then I send "PUT" request
    When I validate expected response code "201" or "204" for "PUT"
    Given I set api endpoint "/api/bindings/%2F/e/com.telus.tinaa.bsaf.clm.bi/q/tinaa-requests-tests" for "POST"
    And I Set POST request Body "bindQueue.json" for "com.telus.tinaa.bsaf.clm.bi.ingestion.request"
    When I send "POST" request
    And I validate expected response code "201" for "POST"
    And Validate response header "location" for "tinaa-requests-tests/com.telus.tinaa.bsaf.clm.bi.ingestion.request"
    And I set api endpoint "/api/exchanges/%2F/com.telus.tinaa.bsaf.clm.bi/bindings/source" for "GET"
    Then I send "GET" request
    And I validate expected response code "200" for "GET"
    And Validate that "tinaa-requests-tests" queue "has" "com.telus.tinaa.bsaf.clm.bi" exchange as source