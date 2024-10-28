@portal @tc130
Feature: Execute service from BI service queue from a read only user

  Scenario: Execute service from BI service queue from a read only user
    Given I set data values against testcase "130"
    Given I should land on BI Home page
    And "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    And Validate the service is available in service queue
    And Validate that service request has "Operation" as "modify"
    And Click on "reviewButton" button in service queue table to open "reviewModal"
    And I read the "old" "requestId" for "modify" scenario
    When I click on "cancelButton" button
    And An "Confirmation" box should open
    And I validate the "confirm" message in the "Confirmation" box for "cancel"
    And I click on "Continue" button
    And An "Alert" box should open
    And I validate the "error" message in the "Alert" box for "cancel"
    And I click on "OK" button
    And Validate the service is available in service queue
    And Click on "reviewButton" button in service queue table to open "reviewModal"
    And I read the "old" "requestId" for "modify" scenario
    Then Validate that the "cancelButton" button is "enabled"