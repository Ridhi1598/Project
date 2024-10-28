@portal @tc131
Feature: Execute service from BI service queue from a read only user

  Scenario: Execute service from BI service queue from a read only user
    Given I set data values against testcase "131"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    When I "execute" update request for selected service id
    Then Validate that the "performButton" button is "disabled"