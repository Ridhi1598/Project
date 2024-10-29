@BNGDryRun @cse2e
Feature: Onboard_BNG_Create_BNG_config
  This feature test the functionality of create BNG config

  Scenario: Onboard_BNG_Create_BNG_config
    Given I set data values against testcase "34"
    Given I should land on CS Home page
    Then "Home" page title should be "Dashboard"
    When I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    Then I search for available "BNG" to "Onboarding"
    And I click on "Onboard" button
    And I enter the Onboarding "BNG" Configuration Parameters
    And I click on "Next" button
    Then I enter the Onboarding BNG Configuration details
    And I click on "DryRun" button
    And Wait for the BNG DryRun status response and validate the status for "success" scenario






