@portal @tc66
Feature: User Permission - Execute
User should not be able to Execute the service if the user has read only rights

  Scenario: User should not be able to rollback a service if user permission is read only

    Given I read test data for testcase
    Then I click on "serviceUpdateSidebar" button
    When "ServiceUpdate" page title should be "Service Update Queue"
    When I search the request by using "CSID" from Service Update Queue page
    Then I click on "firstRequestServiceUpdateQueue" button
    And I validate that the "Execute" button should not be visible for read-only user
