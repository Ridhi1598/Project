Feature: Service Dashboard Total Result Pages Against Resluts Selected Per Page
    This feature tests if the correct number of total pages are shown as per results per page dropdown selection

  Scenario: Check Search Results
    Given I set data values against testcase "86"
    Given I should land on BI Home page
    Given "Home" page title should be "BI service dashboard"
    Then I iteratively verify total number of pages displayed