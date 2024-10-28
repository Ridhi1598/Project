@portal @tc34
Feature: Update parameters for portal - Non existing service
  This feature tests the Update parameters for non existing service

  Scenario: Update parameters for valid service with invalid values
    Given I read test data for testcase
#    When I navigate to "services" page
    Then "Home" page title should be "Services"
    When I click on "advanceFilter" button
    Then I search and validate for a non existing service-id 101010
    And I click on "clearAllFilter" button




    