@portal @tc14
Feature: Contact Support
  This feature tests the contact support functionality for BI Portal

  Scenario: Contact support email reject
    Given I read test data for testcase
    When "Home" page title should be "Services"
    Then I wait for the "current page" to load
    And I click on "contactSupport" button
    And Wait for the "contactSupportPopup" popup to appear
    And I click on "submit" button
    But I validate the "subject" field "error" message
    And I validate the "description" field "error" message
    Then I click on "cancelContactSupport" button
