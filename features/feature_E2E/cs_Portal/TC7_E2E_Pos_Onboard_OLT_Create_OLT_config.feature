@OLTDryRun @cse2e
Feature: Onboard_OLT_Create_OLT_config
  This feature test the functionality of create OLT config

  Scenario: Onboard_OLT_Create_OLT_config
    Given I set data values against testcase "36"
    Given I should land on CS Home page
    Then "Home" page title should be "Dashboard"
    When I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingOLT"
    Then "OnboardingOLT" page title should be "Onboarding - OLT"
    Then I search for available "OLT" to "Onboarding"
    And  I click on "Onboard" button
    And I enter the Onboarding "OLT" Configuration Parameters
    Then I click on "Next" button
    When I enter the Onboarding OLT Configuration details
    And I click on "DryRun" Button
    Then Wait for the OLT DryRun status response and validate the status for "success" scenario