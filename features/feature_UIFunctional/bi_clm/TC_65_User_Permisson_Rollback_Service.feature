@portal @tc65
Feature: User Permission - Rollback
User should not be able to Rollback a service if the user has read only rights

  Scenario: User should not be able to rollback a service if user permission is read only
    Given I read test data for testcase
    When I login into the application
    Then "Home" page title should be "Services"
    Then I validate that the "advanceFilter" button should be clickable
    Then I click on "advanceFilter" button
    When I search the service by "CSID" only
    Then I go to "Services" page
    When I click on "rollback" button
    Then I wait for the loader to be disabled
    And I wait for the "parameterInformation" element to be visible
    When Select the version from the dropdown to rollback the service for read-only user
    Then I validate that the "rollbackParameterInformation" should be disable
