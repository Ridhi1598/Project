Feature: Validate Home Page nad Manage Customer Page
    This features tests the functionality related to landing Home & Manage Customer page

@buildtest @temp_demo
Scenario: Add Customer to the customer list
    Given I should land on Home page
    When "Home" page title should be "CPE AUDIT/REMEDIATION USE CASE"
    And I navigate view by clicking on "ManageCustomers"
    Then "ManageCustomers" page title should be "Manage Customers"
