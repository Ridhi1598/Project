Feature: New User Registration
  This feature tests the functionality of registering a new user

  @register
  Scenario: Register new user
    Given I set data values against testcase "80"
    And I fill registration details and should land on the Business Internet Portal
    When "UserRegistration" page title should be "Business Internet Portal"
    Then I verify the new user registration details and register
    And "Landing" page title should be "TINAA BUSINESS INTERNET SERVICES"