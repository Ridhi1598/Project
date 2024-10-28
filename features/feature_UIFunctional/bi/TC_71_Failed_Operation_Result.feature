Feature: Failed Operation Result
  This feature tests the functionality showing a reason for a failed operation

  Scenario: Failed Operation Result
    Given I set data values against testcase "71"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I search for "FAILED" Operation Result
    And Validate all Operation Result should be "FAILED"
    Then I should see the reason for failure in a pop up bubble
    Then I click on "FAILED" Operation Result text
    Then Validate alert Modal should open and display same reason for failure
    And I click on "AlertcloseButton" button
    Then I click on "AlertButton" button
    And Validate the same reason for failure display on alert Modal
    Then Close the error window