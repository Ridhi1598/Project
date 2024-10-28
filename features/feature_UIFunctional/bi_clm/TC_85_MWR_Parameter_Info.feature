@portal @tc85
Feature: MWR - Parameter Information
  Parameter information should display MWR details only

  Scenario: This scenario validate that the parameter information displays MWR details only
    Given I read test data for BI_CLM UI testcase
    When "Home" page title should be "Services"
    Then I click on "Transactions" button
    When "Transactions" page title should be "Transactions"
    Then I validate that the "advanceFilter" button should be clickable
    When I click on "advanceFilter" button
    Then I search the Transactions by using "OperationType"
    When I click on "SearchResult" button
    Then I wait for the "Transaction page" to load
    When I click on "request_id_transactions" button
    Then I wait for the "parameterInfo" element to be visible
    When validate the access type should be "MWR" on Parameter Information page
    Then MWR "Tunnel" value should be visible on Parameter Information page
    And I click on "servicesSidebar" button
