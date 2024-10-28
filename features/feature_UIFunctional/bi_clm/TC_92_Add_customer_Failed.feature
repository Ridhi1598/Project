Feature: BI CLM Customers-Add customer details input validation- Failed

  Scenario: This scenario test the add customer functionality based on Customer ID and Customer Name
    Given I read test data for testcase
    When "Customers" page title should be "Customers"
    Then I click on "add customer" button
    And Wait for the "createcustomerPopup" popup to appear
    When I validate that all the fields should be clear
    Then I check "save" button is enabled
    And I left "CustomerID" blank
    And I enter "CustomerName"
    When I check "save" button is enabled
    Then I clear all fields of "Customer"
    When I validate that all the fields should be clear
    Then I enter "CustomerID"
    And I left "CustomerName" blank
    When I check "save" button is enabled
    Then I clear all fields of "Customer"



  Scenario: Adding prexisting customer
    When I enter the prexisting "customer id" and "CustomerName"
    Then I click on "save" button
    And I validate the "customerexists" "success" alert "message"
    And I clear all fields of "Customer"



  Scenario: This scenario test the add customer functionality based on Email
    When I validate that all the fields should be clear
    Then I enter "CustomerID"
    And I enter "CustomerName"
    And I enter "Email"
    When I check "save" button is enabled
    Then I click on "cancel" button
    And I click on "Refresh" button


