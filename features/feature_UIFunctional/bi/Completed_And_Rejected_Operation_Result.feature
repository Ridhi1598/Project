Feature: Completed and Rejected Operation Result
  This feature tests the functionality of completed and Rejected operation validation of modify port

  Background:
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"

  Scenario: Completed Operation result
    Then I look for a "Completed" Operation Result of "modify port" Operation
    Then Open "Parameter Information" box by expanding the row
    Then Validate that the Parameter information should be Available

  Scenario: Rejected Operation result
    Then I look for a "Rejected" Operation Result of "modify port" Operation
    Then Open "Parameter Information" box by expanding the row
    Then Validate that Parameter information should be "Data Not Available!"
