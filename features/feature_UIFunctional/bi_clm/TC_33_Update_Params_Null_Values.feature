@portal @tc33
Feature: Update parameters for portal - Valid service with Null values
  This feature tests the Update parameters for a valid service with Null values

  Scenario: Update parameters for valid service with invalid values
    Given I read test data for testcase
#    When I navigate to "services" page
    Then "Home" page title should be "Services"
    Then I validate that the "advanceFilter" button should be clickable
    Then I click on "advanceFilter" button
    When I search the service-id to validate the Update parameters
    Then I click on "firstEdit" button
    When I click on "serviceEditDetails" button
    Then I go to "ServiceUpdate"
    When I edit the field value of "ipv4ProviderPrefix1" and set it to "NULL"
    Then Validate the popup message should appears for "Null value"
    And I click on "servicesSidebar" button



    