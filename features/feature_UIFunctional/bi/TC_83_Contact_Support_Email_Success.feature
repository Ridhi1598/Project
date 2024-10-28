Feature: Contact Support Email
    This feature tests the functionality of Contact support email

  Scenario: Send the contact support email: Success
    Given I set data values against testcase "83"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I navigate to "mailIcon" section
    And wait till the Contact support popup will shown up
    And I send the contact support email