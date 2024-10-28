Feature: Error Message Will show On click of status button incase of Rejected- Work Orders Page

  Scenario: Error message for click on status button- Rejected
    Given I read test data for testcase
#    Then I go to "WorkOrders" page
    And I click on "clearFilter" button
    Then I click on "advanceFilter" button
    And I enter "Status"
    When I click on "SearchResult" button
    When I click on "Rejected" button
    Then Wait for the "ErrPopup" popup to appear
    When I click on "close" button