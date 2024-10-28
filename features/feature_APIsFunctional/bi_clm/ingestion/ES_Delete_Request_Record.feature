Feature: Delete Request Record in controller requests index

  Scenario: Update ES record for a delete request record in "clm-ingestion-service-requests" index
    Given I set BI "ES" url
    And I set data values against test case "19"
    And I create a document id for request record creation
    And I set api endpoint for "delete" a after requests record
    And I set api request body for "delete" a requests record
    When I send HTTP request for "delete" service
#    Then I validate that the requests record is "deleted"
