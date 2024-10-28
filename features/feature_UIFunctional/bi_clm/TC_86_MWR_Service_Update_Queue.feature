@portal @tc86
Feature: MWR - Service Update Queue
  On click of "Edit" button MWR section should be enabled

  Scenario: This scenario validates if main BI service contain MWR then on click of "Edit" button MWR section should be enabled
    Given I read test data for BI_CLM UI testcase
    When "Home" page title should be "Services"
    Then I validate that the "advanceFilter" button should be clickable
    Then I click on "advanceFilter" button
    When I search the service by "CSID" only
    Then I click on "firstEdit" button
    When I click on "serviceEditDetails" button
    Then Validate that the "QoS" field should be enable
    Then Validate that the "Prefixes" field should be enable
    When I update the Qos and prefix values of the selected service
    Then I click on "save" button
    When I validate that the alert message should appear for "Service Update"
    Then I wait for the "Service Update Page" to load
    Then "ServiceUpdate" page title should be "Service Update Queue"
    Then Fetch the request-id from the Total Requests table of Service Update Page
    When Mock "display-config-success" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    Then "Success" response should be appear in the Display config results for the created request
    When I click on "edit" button
    Then I wait for the loader to be disabled
    Then I click on "serviceEditDetails" button
    Then I validate that the MWR details should be "enabled"
    And I click on "servicesSidebar" button