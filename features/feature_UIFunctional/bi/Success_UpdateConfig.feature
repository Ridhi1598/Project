Feature: Edit and execute a pending update request
  This feature tests the functionality of update parameters information from service queue page


  Scenario: Modify service from service queue page
    Given I set data values against testcase "17"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I click on "ServiceUpdate" button
#    Then Search the selected service ID and click on the result
#    And Update the required values of parameter information for "success" scenario
#    And Wait for next page to load and validate the configurations for "success" scenario
    Then I click on "Review" button
    Then I validate that "CurrentConfigData" should display expected response
    Then I click on "expectedConfigButton" button
    Then I wait for expectedConfig valid response
    Then I validate that "ExpectedConfigData" should display expected response
    Then I click on "EditButton" button
    And Update the "success" IPV4ProviderPrefixes in Parameter edit Form
    Then I click on "AlertSave" button
    Then I click on "AlertOk" button
    Then I click on "Review" button
    Then I wait to page be loaded
    Then I validate that "CurrentConfigData" should display expected response
    Then I click on "expectedConfigButton" button
    Then I validate that "ExpectedConfigData" should display expected response
    Then I click on "expectedConfigButton" button
    Then I validate Expected config for "success" scenario
    Then I validate Current config should different than expected config
    Then I click on "ReviewUpdateClose" button
    Then I click on "ExecuteButton" button
    Then I fill the required parameters for Execution details form
    Then I validate the customer service is not present in service update queue
    Then I click on "Dashboard" button
    Then Service should be updated for "SUBMITTED" in the BI service dashboard table
    Then I wait and for operation to be completed and refresh the page
    Then Service should be updated for "COMPLETED" in the BI service dashboard table