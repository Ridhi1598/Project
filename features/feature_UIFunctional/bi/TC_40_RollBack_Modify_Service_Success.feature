Feature: RollBack Operation
  This feature tests the functionality of Roll Back Operation and validation

  Scenario: RollBack Operation and validation
    Given I set data values against testcase "10"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then "OperationTypeValue" should be "modify service"
    Then "OperationResultValue" should be "COMPLETED"
    Then I look for the associated Request ID
    Then Open "Parameter Information" box by expanding the row
    Then I look for the associated prefix value
    When I click on "HistoryButton" and "History" Modal should open
    Then Validate that the associated Request ID should be same
    And  RollBack button should be available in action column
    Then I click on "RollBackButton" and "Alert" Modal should open
    When I click on "AlertContinue" button
    Then "AlertMessage" should be "Successfully reverted!"
    Then I click on "AlertOk" button
    Then Wait for the operation to submit
    Then "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then Validate that a new request id is generated
    Then "OperationTypeValue" should be "rollback service"
    Then "OperationResultValue" should be "SUBMITTED"
    And Validate that the Customer Name and Network Element Name should be empty
    Then Wait for the "OperationTypeValue" to "COMPLETED" and refresh the page
    Then "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then "OperationResultValue" should be "COMPLETED"
    Then Open "Parameter Information" box by expanding the row
    And Validate that associated prefix value should be displayed
    Then I click on "HistoryButton" button
    And Validate RollBack config button should be available on action column
    Then I click on Close History Modal button
    Then "Home" page title should be "BI service dashboard"
