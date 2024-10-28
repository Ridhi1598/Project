@portal @tc13
Feature: Contact Support
  This feature tests the contact support functionality for BI Portal

  Scenario: Successful contact support email
    Given I read test data for testcase
    When "Home" page title should be "Services"
    Then I wait for the "current page" to load
    Then I click on "contactSupport" button
    And Wait for the "contactSupportPopup" popup to appear
    And I enter the details and click "submit"
    Then I validate the "email" "success" alert "message"
