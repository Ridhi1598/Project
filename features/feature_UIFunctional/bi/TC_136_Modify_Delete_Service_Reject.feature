Feature:Modify Delete Service
  This feature tests the functionality of Modify a deleted service and validation

  Scenario: Modify an MWR service and validation
    Given I set data values against testcase "136"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    Then I filter and search the "OperationType" parameter
    And Wait for the search results to appear
    And Validate that all results have the expected result for "OperationType" for "exact" search
    When Open "Parameter Information" box by expanding the row
    And Validate "Save" button should be disable