@ingestion
Feature: Validate ingestion response for updating an existing service through portal
  This features validates ingestion response for updating an existing service through portal

  Scenario: Update ES record for a create request record in "bi_clm-ingestion-requests" index
    Given I set BI "ES" url
    And I set data values against test case "51"
    And I create a document id for request record creation
    And I set api endpoint for "create" a requests record
    And I set api request body for "create" a requests record
    And Update request state "pending" for "create" service
    When I send HTTP request for "create" service
    Then I validate that the requests record is "created"

  Scenario: Update service record for in_progress state to false
    Given I set data values against test case "54"
    And I set BI "ES" url
    And I read service id for test case
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    And Update in_progress state for the service
    And I validate that a "service" record is found in "clm-ingestion-service-services" index
    When Validate the service record for "in-progress" state to be "false"

@updateFromServiceQueue
  Scenario: Updating a pending service request
    Given I read test data for testcase
    And I generate access token for authorization
    When I Send "update" request for "ingestion"
    Then I validate the response body should have "status" as "success"
    And Validate that the request id has "edited" parameters
    Then I validate that a "service" record is found in "clm-ingestion-service-services" index
    And I validate record format for "service" record
