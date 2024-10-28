Feature: BI CLM Edit Customer details- Successful

  Scenario: Update Customer details to null
    Given I read test data for testcase
    When I click on "Customers" button
    Then "Customers" page title should be "Customers"
    And I click on "Refresh" button
    When I filter the "Customer" by "CustomerID" and user "exist" in the results
    Then I click on "edit" icon
    And I clear all fields of "edit"
    When I enter "editcustomerName"
    Then I enter "editEmail"
    And I click on "save" button
    When I validate the "customeredit" "success" alert "message"
    Then I filter the "Customer" by "CustomerName" and user "exist" in the results
    And I click on "Refresh" button


