@BNGPush @cse2e
Feature: Onboadring BNG push BNG config
  This feature test the functionality of push BNG config

  Scenario: Onboarding BNG push config
    Given I set data values against testcase "35"
    Given I should land on CS Home page
    Then "Home" page title should be "Dashboard"
    When I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    And I search for available "BNG" to "Commit"
    Then I validate the "BNG" Status should be "DryRun-Completed"
    And  I click "OnboardingStatus" button
    Then I validate the generated configurations for "bng"
    And I click on "Commit" button
    Then I click on "CommitConfirmation" button
