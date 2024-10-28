Feature: Create Request Record in controller requests index

  Scenario: Update ES record for a create request record in "clm-ingestion-service-requests" index
    Given I set BI "ES" url
    And I set data values against test case "7"
    And I create a document id for request record creation
    And I set api endpoint for "create" a requests record
    And I set api request body for "create" a requests record
    And Update request state "submitted" for "create" service
    When I send HTTP request for "create" service
    Then I validate that the requests record is "created"
