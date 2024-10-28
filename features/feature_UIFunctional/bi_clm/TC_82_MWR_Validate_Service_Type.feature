@portal @tc82
Feature: MWR - Validate Service Type
  This feature tests the MWR service type

  Scenario: This scenario validate the MWR service type
    Given I read test data for BI_CLM UI testcase
    When I should land on "Home" page
    Then "Home" page title should be "Services"
    Then I validate that the "advanceFilter" button should be clickable
    When I click on "advanceFilter" button
    Then I search the service by "CSID" only
    Then Validate the service type should be "PON-MWR"
    And I click on "clearAllFilter" button