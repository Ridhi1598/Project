@portal @tc100
Feature: Execute service from BI service queue from a read only user

  Scenario: Execute service from BI service queue- review modal from a read only user
    Given I set data values against testcase "100"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    When I "review" update request for selected service id
    And I click on "AcceptContinueButton" button once visible
    And I fill the required parameters for Execution details form
    And An "Alert" box should open
    And I validate the "error" message in the "Alert" box for "execute"
    And I click on "OK" button
    And I validate that the "error" message is as expected
    Then I log out
    And "Landing" page title should be "TINAA BUSINESS INTERNET SERVICES"