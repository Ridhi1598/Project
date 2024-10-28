Feature:Blank Execution Details Form
  This feature tests the functionality of Blank value in Execution Details Form and validation

  Scenario: Blank Execution Details in Review update
    Given I set data values against testcase "60"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    And I navigate view by clicking on "ServiceQueue"
    And "ServiceQueue" page title should be "Service Update Queue"
    And Validate the service is available in service queue
    Then Click on "reviewButton" button in service queue table to open "reviewModal"
    When I click on "AcceptContinueButton" button
    And Validate "performButton" button should be disable
    Then I click on required parameters of Execution details form
    Then ErrorMessage should be displayed under required parameters
    Then I click on "ExecutionDetailsClose" button