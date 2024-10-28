Feature: Check RollBack Delete MWR  scenario
  This feature tests RollBack Scenarios for the delete MWR

 Scenario: RollBack Operation for delete MWR
    Given I set data values against testcase "43"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    And "OperationTypeValue" should be "delete mwr"
    And "OperationResultValue" should be "COMPLETED"
    And I look for the associated Request ID
    Then Open "Parameter Information" box by expanding the row
    Then Validate that Parameter information should be "Data Not Available!"
    When I click on "HistoryButton" and "History" Modal should open
    Then Validate that the associated Request ID should be same
    And  RollBack button should be available in action column
    Then I click on "RollBackButton" and "Alert" Modal should open
    When I click on "AlertContinue" button
    When "AlertMessage" should be "Successfully reverted!"
    Then I click on "AlertOk" button
    Then Wait for the operation to submit
    Then "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then Validate that a new request id is generated
    Then "OperationTypeValue" should be "rollback service"
    Then "OperationResultValue" should be "SUBMITTED"
    And Validate that the Customer Name and Network Element Name should be empty
    Then Wait for the "OperationResultValue" to "complete" and refresh the page
    Then "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then "OperationTypeValue" should be "rollback service"
    Then "OperationResultValue" should be "COMPLETED"
    #Then Open "Parameter Information" box by expanding the row
    #And I look for the "NetworkElementValue" for "after" scenario
    #And I look for the "CSIDValue" for "after" scenario
    #Then Validate "NetworkElementName" and "CSIDValue" different after scenario
    Then I click on "HistoryButton" and "History" Modal should open
    And Validate RollBack config button should be available on action column
    Then I click on "RollBackButton" button
    Then I Wait for the Rollback Configuration Information to appear
    And Validate that mwr device is available in Rollback Configuration Information
    Then I click on Close History Modal button