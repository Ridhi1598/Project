@OLTPush @cse2e
Feature: Onboadring OLT push OLT config
  This feature test the functionality of push OLT config

Scenario: Onboarding BNG push config
    Given I set data values against testcase "37"
    Given I should land on CS Home page
    Then "Home" page title should be "Dashboard"
    When I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingOLT"
    Then "OnboardingOLT" page title should be "Onboarding - OLT"
    Then I search for available "OLT" to "Commit"
    And I validate the "OLT" Status should be "DRY RUN - COMPLETED"
    And  I click "OnboardingStatus" button
    Then I validate the generated configurations for "olt"
    And I click on "Commit" button
    Then I click on "CommitConfirmation" button