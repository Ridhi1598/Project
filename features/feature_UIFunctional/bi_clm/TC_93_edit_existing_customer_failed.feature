Feature: BI CLM Edit Customer details- Failed

  Scenario: Update Customer details to null
    Given I read test data for testcase
    When I filter the "Customer" by "CustomerID" and user "exist" in the results
    Then I click on "edit" icon
    When I clear all fields of "edit"
    Then I check "save" button is enabled


  Scenario: Update Customer email
    When I enter "editcustomerName"
    Then I enter "editEmail"
    And I check "save" button is enabled
    When I click on "cancel" button
    Then I click on "Refresh" button
