Feature: BI CLM Display customer services

  Scenario: Display services related to customer
    Given I read test data for testcase
    When I click on "Customers" button
    Then "Customers" page title should be "Customers"
    And I click on "Refresh" button
    When I filter the "Customer" by "CustomerID" and user "exist" in the results
    Then I click on "edit" icon
    And Count "serviceRelated"

