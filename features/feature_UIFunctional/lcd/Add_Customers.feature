Feature: Add Customer
    This features tests the functionality related to add customer

Background:
    Given I should land on Home page

@addCustomers, @demo
Scenario: Add Customer to the customer list
    When "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
    Then I navigate view by clicking on "ManageCustomers"
    Then "ManageCustomers" page title should be "Manage Customers"
    And I navigate view by clicking on "AddCustomerButton"
    Then I click on "AddCustomerButton" button and fill customer details
    Then I navigate view by clicking on "SubmitButton"
    Then Customer name should be displayed in the list of customers with details shown as chosen