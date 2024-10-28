@portal @tc97
Feature: Update service from BI dashboard from a read only user

  Scenario: Update service from BI dashboard from a read only user
    Given I set data values against testcase "97"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    When Filter and search the "serviceId" for update request
    And Open "Parameter Information" box by expanding the row
    And Update "port" value for the service
    And I click on "Save" button
    And An "Alert" box should open
    And I validate the "error" message in the "Alert" box for "update"
    And I click on "OK" button
    And I validate that the "error" message is as expected
    Then I log out
    And "Landing" page title should be "TINAA BUSINESS INTERNET SERVICES"