Feature:Modify a service without changing any parameter from dashboard
  This feature tests the functionality of Modify service without changing any parameter from dashboard and validation

  Scenario: Modify a service without changing any parameter from dashboard
    Given I set data values against testcase "39"
    Given I should land on BI Home page
   When "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    And Validate the service is available in service queue
    Then Click on "reviewButton" button in service queue table to open "reviewModal"
    And I filter and search the "serviceId" parameter
    And Wait for the "serviceId" search results to appear as expected
    And Open "Parameter Information" box by expanding the row
    Then I click on "Edit" button
    Then I click on "Save" button
    And An "Alert" box should open
    And "alertMessage" should be "The entered values should be different than the ones assigned before"