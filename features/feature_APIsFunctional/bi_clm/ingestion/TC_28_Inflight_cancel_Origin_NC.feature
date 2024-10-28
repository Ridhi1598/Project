Feature: Validate ingestion response for cancelling an update request originating from NC
  This features validates ingestion response for cancelling an update request originating from NC

  Scenario: Cancel a pending service request originating from NC
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "cancel" request for "ingestion"
    And I validate the response body should have "status" as "success"
    Then I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record
    And I validate that a "request" record is found in "clm-ingestion-service-requests" index
    And I validate record format for "request" record
    And Validate that request "state" is "cancelled"
    And Validate that the "user_id" is same as the query parameter