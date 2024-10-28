Feature:Modify a service with invalid prefix value
  This feature tests the functionality of Modify a service with invalid prefix value and validation

  Scenario:Modify a service with invalid prefix value
    Given I set data values against testcase "30"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then Open "Parameter Information" box by expanding the row
    And Update "InvalidPrefixFormat" of parameter information
    And I click on "Save" button
    Then I click on "AlertOk" button
    And I Wait for next page to load
    Then "ServiceUpdateQueue" page title should be "Service Update Queue"
    Then I click on "Accept&Execute" button
    Then I fill the required parameters for Execution details form
    Then "ErrorAlertMessage" should be displayed