@portal @tc39
Feature: Update parameters for portal - Cancel Request
  This feature tests the functionality related to cancel the update request

  Scenario: This scenario test the functionality related to cancel the update request
    Given I read test data for testcase
#    When I navigate to "services" page
    Then "Home" page title should be "Services"
    And I validate that the "ServiceUpdate" button should be clickable
    And I click on "ServiceUpdate" button
    When "ServiceUpdate" page title should be "Service Update Queue"
    Then I search the request by using "CSID" from Service Update Queue page
    When I click on "firstRequestServiceUpdateQueue" button
    Then I validate that the "Cancel" button should be clickable
    When I click on "Cancel" button
    Then I click on "Confirm" button
    Then I validate the pop-up message for "Cancel request"
    And I click on "servicesSidebar" button