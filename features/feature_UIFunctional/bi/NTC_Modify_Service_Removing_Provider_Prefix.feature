Feature:Modify service by removing provider prefix
  This feature tests the functionality of Modify a service by removing provider prefix value and validation

  Scenario:Modify a service by removing provider prefix
    Given I set data values against testcase "19"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then Open "Parameter Information" box by expanding the row
    And Update "RemovingProviderPrefix" of parameter information
    And I click on "Save" button
    And "Errormessage" should be "IPV4 Provider Prefixes is required!"