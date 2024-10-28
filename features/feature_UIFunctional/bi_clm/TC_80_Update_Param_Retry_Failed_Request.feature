@portal @tc80
Feature: Update Parameter - Retry Functionality
  This feature tests the Retry functionality from Service Update Queue page

  Scenario: Retry functionality from Service Update Queue
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
    Then Mock "display-config-failed" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    Then "Failed" response should be appear in the Display config results for the created request
    Then I click on "retryButton" button
    Then "In-progress" response should be appear in the Display config results for the created request 
    Then "Timeout" response should be appear in the Display config results for the created request
    Then I validate that the "Cancel" button should be clickable
    When I click on "Cancel" button
    Then I click on "Confirm" button
    Then I validate the pop-up message for "Cancel request"
    And  I click on "servicesSidebar" button

