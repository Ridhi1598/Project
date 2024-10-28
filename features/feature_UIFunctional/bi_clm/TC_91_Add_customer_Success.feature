Feature: BI CLM Customers-Add customer details input validation-  Success



  Scenario: Customers - Add new customer
    Given I read test data for testcase
#    When I should land on "Home" page
#    Then "Home" page title should be "Services"
    When I click on "CustomersSideBar" button
    Then "Customers" page title should be "Customers"
    And I click on "add customer" button
    When I enter "CustomerID" and "CustomerName"
    Then I enter "Email"
    When I click on "save" button
    Then I validate the "customercreated" "success" alert "message"
    And I filter the "Customer" by "CustomerID" and user "exist" in the results
    And I click on "Refresh" button