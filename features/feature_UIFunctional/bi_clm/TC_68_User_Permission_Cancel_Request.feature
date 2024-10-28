@portal @tc68
Feature: User Permission - Cancel
User should not be able to Cancel the service if the user has read only rights

  Scenario: User should not be able to rollback a service if user permission is read only

    Given I read test data for testcase
    And I validate that the "Cancel" button should not be visible for read-only user
