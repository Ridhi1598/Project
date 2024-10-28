@portal @tc35
Feature: Update parameters of the service whose state is pending - Success
  This feature tests the functionality related to Update the parameters for pending state service  

  Scenario: Update parameter for a pending service - Success
    Given I read test data for testcase
    When I click on "edit" button
    Then I wait for the loader to be disabled
    Then I click on "serviceEditDetails" button
    And I go to "Home" page
    When I update the Qos and prefix values of the selected service
    Then I click on "save" button
    When I validate that the alert message should appear for "Service Update"
    Then I wait for the "Service Update Page" to load
    Then "ServiceUpdate" page title should be "Service Update Queue"
    Then Fetch the request-id from the Total Requests table of Service Update Page
    Then I click on "firstRequestServiceUpdateQueue" button
    When Mock "display-config-success" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    Then "Success" response should be appear in the Display config results for the created request
    Then I click on "ServicesSidebar" button
