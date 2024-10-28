@portal @tc36
Feature: Update parameters of the service whose state is pending - Failed
  This feature tests the functionality related to Update the parameters for pending state service  

  Scenario: Update parameter for a pending service - Failed
    Given I read test data for testcase
    When I login into the application
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
    Then I validate the alert Message for "in-process" Service
    And I click on "Services" button