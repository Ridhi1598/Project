@portal @tc71
Feature: Execute update request : In-progress request
  This feature tests the Execute the update request for in-progress state

  Scenario: Execute update request: In-progress request
    Given I read test data for testcase
#    When I navigate to "services" page
    Then "Home" page title should be "Services"
    Then I validate that the "advanceFilter" button should be clickable
    Then I click on "advanceFilter" button
    When I search the service by "CSID" only
    Then I click on "firstEdit" button
    When I click on "serviceEditDetails" button
    When I update the Qos and prefix values of the selected service
    Then I click on "save" button
    When I validate that the alert message should appear for "Service Update"
    Then I wait for the "Service Update Page" to load
    Then "ServiceUpdate" page title should be "Service Update Queue"
    Then Fetch the request-id from the Total Requests table of Service Update Page
    Then "In-progress" response should be appear in the Display config results for the created request 
    Then I validate that the "Execute" button should be clickable
    When I click on "Execute" button
    Then I fill the required parameter for Expected config box
    When I click on "submit" button 
    Then Wait for the "errorMessage" popup to appear
    And I validate that the "yesConfirmationRequest" button should be clickable
    When I click on "yesConfirmationRequest" button
    Then "Transactions" page title should be "Transactions"
    When I wait for the "Transactions page" to load
    Then I validate that the created transaction should be in "Submitted" state
    Then Mock "success" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    And I wait for the transaction state to be changed to "Completed"
    And I click on "servicesSidebar" button