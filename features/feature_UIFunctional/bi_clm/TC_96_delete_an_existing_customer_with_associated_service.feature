Feature: BI CLM Customers-Delete Existing Customer
  This feature tests the login and logout functionality for BI Portal

  Scenario: Customers-Delete Existing Customer
    Given I read test data for testcase
    When I click on "Refresh" button
    Then I click on "Customers" button
    When "Customers" page title should be "Customers"
    Then I filter the "Customer" by "CustomerID" and user "exist" in the results
    When I click on "edit" icon
    Then Count "serviceRelated"
    When I click on "Customers" button
    Then I filter the "Customer" by "CustomerID" and user "exist" in the results
    When I click on "delete" icon
    Then I click on "confirm" button
    And I validate the "customerdeleted" "failed" alert "message"

