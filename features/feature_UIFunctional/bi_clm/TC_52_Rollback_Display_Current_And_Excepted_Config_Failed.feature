@TC_52
Feature: RollBack - Display current and expected config: Failed
  This feature tests the functionality related to displaying the current and expected config - Failed

  Scenario: Display current and expected config: Failed
    Given I read test data for testcase
    When "Home" page title should be "Services"
    Then I validate that the "advanceFilter" button should be clickable
    Then I click on "advanceFilter" button
    When I search the service by "CSID" only
    Then I Validate that the Service state should be "active"
    Then I go to "Services" page
    When I click on "rollback" button
    Then I wait for the loader to be disabled
    And I wait for the "parameterInformation" element to be visible
    When I select the version from the dropdown to rollback the service   
    Then I click on "yesConfirmationRequest" button
    When "ServiceUpdate" page title should be "Service Update Queue"
    Then I search the request by using "CSID" from Service Update Queue page
    Then Fetch the request-id from the Total Requests table of Service Update Page
    Then Mock "display-config-failed" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    Then "Failed" response should be appear in the Display config results for the created request
    When I click on "Cancel" button
    Then I click on "Confirm" button
    Then I validate the pop-up message for "Cancel request"
    And I click on "servicesSidebar" button