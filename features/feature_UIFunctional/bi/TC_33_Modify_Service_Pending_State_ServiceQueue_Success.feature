Feature:Modify a service in pending state
  This feature tests the functionality of Modify service in pending state and validation

  Scenario: Modify a service in pending state
    Given I set data values against testcase "33"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    And Validate the service is available in service queue
    Then Click on "reviewButton" button in service queue table to open "reviewModal"
    And Wait for loader bar to disappear
    When I click on "Edit" button
    And Update "port" value for the service
    And I click on "Save" button
    And An "Alert" box should open
    Then "alertMessage" should be "Successfully Updated!"
    Then I click on "OK" button