@portal @tc64
Feature: User Permission
  User should not be able to Update the service from if user permission is read only

  Scenario: User should not be able to update a service from if user permission is read only
    Given I read test data for testcase
    When I login into the application
    Then "Home" page title should be "Services"
    When I wait for the "Service" to load
    Then I validate that the edit button should be disable for read-only user




