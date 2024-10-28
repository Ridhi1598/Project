Feature: Check RollBack Create MWR  scenario
  This feature tests RollBack Scenarios for the create MWR

 Scenario: RollBack Operation for create MWR
    Given I set data values against testcase "42"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    And "OperationTypeValue" should be "create mwr"
    And "OperationResultValue" should be "COMPLETED"
    And I look for the associated Request ID
    Then Open "Parameter Information" box by expanding the row
    And I look for the "NetworkElementValue" for "before" scenario
    And I look for the "CSIDValue" for "before" scenario
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
    Then Wait for the "OperationResultValue" to "complete" and refresh the page*
    Then "Home" page title should be "BI service dashboard"
    Then I look for a Customer Service ID
    Then "OperationTypeValue" should be "rollback service"
    Then "OperationResultValue" should be "COMPLETED"
    Then Open "Parameter Information" box by expanding the row
    And I look for the "NetworkElementValue" for "after" scenario
    And I look for the "CSIDValue" for "after" scenario
    Then Validate "NetworkElementName" and "CSIDValue" different after scenario