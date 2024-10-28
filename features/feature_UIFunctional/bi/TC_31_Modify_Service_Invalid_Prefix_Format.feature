Feature:Modify a service with invalid prefix format
  This feature tests the functionality of Modify a service with invalid prefix value and validation

  Scenario:Modify a service with invalid prefix value
    Given I set data values against testcase "31"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then Open "Parameter Information" box by expanding the row
    And Update "InvalidPrefixFormat" of parameter information
    And I click on "Save" button
    And "Errormessage" should be Displayed