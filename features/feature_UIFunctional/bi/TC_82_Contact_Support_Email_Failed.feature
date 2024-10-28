Feature: Contact Support Email
    This feature tests the functionality of Contact support email

  Scenario: Send contact support email: Failed
    Given I set data values against testcase "82"
    Given I should land on BI Home page
    When "Home" page title should be "BI service dashboard"
    Then I navigate to "mailIcon" section
    And Wait till the Contact support popup will shown up
    Then I navigate view by clicking on "contactSupportMailSave"
    Then Validate the input validation messages for contact support email