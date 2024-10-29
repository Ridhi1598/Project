@tc_94
Feature: Negative - Onboarding BNG with empty values
   This feature tests the negative scenario of onboarding the BNGs with empty values

  Scenario: Onboarding BNG with empty values
    Given I set data values against testcase "94"
#
#    Given I should land on CS Home page
#    Then "Home" page title should be "Dashboard"
#
    When I expand the "Onboarding" sidebar
    And I navigate view by clicking on "OnboardingBNG"
    Then "OnboardingBNG" page title should be "Onboarding - BNG"
    When I click on "OnboardANewBNGPair" button
#    Then I click on "Next" button
#    Then I validate the error message for "emptyBNG" test
