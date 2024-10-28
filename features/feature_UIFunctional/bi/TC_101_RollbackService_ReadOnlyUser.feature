@portal @tc101
Feature: Rollback service from BI service dashboard from a read only user

  Scenario: Rollback service from BI service dashboard from a read only user
    Given I set data values against testcase "101"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    When Filter and search the "serviceId" for update request
    Then I navigate History Modal by clicking on "ActionButton"
#  Add Steps for rollback
    And I click on "Yes" button
    And An "Alert" box should open
    And I validate the "error" message in the "Alert" box for "Rollback"
    And I click on "OK" button
    And I validate that the "error" message is as expected
    Then I log out
    And "Landing" page title should be "TINAA BUSINESS INTERNET SERVICES"