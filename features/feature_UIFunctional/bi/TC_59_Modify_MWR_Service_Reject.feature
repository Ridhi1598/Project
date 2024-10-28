Feature:Modify MWR Service
  This feature tests the functionality of Modify an MWR service and validation

  Scenario: Modify an MWR service and validation
    Given I set data values against testcase "59"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I filter and search the "serviceId" parameter
    Then I filter and search the "OperationType" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Validate that "operationType" should be "create mwr"
    When Open "Parameter Information" box by expanding the row
    And Validate "Save" button should be disable