Feature: Manage Customers
  This feature tests the functionality related to customer management

  Background:
    Given I should land on Home page
    Given "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
    Given I navigate view by clicking on "ManageCustomers"
    Given "ManageCustomers" page title should be "MANAGE CUSTOMERS"

  @editCustomer
  Scenario: Edit customer's details
    When Search customer by name
    And Open Edit Customer form by clicking on Edit button
    And Update Customer details on Edit Customer form
    Then Updated details should be reflected in the list of Customers

  @deleteCustomer
  Scenario: Delete a customer profile
    When Search customer by name
    When Click on Delete button to open "deleteCustomerView"
    And Enter customer name for verification
    And I click on "deleteCustomerSubmit" button
    And Enter customer name to confirm
    Then Customer name should not be displayed in the list of customers
    And Commit the delete operation

