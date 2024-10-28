@portal @tc37
Feature: Display config - Mock failed response
  This feature tests the functionality related to mock the failed response in Display config

  Scenario: Mock failed response - Display config 
    Given I read test data for testcase
#    When I navigate to "services" page
    Then "Home" page title should be "Services"
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
    When I search the request by using "CSID" from Service Update Queue page
    Then Fetch the request-id from the Total Requests table of Service Update Page
    Then Mock "display-config-failed" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    Then "Failed" response should be appear in the Display config results for the created request
    