@portal @tc84
Feature: MWR - Operation type from Transactions page
  This feature validates the operation type should contain MWR in it

  Scenario: Operation type should contain MWR in it
    Given I read test data for BI_CLM UI testcase
    Then "Home" page title should be "Services"
    When I click on "Transactions" button
    Then "Transactions" page title should be "Transactions"
    Then I validate that the "advanceFilter" button should be clickable
    When I click on "advanceFilter" button
    Then I search the Transactions by using "CSID_OperationType"
    When I click on "SearchResult" button
    Then I wait for the "Transaction page" to load
    Then I validate that the operation type should contain MWR in it
    And I click on "servicesSidebar" button

