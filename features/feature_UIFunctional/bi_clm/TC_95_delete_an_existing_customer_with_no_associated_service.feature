Feature: BI CLM Customers-Delete Existing Customer
  This feature tests the login and logout functionality for BI Portal

  Scenario: Customers-Delete Existing Customer
    Given I read test data for testcase
    When I click on "Customers" button
    Then "Customers" page title should be "Customers"
    And I click on "Refresh" button
    When I filter the "Customer" by "CustomerID" and user "exist" in the results
    Then I click on "edit" icon
    And Count "no_data"
    When I click on "Customers" button
    Then "Customers" page title should be "Customers"
    And I filter the "Customer" by "CustomerID" and user "exist" in the results
    When I click on "delete" icon
    Then I click on "confirm" button
    When I validate the "customerdeleted" "success" alert "message"
    Then I filter the "Customer" by "CustomerID" and user "does'nt exist" in the results
    And I click on "Refresh" button


