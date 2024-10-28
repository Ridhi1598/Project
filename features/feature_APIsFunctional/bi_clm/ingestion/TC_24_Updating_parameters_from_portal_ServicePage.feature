@ingestion
Feature: Validate ingestion response for updating an existing service through portal
  This features validates ingestion response for updating an existing service through portal

  Scenario: Create a service record and update params from TINAA
    Given I read test data for testcase
    When I create "1" document id for request record creation
    When I send request to "create" a "BaseService" record in "ES" "request" record
    When I send request to "create" a "Service" record in "ES" "service" record
    When I generate access token for authorization
    When I Send "update" request for "ingestion"
    Then Validate that the new request id is returned
    And I extract response value for "requestId"
    And Validate that the request id has "updated" parameters
    Then I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record
