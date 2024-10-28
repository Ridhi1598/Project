@TC_51
Feature: RollBack - Display current and expected config: Success
  This feature tests the functionality related to displaying the current and expected config - Success

  Scenario: Display current and expected config: Success
    Given I read test data for testcase
#    When I navigate to "services" page
    Then "Home" page title should be "Services"
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
    When Mock "display-config-success" response to "RMQ" "com.telus.tinaa.bsaf.clm.bi.ingestion.response" queue
    Then "Success" response should be appear in the Display config results for the created request
