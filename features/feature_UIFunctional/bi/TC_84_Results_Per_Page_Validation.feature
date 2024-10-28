Feature: Service Dashboard Results Per Page Validation
    This feature tests if the correct number of results are shown per page as per dropdown selection

  Scenario: Check Search Results
    Given I set data values against testcase "84"
    Given I should land on BI Home page
    Given "Home" page title should be "BI service dashboard"
    Then I iteratively validate the number of results displayed per page